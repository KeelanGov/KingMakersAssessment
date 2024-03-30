"""
Web scraping scripts to retrieve data for poulating game_names
from online slots' websites.
"""

import requests
import logging
from lxml import html
from tqdm import tqdm
import time

logger = logging.Logger(__name__)
logger.setLevel(logging.INFO)

def scrape_first_site(url="https://rwnewyork.com/new-york-casino/slots/slot-list/"):
    """
    Scraping of site rwnewyork.com for slot game names
    Expected data output: ~563 slot game names
    """
    logger.info(f"Starting to scrape site {url}")
    game_names = []

    try:
        # verify set to false due to SSL issues, needs to be replaced CA certs if replicated.
        response = requests.get(url, verify=False)

        if response.status_code == 200:
            logger.info("Request to site successful.")
            tree = html.fromstring(response.content)

            # xpath used due to time constraints - use class in future - more fault tolerant/less subject to smaller changes
            div_element = tree.xpath('/html/body/div[1]/div[2]/div[2]/div/main/article/div/div')[0]

            # Searching child tags/elements for name in text
            if div_element is not None:
                content = div_element.text_content().strip()
                lines = content.split('\n')
                for line in lines:
                    line = line.strip("'")
                    if line:
                        game_names.append(line)
            else:
                logger.error("There was an error accessing the div element. HTML of site needs to be checked.")
                raise ValueError("The specified div element was not found on the webpage.")

        else:
            logger.error("Request to site was unsuccessful.")
            # Error handling for status codes needs to be added
            raise ValueError(f"The webpage is not accessible. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        raise e
    
    logger.info(f"Scraping completed, game names collected: {len(game_names)}")
    return game_names

def scrape_second_site(url="https://www.ybrcasinoandsportsbook.com/casino/slots"):
    """
    Scraping of site ww.ybrcasinoandsportsbook.co for slot game names
    Very similar to first scraper
    Expected data output: ~209 slot game names
    """
    logger.info(f"Starting to scrape site {url}")
    game_names_2 = []

    try:
        # verify set to false due to SSL issues, needs to be replaced with CA certs if replicated.
        response = requests.get(url, verify=False)

        if response.status_code == 200:
            logger.info("Request to site successful.")
            tree = html.fromstring(response.content)

            # xpath used due to time constraints - use class in future - more fault tolerant/less subject to smaller changes
            div_elements = tree.xpath('/html/body/div[2]/section[1]/div/div/div[2]')

            # Searching child tags/elements for name in text
            if div_elements:
                for div in div_elements:
                    paragraphs = div.findall('.//p')
                    for paragraph in paragraphs:
                        br_tags = paragraph.findall('.//br')
                        values = [br.tail.strip() for br in br_tags if br.tail]
                        game_names_2.extend(values)
                
            else:
                logger.error("There was an error accessing the div element. HTML of site needs to be checked.")
                raise ValueError("The specified div element was not found on the webpage.")
        else:
            logger.error("Request to site was unsuccessful.")
            # Error handling for status codes needs to be added
            raise ValueError(f"The webpage is not accessible. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        raise e
    
    logger.info(f"Scraping completed, game names collected: {len(game_names_2)}")
    return game_names_2

def scrape_third_site(url="https://casino.guru/free-casino-games/slots"):
    """
    Scraping of site ww.ybrcasinoandsportsbook.co for slot game names
    Wish I found this site first, has a lot of game names.
    Expected data output: ~141400 slot game names
    """
    logger.info(f"Starting to scrape site {url}")
    try:
        # verify set to false due to SSL issues, needs to be replaced with CA certs if replicated.
        response = requests.get(url, verify=False)
        
        tree = html.fromstring(response.content)    
        input_element = tree.find('.//input[@class="js-paging-goto"]')
        
        if input_element is not None:
            # Get the value of the 'data-max' attribute - the max number of paginations
            data_max_value = input_element.get('data-max')
            logger.info(f"The value of the 'data-max' attribute is: {data_max_value}")
        else:
            logger.error("Error when trying to find max number of paginations through data-max attribute")
            raise ValueError("Input element with class 'js-paging-goto' not found.")

        
        game_names_3 = []
        logger.info("Starting to search through pages")
        for page_num in tqdm(range(int(data_max_value))):
            time.sleep(1)
            url = f"https://casino.guru/free-casino-games/slots/{page_num}"
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                tree = html.fromstring(response.content)
                parent_div = tree.find_class('results-content js-results-content')
                if parent_div:
                    # Find all child div elements inside the parent div
                    child_divs = parent_div[0].findall('.//div')
                
                    # Iterate over child divs and find <a> tags with the class "game-item-name"
                    for child_div in child_divs:
                        game_item_links = child_div.findall('.//a[@class="game-item-name"]')
                
                        # Print the text and href attributes of the <a> tags
                        values = [link.text.strip() for link in game_item_links]
                        game_names_3.extend(values)
                
                else:
                    logger.error("There was an error finding the parent_div")
                    raise ValueError("Parent div element not found.")
                
            else:
                logger.error("Request to site was unsuccessful.")
                # Error handling for status codes needs to be added
                raise ValueError(f"The webpage is not accessible. Status code: {response.status_code}")


    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        raise e
    
    logger.info(f"Scraping completed, game names collected: {len(game_names_3)}")
    return game_names_3