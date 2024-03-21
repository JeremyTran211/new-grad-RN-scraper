# Oraclecloud
# This site requires regular maintainence on all XPATH. 
#
#
# 

import time
import re
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def oraclecloud_listing(url):
    i = 0
    # Open site with interface
    # driver = webdriver.Firefox()
    
    # Open site wth headless option
    fox_options = Options()
    fox_options.add_argument("-headless")
    driver = webdriver.Firefox(options=fox_options)
    driver.get(url)
    WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')

    job_listings = []
    
    
    # Get total listing
    try:                      
        total_listing_xpath = '/html/body/div[3]/div[1]/div/div[1]/main/div/div/div/div/div/div[2]/div/div/div/div/search-filters-panel-horizontal/div/div/search-filters-horizontal/div[1]/ul/li[1]/div'
        total_links = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, total_listing_xpath)))
        total_text = total_links.text
        numbers = re.findall(r'\d+', total_text)
        number = int(numbers[0])
        total = number
        
    except Exception as e:
        print(f"Error at total: ", e)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the new content to load
        time.sleep(random.uniform(3, 6))

        # Calculate the new scroll height and compare it with the last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  
        last_height = new_height
        
    while total != len(job_listings):
        job_details = {}
        if i == 2:
            i += 1
            continue
        
        try:                    
            job_title_xpath = f'/html/body/div[3]/div[1]/div/div[1]/main/div/div/div/div/div/div[3]/div/div/div/div/div/div/ul/li[{i + 1}]/div/a/div[1]/search-result-item-header/div/span'
            job_title_box = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, job_title_xpath)))
            job_details["Job"] = job_title_box.text
        except TimeoutException:
            print(f"Job title not found for item {i+1}")

        try:                  
            job_link_xpath = f'/html/body/div[3]/div[1]/div/div[1]/main/div/div/div/div/div/div[3]/div/div/div/div/div/div/ul/li[{i + 1}]/div/a'
            job_link_box = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, job_link_xpath)))
            job_details["Link"] = job_link_box.get_attribute('href')
        except TimeoutException:
            print(f"Job link not found for item {i+1}")

        try:                         
            location_xpath = f'/html/body/div[3]/div[1]/div/div[1]/main/div/div/div/div/div/div[3]/div/div/div/div/div/div/ul/li[{i + 1}]/div/a/div[1]/search-result-item-header/div/div/span[1]/span'
            location_box = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, location_xpath)))
            job_details["Location"] = location_box.text

        except TimeoutException:
            print(f"Location not found for item {i+1}")
                
        if job_details:
            job_listings.append(job_details)
            
        i += 1
    
    return job_listings
 
def oraclecloud_runner():
    try:
        url = (
                "https://ecvz.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions?"
                "lastSelectedFacet=ORGANIZATIONS&location=Napa%2C+CA%2C+United+States&locationId=300000002565489&"
                "locationLevel=city&mode=job-location&radius=25&radiusUnit=MI&selectedOrganizationsFacet=300000009236588"
        )

        oraclecloud_jobs = oraclecloud_listing(url)

    except Exception as e:
        print(f"Error at start: ", e)
    
    return oraclecloud_jobs