import threading
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from runners.hcahealthcare import hcahealthcare_runner
from runners.governmentjobs import governmentjobs_runner  
from runners.oraclecloud import oraclecloud_runner
from runners.workday import workday_runner
from runners.whhs import whhs_runner
from runners.commonspirit import spirit_runner


def run_site(scraper_fn, label):
   try: 
      df = scraper_fn
      return (label, filter_df(df))
   except Exception as e:
      print(f"Error in {label: {e}}")
      return(label, pd.DataFrame())

def filter_df(df):
    try:
        data = pd.DataFrame(df)
        filtered_df = data[data["Job"].str.contains(r"New Graduate Nurse Residency|Clinical Nurse I\b|Clinical Nurse 1|New Grad RN Residency|"
                                                    r"New Grad Nurse Residency Program|Nurse 1|Staff Nurse I\b|Registered Nurse I\b|Staff Nurse 1|"
                                                    r"New Grad|New Grad Registered Nurse|RN New Grad Residency Program|Nurse Residency Program|"
                                                    r"New Grad RN|RN 1|RN I\b|RN\b", case=False, na=False)]
        return filtered_df
     
    except Exception as e:
        print(f"Error occurred while filtering: {e}")
        return df 
def scraper_pipeline():
    scrapers = [
        (hcahealthcare_runner, 'HCA'),
        (governmentjobs_runner, 'GOV'),
        (oraclecloud_runner, 'OC'),
        (workday_runner, 'WD'),
        (whhs_runner, 'WHHS'),
        (spirit_runner, 'CS')
    ]

    RN_listings = {} 

    with ThreadPoolExecutor(max_workers=6) as executor:
        results = executor.map(lambda s: run_site(*s), scrapers)

if __name__ == "__main__":
    scraper_pipeline()

# combined_df = pd.concat([
#                            RN_listings.get('HCA', pd.DataFrame()), 
#                            RN_listings.get('GOV', pd.DataFrame()),  
#                            RN_listings.get('OC', pd.DataFrame()),
#                            RN_listings.get('WD', pd.DataFrame()),
#                            RN_listings.get('WHHS', pd.DataFrame()),
#                            RN_listings.get('CS', pd.DataFrame())
#                         ], ignore_index=True)
# combined_df.to_csv('../New_Grad_Listings.csv', index = False)