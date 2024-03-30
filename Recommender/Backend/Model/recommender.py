from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF, VectorAssembler, MinMaxScaler, StringIndexer, OneHotEncoder
from pyspark.ml.linalg import Vectors, DenseMatrix
from pyspark.sql.functions import col, array, lit, countDistinct, collect_list, row_number, udf, explode
from pyspark.sql.types import ArrayType, IntegerType
from pyspark.ml.linalg import SparseVector
from pyspark.sql.window import Window


from pymongo import MongoClient

# Create a SparkSession
spark = SparkSession.builder \
    .appName("GameRecommender") \
    .config("spark.driver.host", "localhost") \
    .getOrCreate()

# Register the MySQL JDBC driver
spark.sparkContext._jvm.Class.forName("com.mysql.cj.jdbc.Driver")

# JDBC connection URL
jdbc_url = "jdbc:mysql://db:3306/games_db?user=root&password=secret"

# Read data from the database tables
game_attributes_df = spark.read.format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "game_attributes") \
    .load()

player_history_df = spark.read.format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "player_history") \
    .load()

print("Game attributes DataFrame schema:")
game_attributes_df.printSchema()
print("Number of rows:", game_attributes_df.count())
print("Number of columns:", len(game_attributes_df.columns))

print("Player history DataFrame schema:")
player_history_df.printSchema()
print("Number of rows:", player_history_df.count())
print("Number of columns:", len(player_history_df.columns))

# Preprocess game attributes
def preprocess_game_attributes(game_attributes_df):
    # Perform text vectorization on game name and themes
    text_columns = ['game_name', 'themes']
    for col in text_columns:
        tokenizer = Tokenizer(inputCol=col, outputCol=f"{col}_tokens")
        game_attributes_df = tokenizer.transform(game_attributes_df)
        hashingTF = HashingTF(inputCol=f"{col}_tokens", outputCol=f"{col}_tf")
        game_attributes_df = hashingTF.transform(game_attributes_df)
        idf = IDF(inputCol=f"{col}_tf", outputCol=f"{col}_tfidf")
        game_attributes_df = idf.fit(game_attributes_df).transform(game_attributes_df)

    # Normalize numerical columns
    numerical_columns = ['free_spins', 'paylines', 'rtp']
    assembler = VectorAssembler(inputCols=numerical_columns, outputCol="numerical_features")
    game_attributes_df = assembler.transform(game_attributes_df)
    scaler = MinMaxScaler(inputCol="numerical_features", outputCol="scaled_numerical_features")
    game_attributes_df = scaler.fit(game_attributes_df).transform(game_attributes_df)

    # One-hot encode categorical columns
    categorical_columns = ['wild_symbols', 'scatter_symbols', 'bonus_rounds', 'multipliers', 'jackpots',
                           'reel_mechanisms', 'gamble_feature', 'mystery_symbols', 'random_triggers', 'volatility']

    # Drop columns with only one unique value
    columns_to_drop = []
    for col in categorical_columns:
        distinct_count = game_attributes_df.agg(countDistinct(col).alias("distinct_count")).collect()[0]["distinct_count"]
        if distinct_count == 1:
            columns_to_drop.append(col)
            print(f"Dropping column '{col}' due to having only one unique value.")

    game_attributes_df = game_attributes_df.drop(*columns_to_drop)
    categorical_columns = [col for col in categorical_columns if col not in columns_to_drop]

    # Encode remaining categorical columns
    for col in categorical_columns:
        indexer = StringIndexer(inputCol=col, outputCol=f"{col}_index")
        game_attributes_df = indexer.fit(game_attributes_df).transform(game_attributes_df)
        encoder = OneHotEncoder(inputCol=f"{col}_index", outputCol=f"{col}_encoded")
        game_attributes_df = encoder.fit(game_attributes_df).transform(game_attributes_df)

    return game_attributes_df

# Preprocess game attributes
preprocessed_game_attributes_df = preprocess_game_attributes(game_attributes_df)

print("Preprocessed game attributes DataFrame schema:")
preprocessed_game_attributes_df.printSchema()
print("Number of rows:", preprocessed_game_attributes_df.count())
print("Number of columns:", len(preprocessed_game_attributes_df.columns))

# Create the feature vector
feature_columns = [col for col in preprocessed_game_attributes_df.columns if col.endswith("_tfidf") or col.endswith("_encoded") or col == "scaled_numerical_features"]
assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
preprocessed_game_attributes_df = assembler.transform(preprocessed_game_attributes_df)

print("Game attributes DataFrame with feature vector schema:")
preprocessed_game_attributes_df.printSchema()
print("Number of rows:", preprocessed_game_attributes_df.count())
print("Number of columns:", len(preprocessed_game_attributes_df.columns))

# Calculate cosine similarity between game features
def cosine_similarity(v1, v2):
    return v1.dot(v2) / (v1.norm(2) * v2.norm(2))

# Create a 1000x1000 similarity matrix
num_games = 1000
similarity_matrix = DenseMatrix(num_games, num_games, [0.0] * (num_games * num_games))

# Collect the features as a list
features_list = preprocessed_game_attributes_df.select("game_id", "features").orderBy("game_id").collect()

for i in range(num_games):
    game1 = features_list[i][1]
    for j in range(num_games):
        game2 = features_list[j][1]
        similarity = cosine_similarity(game1, game2)
        similarity_matrix.values[i * num_games + j] = similarity

print("Similarity matrix:")
print(similarity_matrix)

# Convert the similarity matrix to a PySpark DataFrame
similarity_df = spark.createDataFrame([(i, j, float(similarity_matrix.values[i * num_games + j])) for i in range(num_games) for j in range(num_games)], ["item_id", "similar_item_id", "similarity"])

# Function to get the k-nearest neighbors for a given item
@udf(returnType=ArrayType(IntegerType()))
def get_knn(item_id, similarity_df_name, k):
    similarity_df = spark.table(similarity_df_name)
    similar_items = similarity_df.filter(col("item_id") == item_id).orderBy(col("similarity").desc()).limit(k+1).select("similar_item_id").collect()
    return [row.similar_item_id for row in similar_items if row.similar_item_id != item_id][:k]

# Function to create item neighborhoods using kNN
def create_item_neighborhoods(similarity_df, k):
    window_spec = Window.partitionBy("item_id").orderBy(col("similarity").desc())
    item_neighborhoods_df = similarity_df.withColumn("rank", row_number().over(window_spec)) \
        .filter(col("rank") <= k+1) \
        .filter(col("item_id") != col("similar_item_id")) \
        .groupBy("item_id") \
        .agg(collect_list("similar_item_id").alias("neighbors"))
    return item_neighborhoods_df

k = 20  # Number of nearest neighbors
item_neighborhoods = create_item_neighborhoods(similarity_df, k)

# Print the neighbors for item 0
print(f"Neighbors of item 0: {item_neighborhoods.filter(col('item_id') == 0).select('neighbors').first()[0]}")

item_neighborhoods_list = [
    {"item_id": row.item_id, "neighbors": row.neighbors}
    for row in item_neighborhoods.collect()
]

# Connect to MongoDB
client = MongoClient("mongodb://root:secret@mongodb:27017/")
db = client["recommendations"]
collection = db["item_neighborhoods"]
collection.delete_many({})
collection.insert_many(item_neighborhoods_list)

spark.stop()
