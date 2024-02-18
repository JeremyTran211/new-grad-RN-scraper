import threading
import pandas as pd
from Scripts.hcahealthcare import hcahealthcare_runner
from Scripts.governmentjobs import governmentjobs_runner  

# Filter results of scraping
def filter_df(df):
    try:
        data = pd.DataFrame(df)
        filtered_df = data[data["Job"].str.contains(r"New Graduate Nurse Residency|Clinical Nurse I\b|Clinical Nurse 1|New Grad RN Residency|"
                                                    r"New Grad Nurse Residency Program|Nurse 1|Staff Nurse I\b|Registered Nurse I\b|Staff Nurse 1|"
                                                    r"New Grad|New Grad Registered Nurse|RN New Grad Residency Program|Nurse Residency Program|"
                                                    r"New Grad RN|RN 1|RN I\b|Manager|Traffic", case=False, na=False)]
        return filtered_df
    except Exception as e:
        print(f"Error occurred while filtering: {e}")
        return df  # Return the original DataFrame in case of an error

# hcahealthcare 
def run_hca(listings_dict):
   try:
      # Get dataframe from hca
      hca = hcahealthcare_runner()
      # Filter before inserting into combined dictionary
      filtered_hca = filter_df(hca)
      # Add to combined dictionary with key 'HCA'
      listings_dict['HCA'] = filtered_hca
   except Exception as e:
      print(f"An error occurred: {e}")
   return filtered_hca

# governmentjobs
def run_gov(listings_dict):
   try:
      gov = governmentjobs_runner()
      filtered_gov = filter_df(gov)
      listings_dict['GOV'] = filtered_gov
   except Exception as e:
      print(f"An error occurred: {e}")

#------------------- PROGRAM START---------------------#

# To handle all the df from threads
RN_listings = {}

thread_hca = threading.Thread(target=run_hca, args=(RN_listings,))
thread_gov = threading.Thread(target=run_gov, args=(RN_listings,))

thread_hca.start()
thread_gov.start()

thread_hca.join()
thread_gov.join()

combined_df = pd.concat([RN_listings.get('HCA', pd.DataFrame()), RN_listings.get('GOV', pd.DataFrame())], ignore_index=True)
combined_df.to_csv('New_Grad_Listings.csv',index = False)