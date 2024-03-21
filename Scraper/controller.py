import threading
import pandas as pd
from Scripts.hcahealthcare import hcahealthcare_runner
from Scripts.governmentjobs import governmentjobs_runner  
from Scripts.oraclecloud import oraclecloud_runner
from Scripts.workday import workday_runner
from Scripts.whhs import whhs_runner

def filter_df(df):
    try:
        data = pd.DataFrame(df)
        filtered_df = data[data["Job"].str.contains(r"New Graduate Nurse Residency|Clinical Nurse I\b|Clinical Nurse 1|New Grad RN Residency|"
                                                    r"New Grad Nurse Residency Program|Nurse 1|Staff Nurse I\b|Registered Nurse I\b|Staff Nurse 1|"
                                                    r"New Grad|New Grad Registered Nurse|RN New Grad Residency Program|Nurse Residency Program|"
                                                    r"New Grad RN|RN 1|RN I\b|Manager|OR Staff RN II - Operating Room - Full Time 8 hr - Nights Variable\b", case=False, na=False)]
        return filtered_df
    except Exception as e:
        print(f"Error occurred while filtering: {e}")
        return df  # Return the original DataFrame in case of an error

def run_hca(listings_dict):
   try:
      # Get dataframe from hca
      hca = hcahealthcare_runner()
      # Filter before inserting into combined dictionary
      filtered_hca = filter_df(hca)
      # Add to combined dictionary with key 'HCA'
      listings_dict['HCA'] = filtered_hca
      
   except Exception as e:
      print(f"An error occurred at HCA: {e}")
      
   return filtered_hca

def run_gov(listings_dict):
   try:
      gov = governmentjobs_runner()
      filtered_gov = filter_df(gov)
      listings_dict['GOV'] = filtered_gov
      
   except Exception as e:
      print(f"An error occurred at GovernmentJobs: {e}")
   
def run_oracle(listings_dict):
   try:
      oc = oraclecloud_runner()
      filtered_oc = filter_df(oc)
      listings_dict['OC'] = filtered_oc
   
   except Exception as e:
      print(f"An error occured at OracleCloud: {e}")

def run_workday(listings_dict):
   try:
      wd = workday_runner()
      filtered_wd = filter_df(wd)
      listings_dict['WD']  = filtered_wd
   
   except Exception as e:
      print(f"An error occured at Workday: {e}")

def run_whhs(listings_dict):
   try:
      whhs = whhs_runner()
      filtered_whhs = filter_df(whhs)
      listings_dict["WHHS"] = filtered_whhs
   
   except Exception as e:
      print(f"An error occued at WHHS: {e}")
      
#------------------- PROGRAM START ---------------------#

# To handle all the df from threads
RN_listings = {}

thread_hca = threading.Thread(target=run_hca, args=(RN_listings,))
thread_gov = threading.Thread(target=run_gov, args=(RN_listings,))
thread_oc = threading.Thread(target=run_oracle, args=(RN_listings,))
thread_wd = threading.Thread(target=run_workday, args=(RN_listings,))
thread_whhs = threading.Thread(target=run_whhs, args=(RN_listings,))

thread_hca.start()
thread_gov.start()
thread_oc.start()
thread_wd.start()
thread_whhs.start()

thread_hca.join()
thread_gov.join()
thread_oc.join()
thread_wd.join()
thread_whhs.join()

combined_df = pd.concat([
                           RN_listings.get('HCA', pd.DataFrame()), 
                           RN_listings.get('GOV', pd.DataFrame()),  
                           RN_listings.get('OC', pd.DataFrame()),
                           RN_listings.get('WD', pd.DataFrame()),
                           RN_listings.get('WHHS', pd.DataFrame())
                        ], ignore_index=True)
combined_df.to_csv('../New_Grad_Listings.csv', index = False)