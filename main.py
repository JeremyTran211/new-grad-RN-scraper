import threading
from Scripts.hcahealthcare import hcahealthcare_runner
from Scripts.governmentjobs import governmentjobs_runner

#hcahealthcare 
def run_hca():
   try:
      hca = hcahealthcare_runner()
      print(hca)
      
   except Exception as e:
      print(f"An error occurred: {e}")

#governmentjobs
def run_gov():
   try:
      gov = governmentjobs_runner()
      print(gov)
      
   except Exception as e:
      print(f"An error occurred: {e}")

thread_hca = threading.Thread(target=run_hca)
thread_gov = threading.Thread(target=run_gov)

thread_hca.start()
thread_gov.start()

thread_hca.join()
thread_gov.join()