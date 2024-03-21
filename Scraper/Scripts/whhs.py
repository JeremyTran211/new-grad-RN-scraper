import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def whhs_listings(url):
    fox_options = Options()
    fox_options.add_argument("-headless")
    driver = webdriver.Firefox(options=fox_options)
    driver.get(url)
    WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
   
    iframe_xpath = '//*[@id="jv_careersite_iframe_id"]'
    driver.switch_to.frame(driver.find_element(By.XPATH,iframe_xpath))
    
    job_listings = []
    
    try:              
        container_xpath = '/html/body/div/div/div/article/div/table[11]/tbody'
        container = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, container_xpath)))
        inner_elements = container.find_elements(By.XPATH, "./*")

        for i in range(len(inner_elements)):
            job_xpath = f'/html/body/div/div/div/article/div/table[11]/tbody/tr[{i + 1}]/td[1]/a'
            location_xpath = f'/html/body/div/div/div/article/div/table[11]/tbody/tr[{i + 1}]/td[2]'
            job_links = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, job_xpath)))
            location_links = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, location_xpath)))
          
            job_details = { 
                          "Job": job_links.text, 
                          "Link": job_links.get_attribute('href'),
                          "Location": location_links.text,
                          "Hospital": 'Washington Hospital'
                        }
            
            job_listings.append(job_details)
            
    except Exception as e:
        print(f"Error getting the listings from container: {e}")

    df = pd.DataFrame(job_listings)
    return df

def whhs_runner():
    url = "https://www.whhs.com/careers/current-career-opportunities/"
    
    try:
       whhs_jobs = whhs_listings(url)
       
    except Exception as e:
        print(f"Error getting listing: {e}")
    
    return whhs_jobs
