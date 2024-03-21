import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def governmentjobs_listing(url):
    #Open site with interface
    #driver = webdriver.Firefox()
    
    #Open site wth headless option
    fox_options = Options()
    fox_options.add_argument("-headless")
    driver = webdriver.Firefox(options=fox_options)
    driver.get(url)
    
    job_listings = []
    
    try: 
        while True:
            container_xpath = '//*[@id="job-list-container"]/ul'
            containers = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, container_xpath)))

            if containers:
                inner_elements = containers[0].find_elements(By.XPATH, "./*")
                
                for inner_index in range(len(inner_elements)):
                    # Xpath to job title, link and hospital 
                    job_xpath = f'//*[@id="job-list-container"]/ul/li[{inner_index + 1}]/h3/a'
                    hospital_xpath = f'//*[@id="job-list-container"]/ul/li[{inner_index + 1}]/ul/li[1]'
                    job_links = driver.find_element(By.XPATH, job_xpath)
                    hospital_links = driver.find_element(By.XPATH, hospital_xpath)
                    
                    # Set up key-value dictionary
                    job_details ={
                                  "Job": job_links.text, 
                                  "Link": job_links.get_attribute('href'),
                                  "Location": hospital_links.text
                    }
                    # Adds job details into a single list
                    job_listings.append(job_details)
            else:
                print("Container not found")
                    
            try:
                #Click next button 
                next_xpath = '//*[@id="job-list-container"]/div[3]/div[1]/div[1]/ul/li[9]/a'
                next_button = driver.find_element(By.XPATH, next_xpath)
                next_href = next_button.get_attribute('href')
                
                if next_href:
                    next_button.click()

                    time.sleep(3) 
                    
                else:           
                    break
        
            except Exception as e: 
                print("Error going to next page: ", e)

    except Exception as e:
        print(f"Error while scraping: {e}")
        
    df = pd.DataFrame(job_listings)
    driver.quit()
    
    return df
    
def governmentjobs_runner():
    try:
        url = "https://www.governmentjobs.com/careers/santaclara"
        gov_jobs = governmentjobs_listing(url)

    except Exception as e:
        print(f"Error at insert: ", e)
    
    return gov_jobs