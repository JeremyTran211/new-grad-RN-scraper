import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def workday_listing(url):
    # Open site with interface
    driver = webdriver.Firefox()
    
    # Open site wth headless option
    # fox_options = Options()
    # fox_options.add_argument("-headless")
    # driver = webdriver.Firefox(options=fox_options)
    driver.get(url)
    WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
   
    job_listings = []
    
    try:                    
        container_xpath = '//*[@id="mainContent"]/div/div[2]/section/ul'
        container = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH,container_xpath)))
        inner_elements = container.find_elements(By.XPATH, "./*")
        
        for i in range(len(inner_elements) - 1):
        # Xpath to job title, link and hospital 
            job_xpath = f'//*[@id="mainContent"]/div/div[2]/section/ul/li[{i + 1}]/div[1]/div/div/h3/a'
            location_xpath = f'//*[@id="mainContent"]/div/div[2]/section/ul/li[{i + 1}]/div[2]/div/div/dl/dd'
            job_links = driver.find_element(By.XPATH, job_xpath)
            location_links = driver.find_element(By.XPATH, location_xpath)
            
            # Set up key-value dictionary
            job_details = { 
                            "Job": job_links.text, 
                            "Link": job_links.get_attribute('href'),
                            "Location": location_links.text,
                            "Hospital": "El Camino Real"
                        }
            
            # Adds job details into a single list
            job_listings.append(job_details)
    
    except Exception as e: 
        print(f"Error retreiving listing: {e}")
    
    print(job_listings)
    
    
def workday_runner():
    url = "https://ech.wd5.myworkdayjobs.com/ech"
    try:
        workday_listing(url)
        
    except Exception as e:
        print(f"Could not get listing: {e}")

if __name__ == '__main__':
    workday_runner()