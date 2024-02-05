# 
# Scrape hospitals job listings sites for New Grad RN positions.
# Be able to scrape multiple sites at once and filter through listings
# for New Grad positions. Return number of jobs, job title, hospital name and link 
# as *FILL TBD*
#

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

#Open site
driver = webdriver.Firefox()
url = "https://careers.hcahealthcare.com/search/jobs/in?cfm10%5B%5D=03360&cfm10%5B%5D=location&cfm10%5B%5D=has-video&cfm10%5B%5D=good-samaritan-hospital&cfm10%5B%5D=no-heading&page=1# "
driver.get(url)

# Xpath to container that encapsulates all the job listings
contianer_xpath = '//*[@id="job-list-inner"]/div[2]/div[5]/div'
containers = driver.find_elements(By.XPATH, contianer_xpath)


while True:
    try:
        # Access first element of the list  
        inner_elements = containers[0].find_elements(By.XPATH, "./*")

        # Interate through the container to get number of listings
        for inner_index, inner_element in enumerate(inner_elements):
            # Xpath to title and link
            xpath = f'//*[@id="job-list-inner"]/div[2]/div[5]/div/div[{inner_index + 1}]/div/div/div[2]/h2/a'
            hospital_xpath = f'//*[@id="job-list-inner"]/div[2]/div[5]/div/div[{inner_index + 1}]/div/div/div[2]/div[1]'
            job_links = driver.find_elements(By.XPATH, xpath)
            hospital_links = driver.find_element(By.XPATH, hospital_xpath)
            
        
            print(f"Job {inner_index + 1}: " + job_links[0].text + "\nLink: " + job_links[0].get_attribute('href') 
                + "\nHospital: " + hospital_links.text + "\n")
   
        try: 
            next_xpath = '//*[@id="job-list-inner"]/div[2]/div[5]/div/div[26]/div[1]/div/nav/ul/li[4]/a'
            next_button = driver.find_element(By.XPATH, next_xpath)
            print("HEWWOOOOOOO \n")
            
            if next_button: 
                next_button.click()
                
            else: 
                break 
            
        except NoSuchElementException:
            break
        
            
    except NoSuchElementException:
        print("No inner element found")