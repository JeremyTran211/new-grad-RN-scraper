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
     #driver = webdriver.Firefox()
    
    # Open site wth headless option
    fox_options = Options()
    fox_options.add_argument("-headless")
    driver = webdriver.Firefox(options=fox_options)
    driver.get(url)
    WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
   
    job_listings = []
    current_page_listings = 0
    
    container_xpath = '//*[@id="mainContent"]/div/div[2]/section/ul'
    container = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH,container_xpath)))
    
    while True: 
        try:                  
            container = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH,container_xpath)))  
            inner_elements = container.find_elements(By.XPATH, "./*")
            current_page_listings = len(inner_elements)
            
            try:
                for i in range(len(inner_elements)):
                    # Xpath to job title, link and hospital 
                    job_xpath = f'//*[@id="mainContent"]/div/div[2]/section/ul/li[{i + 1}]/div[1]/div/div/h3/a'
                    location_xpath = f'//*[@id="mainContent"]/div/div[2]/section/ul/li[{i + 1}]/div[2]/div/div/dl/dd'
                    job_links =  WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, job_xpath)))
                    location_links =  WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, location_xpath)))
                    
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
                print(f"Error getting listing: {e}")
                
           
            
            if current_page_listings < 20:
                #print("End of lisitngs")
                break
            
            else: 
                if len(job_listings) <= 20:
                    next_xpath = '//*[@id="mainContent"]/div/div[2]/section/div[2]/nav/div/button'
                
                else: 
                    next_xpath = ' //*[@id="mainContent"]/div/div[2]/section/div[2]/nav/div/button[2]'
               
                try:
                    next_button = driver.find_element(By.XPATH, next_xpath)
                    next_button.click()
                    time.sleep(2)
                    
                except NoSuchElementException:
                   # print("End listing")
                    break
            
        except Exception as e: 
            print(f"Error retreiving listing: {e}") 
            
    driver.quit()      
    df = pd.DataFrame(job_listings)
    return df
    
def workday_runner():
    url = "https://ech.wd5.myworkdayjobs.com/ech"
    try:
        workday_listings = workday_listing(url)
        
    except Exception as e:
        print(f"Could not get listing: {e}")

    return workday_listings