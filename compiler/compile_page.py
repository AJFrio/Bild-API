from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pprint
from bs4 import BeautifulSoup
from openai import OpenAI
import os

dropdowns = 'sl-tree'
dropdowns_class = 'foo__PxTree-module__sltree'
dropdown = 'sl-tree-item'
dropdown_class = 'foo__PxTreeItem-module__sltreeitem foo__PxTreeItem-module__childsltreeitem'
base_url = 'https://bildexternalapi.portledocs.com/#/docs/apireference'

request_info_style = 'display: flex; flex-direction: column; justify-content: space-between; visibility: visible;'

def check_request():
    with open('compiler/links.txt', 'r', encoding='utf-8') as file:
        urls = file.readlines()
        file.close()
    for url in urls:
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode (no GUI)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        request_page = driver.page_source
        soup = BeautifulSoup(request_page, 'html.parser')
        request_info = soup.find(style=request_info_style)
        print(request_info)
        with open('compiler/request_info.txt', 'a', encoding='utf-8') as file:
            file.write(request_info)
            file.write('\n\n\n')
        file.close()


if __name__ == "__main__":
    check_request()