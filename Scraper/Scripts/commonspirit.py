import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains


def spirit_listing(url):
    driver = webdriver.Firefox()
    driver.get(url)

    try:
        reject_button_xpath = '/html/body/div[4]/button'
        reject_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, reject_button_xpath))
        )
        reject_button.click()
    
    except NoSuchElementException:
        print("No such button for cookies")
        
    except Exception as e:
        print(f"Failed to close cookie banner: {e}")
    
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
    
    #Clear  pre-existing filter
    for i in range(4):
        try:                            
            close_arizona_xpath = '//*[@id="applied-filters"]/ul/li[2]/button'
            arizona_button = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.XPATH, close_arizona_xpath))
                )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", arizona_button)
            action = ActionChains(driver)
            
            if i == 1:
                action.click(arizona_button)
                action.click(arizona_button)
                action.perform()
                time.sleep(1)
                
            else:
                action.click(arizona_button).perform()
                time.sleep(1)
                
        except Exception as e:
            print(f"Error closing Arizona: {e}")
        
def spirit_runner():
    url = "https://www.commonspirit.careers/search-jobs?orgIds=35300&acm=ALL&alrpm=6252001-5551752,6252001-5417618,6252001-5509151,6252001-5332921,6252001-4896861&ascf=[%7B%22key%22:%22industry%22,%22value%22:%22Dignity+Health%22%7D,%7B%22key%22:%22industry%22,%22value%22:%22CommonSpirit%22%7D]"
    
    try: 
        spirit_listing(url)
        
    except Exception as e:
        print(f"Fail to get listing from CommonSpirit: {e}")


if __name__ == "__main__":
    spirit_runner()