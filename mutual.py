from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from pprint import pprint
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json

def update_json_file(filename, target_url, mutual_connections):
    try:
        with open(filename, 'r') as infile:
            data = json.load(infile)
    except FileNotFoundError:
        data = {}

    data[target_url] = mutual_connections

    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def get_mutual_connections(wait, driver, target):


    # Navigate to the desired LinkedIn profile URL
    driver.get(target)
    mutual_connections = {}

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.link-without-hover-visited")))
    # time.sleep(3)

    anchor_element = driver.find_element(By.CSS_SELECTOR, "a.link-without-hover-visited")
    # Get the 'href' attribute of the anchor element
    link = anchor_element.get_attribute("href")

    line = anchor_element.find_element(By.CSS_SELECTOR, "span.t-normal")
    total_connections = 0
    if ',' in line.text:
        connections_string = line.text.split(',')[2]
        numbers = re.findall(r'\d+', connections_string)
        total_connections = int(numbers[0]) + 2
    elif 'and' in line.text:
        total_connections = 2
    else:
        total_connections = 1

    print(total_connections)

    pages = total_connections // 10
    if total_connections % 10 > 0:
        pages += 1


    for i in range(pages):
        page = link + f"&page={i+1}"
        driver.get(page)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'li.reusable-search__result-container')))
        # time.sleep(4)
        list_items = driver.find_elements(By.CSS_SELECTOR, 'li.reusable-search__result-container')

        for item in list_items:
            relevant_element = item.find_element(By.XPATH, ".//span[@aria-hidden='true']")
            relevant_anchor = item.find_element(By.CSS_SELECTOR, "a.app-aware-link ")
            relevant_link = relevant_anchor.get_attribute("href")
            mutual_connections[relevant_element.text] = relevant_link.split('?')[0]
            update_json_file('connections_data.json', target, mutual_connections)


    pprint(mutual_connections)
    




    return mutual_connections