import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options



def hcahealthcare_listing(url):
    
    #Open site wth headless option
    fox_options = Options()
    fox_options.add_argument("-headless")
    driver = webdriver.Firefox(options=fox_options)
    driver.get(url)
    
    job_listings = []

    try:
        # Wait and click the Reject Cookies button
        reject_button_xpath = '//*[@id="search-jobs-in"]/div[2]/div[2]/a[2]'
        reject_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, reject_button_xpath))
        )
        reject_button.click()
        print("Rejected cookies")
        
    except TimeoutException:
        print("No cookie banner found or button not clickable.")
    except NoSuchElementException:
        print("Cookie button not found.")
    except Exception as e:
        print("Error interacting with cookie banner: ", e)
        
    while True:
        # Xpath to container that encloses all the job listings to get number of listings
        contianer_xpath = '//*[@id="job-list-inner"]/div[2]/div[5]/div'
        containers = driver.find_elements(By.XPATH, contianer_xpath)

        # Access the container to get # of listings
        inner_elements = containers[0].find_elements(By.XPATH, "./*")

        for inner_index in range(len(inner_elements) - 1):
            # Xpath to job title, link and hospital 
            job_xpath = f'//*[@id="job-list-inner"]/div[2]/div[5]/div/div[{inner_index + 1}]/div/div/div[2]/h2/a'
            hospital_xpath = f'//*[@id="job-list-inner"]/div[2]/div[5]/div/div[{inner_index + 1}]/div/div/div[2]/div[1]'
            job_links = driver.find_element(By.XPATH, job_xpath)
            hospital_links = driver.find_element(By.XPATH, hospital_xpath)
            
            # Set up key-value dictionary
            job_details = { 
                          "Job": job_links.text, 
                          "Link": job_links.get_attribute('href'),
                          "Hospital": hospital_links.text
                        }
            
            # Adds job details into a single list
            job_listings.append(job_details)
        
        time.sleep(3) 
        
        try:
            #Click next button 
            next_xpath = '//*[@id="job-list-inner"]/div[2]/div[5]/div/div[26]/div[1]/div/nav/ul/li[4]/a/i'
            next_button = driver.find_element(By.XPATH, next_xpath)
            next_button.click()
            print("Clicked") 
            
        except NoSuchElementException:
            print("Reached the end of listings")
            break
        
        except Exception as e:
            print("Error going to next page: ", e)


    df = pd.DataFrame(job_listings)
    driver.quit()
    
    return df 

def hcahealthcare_runner():
    url1 = "https://careers.hcahealthcare.com/search/jobs/?cfm10[]=08385&cfm10[]=location&cfm10[]=has-video&cfm10[]=no-heading&cfm10[]=regional-medical-center-of-san-jose"
    url2 = "https://careers.hcahealthcare.com/search/jobs/in?cfm10%5B%5D=03360&cfm10%5B%5D=location&cfm10%5B%5D=has-video&cfm10%5B%5D=good-samaritan-hospital&cfm10%5B%5D=no-heading&page=1#"
   
    try: 
        data1 = hcahealthcare_listing(url1)
    
    except Exception as e:
        print(f"An error as occured in HcaHealthcare1: {e}")
        
    try: 
        data2 = hcahealthcare_listing(url2)
    
    except Exception as e:
        print(f"An error as occured in HcaHealthcare2: {e}")
    
    hca_combined = pd.concat([data1, data2], ignore_index=True) if data1 is not None and data2 is not None else None

    return hca_combined