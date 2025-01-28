from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pprint
from bs4 import BeautifulSoup
from openai import OpenAI
import os

dropdowns = 'sl-tree'
dropdowns_class = 'foo__PxTree-module__sltree'
dropdown = 'sl-tree-item'
dropdown_class = 'foo__PxTreeItem-module__sltreeitem  null'
base_url = 'https://bildexternalapi.portledocs.com/#/docs/apireference'

def select_dropdowns():
    chrome_options = Options()
    #chrome_options.add_argument('--headless')  # Run in headless mode (no GUI)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(base_url)
    time.sleep(4)

    main_dropdown = 'foo__ApiSiderbarList-module__tagTitle'
    specific_page = 'foo__PxTreeItem-module__titleContainer'
    dashboard = 'dashboardWrapper'
    #USE THESE
    name_p_style = 'font-size: var(--px-font-size-large); font-style: normal; font-weight: 600; line-height: normal; text-transform: capitalize; color: rgb(60, 57, 55);'
    top_banner_style = 'width: 100%; display: flex; flex-direction: row; align-items: center; padding: 6px 5px; border-radius: 8px; gap: 12px; position: sticky; top: -24px; z-index: 0; font-size: var(--px-font-size-xsmall); background: var(--px-color-neutral-100); border: 1px solid var(--px-color-neutral-200);'
    description_p_class = 'PxEditorLexicalTheme__paragraph'
    request_body_style = 'width: 100%; display: flex; gap: 5px; flex-direction: column;'

    # Find all divs with the specified class and click them
    divs_to_click = driver.find_elements(By.CLASS_NAME, specific_page)
    for div in divs_to_click[:5]:
        div.click()
        time.sleep(.5)  # Optional: wait a bit between clicks if needed
        
        # Use JavaScript to find the element with the specific style
        try:
            dashboard_div = driver.execute_script(
                "return Array.from(document.querySelectorAll('p')).find(p => p.style.cssText.includes(arguments[0]));",
                name_p_style
            )
            if dashboard_div:
                dashboard_text = dashboard_div.text
                top_banner_div = driver.execute_script(
                    "return Array.from(document.querySelectorAll('div')).find(div => div.style.cssText.includes(arguments[0]));",
                    top_banner_style
                )
                top_banner_text = top_banner_div.text.replace('\n', '##').replace('Change Base URL Selection', '')
                description_div = driver.find_element(By.CLASS_NAME, description_p_class)
                description_text = description_div.text
                try:
                    request_body_div = driver.execute_script(
                        "return Array.from(document.querySelectorAll('div')).find(div => div.style.cssText.includes(arguments[0]));",
                        request_body_style
                    )
                    request_body_text = request_body_div.text
                    print(request_body_text)
                except:
                    request_body_text = ''
                with open('compiler/dashboard.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{dashboard_text}##{top_banner_text}##{description_text}##{request_body_text}\n')
                    file.close()
            else:
                print('Element with specified style not found')
        except Exception as e:
            print(f'Error: {e}')

    driver.quit()

def find_dropdowns():
    chrome_options = Options()
    #chrome_options.add_argument('--headless')  # Run in headless mode (no GUI)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(base_url)
    time.sleep(5)
    
    # Get the page source and parse it
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Find the div with class 'px-theme-light' and print the text of all divs inside it
    px_theme_light_div = soup.find('div', class_='px-theme-light')
    if px_theme_light_div:
        for div in px_theme_light_div.find_all('div'):
            text = div.get_text(strip=True)
            div_class = div.get('class', [''])[0]  # Get the first class or an empty string if no class
            print(f"Text: {text}, Class: {div_class}")
            with open('compiler/dropdowns.txt', 'a', encoding='utf-8') as file:
                file.write(f"Text: {text}\nClass: {div_class}\n\n")
                file.close()

    driver.quit()

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
            file.write(soup.prettify())
            file.write('\n\n\n')
        file.close()


if __name__ == "__main__":
    #check_request()
    select_dropdowns()