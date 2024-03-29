# New Grad RN Web Scraper

## Project Overview
The New Grad RN Web Scraper is a Python-based tool designed to automate the job search process for new graduate registered nurses by aggregating and filtering job listings from multiple healthcare websites. It simplifies finding New Grad RN positions, providing a consolidated view of available opportunities.

## Features
- Scrapes job listings from 7 distinct healthcare and hospital websites all around the Bay Area.
- Filters and consolidates listings into a unified csv file for easy access. (Plans to move to database along with deployment)

## Sources
1. [Washington Hospital, Fremont](https://www.whhs.com/careers/current-career-opportunities/)
2. [Regional Medical Center, San Jose](https://careers.hcahealthcare.com/search/jobs/?cfm10[]=08385&cfm10[]=location&cfm10[]=has-video&cfm10[]=no-heading&cfm10[]=regional-medical-center-of-san-jose)
3. [Santa Clara County Jobs, RN only](https://www.governmentjobs.com/careers/santaclara)
4. [Good Samaritan, San Jose](https://careers.hcahealthcare.com/search/jobs/in?cfm10%5B%5D=03360&cfm10%5B%5D=location&cfm10%5B%5D=has-video&cfm10%5B%5D=good-samaritan-hospital&cfm10%5B%5D=no-heading&page=1#)
5. [El Camino Health, Moutain View](https://ech.wd5.myworkdayjobs.com/ech)
6. [Adventist Health, St Helena](https://ecvz.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions?lastSelectedFacet=ORGANIZATIONS&location=Napa%2C+CA%2C+United+States&locationId=300000002565489&locationLevel=city&mode=job-location&radius=25&radiusUnit=MI&selectedOrganizationsFacet=300000009236588)
7. [Dignity Health Sequoia Hospital, Belmont, Redwood City, San Francisco, Santa Cruz](https://www.commonspirit.careers/search-jobs?orgIds=35300&acm=ALL&alrpm=6252001-5551752,6252001-5417618,6252001-5509151,6252001-5332921,6252001-4896861&ascf=[%7B%22key%22:%22industry%22,%22value%22:%22Dignity+Health%22%7D,%7B%22key%22:%22industry%22,%22value%22:%22CommonSpirit%22%7D])

## Installation
To set up the scraper on your local machine, follow these steps:

```bash
pip install -r requirements.txt
python3 controller.py
