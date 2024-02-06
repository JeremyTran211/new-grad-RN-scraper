from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


#Open site
driver = webdriver.Firefox()
url = "https://careers.hcahealthcare.com/search/jobs/in?cfm10%5B%5D=03360&cfm10%5B%5D=location&cfm10%5B%5D=has-video&cfm10%5B%5D=good-samaritan-hospital&cfm10%5B%5D=no-heading&page=1# "
driver.get(url)

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

    # Access the container for listings
    inner_elements = containers[0].find_elements(By.XPATH, "./*")

    for inner_index in range(len(inner_elements) - 1):
        # Xpath to title and link
        job_xpath = f'//*[@id="job-list-inner"]/div[2]/div[5]/div/div[{inner_index + 1}]/div/div/div[2]/h2/a'
        hospital_xpath = f'//*[@id="job-list-inner"]/div[2]/div[5]/div/div[{inner_index + 1}]/div/div/div[2]/div[1]'
        job_links = driver.find_elements(By.XPATH, job_xpath)
        hospital_links = driver.find_element(By.XPATH, hospital_xpath)
        print(f"Job {inner_index + 1}: " + job_links[0].text + "\nLink: " + job_links[0].get_attribute('href') 
            + "\nHospital: " + hospital_links.text + "\n")
    
    time.sleep(3) 
    
    try:
        next_xpath = '//*[@id="job-list-inner"]/div[2]/div[5]/div/div[26]/div[1]/div/nav/ul/li[4]/a/i'
        next_button = driver.find_element(By.XPATH, next_xpath)
        next_button.click()
        print("Clicked") 
        
    except NoSuchElementException:
        print("Reached the end of listings")
        break