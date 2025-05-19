import time
import re
import pandas as pd
from selenium import webdriver      # Core driver of selenium
from selenium.webdriver.common.by import By     # Helps locate elements by ID, class,..
from selenium.common.exceptions import TimeoutException, NoSuchElementException     # Look for element on page
from selenium.webdriver.support.ui import WebDriverWait     # Wait on Webpage for elements to be present
from selenium.webdriver.support import expected_conditions as EC      # Wait until specific condition is true
from selenium.webdriver.firefox.options import Options      # Activate options on Firefox
from selenium.webdriver.common.action_chains import ActionChains    # Chain multiple actions on a page

def spirit_listing(url):
    # Start the driver for Firefox
    driver = webdriver.Firefox()
    driver.get(url)
    
    # Job listing l
    job_listings = []

    # Attempting to clear the cookies permission pop-up if present
    try:
        # Waiting 20sec until element is clickable in attempt to clear cookies pop-up by rejecting it
        reject_button_xpath = '/html/body/div[4]/button'
        reject_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, reject_button_xpath))
        )
        reject_button.click()
    
    # If the pop-up appears and if we failed to close the pop-up
    except NoSuchElementException:
        print("No such button for cookies")
        
    except Exception as e:
        print(f"Failed to close cookie banner: {e}")
    
    # Same thing but for a different pop-up, *** Add reason ***
    try:
        reject_button_xpath = '//*[@id="igdpr-button"]'
        reject_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, reject_button_xpath))
        )
        reject_button.click()
    
    except NoSuchElementException:
        print("No such button for banner")
        
    except Exception as e:
        print(f"Failed to accept banner: {e}")
        
    time.sleep(1)
    
    #Clear pre-existing filter
    for i in range(4):
        try:                            
            close_arizona_xpath = '//*[@id="applied-filters"]/ul/li[2]/button'
            arizona_button = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.XPATH, close_arizona_xpath))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", arizona_button)
            action = ActionChains(driver)
            
            if i == 0:
                action.click(arizona_button)
                action.click(arizona_button)
                action.perform()
                time.sleep(1)
                
            else:
                action.click(arizona_button).perform()
                time.sleep(1)
                
        except Exception as e:
            print(f"Error closing pre-existing filters: {e}")
    
    city_list_xpath = '//*[@id="city-toggle"]'
    city_list_button = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.XPATH, city_list_xpath))
    )
    city_list_button.click()
    time.sleep(2)
    
    #Apply new filter 
    filter_numbers = [31, 34, 25, 4]
    for i in filter_numbers:
        new_filter_xpath = f'//*[@id="city-filter-{i}"]'
        
        new_filter_button = WebDriverWait(driver, 30).until(
                                EC.element_to_be_clickable((By.XPATH, new_filter_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", new_filter_button)
        new_filter_button.click()
        time.sleep(1)
    
    try:                      
        total_listing_xpath = '//*[@id="search-results"]/h2'
        total_links = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, total_listing_xpath)))
        total_text = total_links.text
        numbers = re.findall(r'\d+', total_text)
        number = int(numbers[0])
        total = number
        
    except Exception as e:
        print(f"Error at total: ", e)
    
    # Get listings 
    while total > len(job_listings):
        contianer_xpath = '//*[@id="search-results-list"]/ul'
        containers = driver.find_element(By.XPATH, contianer_xpath)
        inner_elements = containers.find_elements(By.XPATH, "./*")

        for i in range(len(inner_elements)):
            title_xpath = f'//*[@id="search-results-list"]/ul/li[{i + 1}]/a[1]/div/h2'
            link_xpath = f'//*[@id="search-results-list"]/ul/li[{i + 1}]/a[1]'
            location_xpath = f'//*[@id="search-results-list"]/ul/li[{i + 1}]/a[1]/div/span[3]'
            hospital_xpath = f'//*[@id="search-results-list"]/ul/li[{i + 1}]/a[1]/div/span[2]'
            
            title_links = driver.find_element(By.XPATH, title_xpath)
            link_links = driver.find_element(By.XPATH, link_xpath)
            location_links = driver.find_element(By.XPATH, location_xpath)
            hospital_links = driver.find_element(By.XPATH, hospital_xpath)
            
            job_details = { 
                            "Job": title_links.text,
                            "Link": link_links.get_attribute('href'),
                            "Location": location_links.text,
                            "Hospital": hospital_links.text
                            }
                
            job_listings.append(job_details)
        
        try:
            next_xpath = ' //*[@id="pagination-bottom"]/div[2]/a[2]'
            next_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, next_xpath)))
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", next_button)
            time.sleep(1)
            next_button.click()
            time.sleep(1)
            
        except NoSuchElementException:
            break
        
        except Exception as e:
            print("Error going to next page: ", e)
            
    driver.quit()
    df = pd.DataFrame(job_listings)
    print(len(df))
    return df
    
def spirit_runner():
    url = "https://www.commonspirit.careers/search-jobs?orgIds=35300&acm=ALL&alrpm=6252001-5551752,6252001-5417618,6252001-5509151,6252001-5332921,6252001-4896861&ascf=[%7B%22key%22:%22industry%22,%22value%22:%22Dignity+Health%22%7D,%7B%22key%22:%22industry%22,%22value%22:%22CommonSpirit%22%7D]"
    
    try: 
        spirit_jobs = spirit_listing(url)
        
    except Exception as e:
        print(f"Fail to get listing from CommonSpirit: {e}")
    
    return spirit_jobs

if __name__ == "__main__":
    spirit_runner()