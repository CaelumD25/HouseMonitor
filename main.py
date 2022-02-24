from time import sleep
from replit_keep_alive import keep_alive
from datetime import datetime
import Aggregate_Data as AD
import Email_Rentals as ER

craigslist_url = "https://victoria.craigslist.org/postings/victoria-bc/apartments-housing-for-rent?availabilityMode=0&lat=48.4620386050385&lon=-123.31047155403003&max_bathrooms=1&max_bedrooms=2&min_bathrooms=1&min_bedrooms=0&search_distance=2&sort=date"

kijiji_url = "https://www.kijiji.ca/b-for-rent/victoria-bc/c30349001l1700173?ll=48.463407%2C-123.311694&address=University+of+Victoria%2C+Victoria%2C+British+Columbia&radius=4.0"

used_vic_url = "https://www.usedvictoria.com/real-estate-rentals?lat=48.464726505426725&lon=-123.31363677978517&ca=%7B%227%22%3A%5B%220%22,%222%22%5D,%228%22%3A%5B%221%22,%221%22%5D%7D&radius=5000&xflags=wanted"

recipients = ["caelumdudek25@gmail.com"]
# recipients = ["caelumdudek25@gmail.com","la.can.hockey@gmail.com"]

def main():

  keep_alive()

  email = ER.Email_Rentals(recipients)
  data = AD.Aggregate_Data(craigslist_url,kijiji_url,used_vic_url)
  
  while True:
    data.update_rentals()
    print("Rentals Checked at",datetime.now())
    new = data.diff()
    if new is None:
      sleep(5*60)
    elif len(new) == 0:
      sleep(5*60)
    else:
      email.send_email(new)
      sleep(5*60)
    

if __name__ == "__main__":
  main()