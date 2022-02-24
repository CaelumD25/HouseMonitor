import pandas as pd
import requests
import Rental
import Collect_Craigslist as CC
import Collect_Kijiji as CK
import Collect_Used_Vic as CUV
from os import path

def rentals_to_df(rentals: Rental) -> pd.DataFrame:
  df = {"name":[],"cost":[],"beds":[],"distance":[],"location":[],"link":[]}
  for rental in rentals:
    df["name"].append(rental.get_name())
    df["cost"].append(rental.get_cost())
    df["beds"].append(rental.get_beds())
    df["distance"].append(rental.get_distance())
    df["location"].append(rental.get_location())
    df["link"].append(rental.get_link())
  return pd.DataFrame(df)
  
def file_exists(loc: str):
  return path.exists(loc)

class Aggregate_Data:
  def __init__(self, craigslist_url, kijiji_url, used_vic_url):
    self.craigslist_url = craigslist_url
    self.kijiji_url = kijiji_url
    self.used_vic_url = used_vic_url
    if file_exists("data_files/gen_houses.json"):
      self.rentals = pd.read_json("data_files/gen_houses.json")
    else:
      self.rentals = self.generate_rentals()

    if file_exists("data_files/prev_houses.json"):
      self.prev_rentals = pd.read_json("data_files/prev_houses.json")
    else:
      self.update_rentals()

    #self.new_rentals = self.diff()

  def __str__(self):
    return str(self.rentals.head())  
  
  def generate_rentals(self,save=True):
    craigslist_html = requests.get(self.craigslist_url).text
    kijiji_html = requests.get(self.kijiji_url).text
    used_vic_html =  requests.get(self.used_vic_url).text

    craigslist_rentals = CC.collect_rental_objects(craigslist_html)
    kijiji_rentals = CK.collect_rental_objects(kijiji_html)
    used_vic_rentals = CUV.collect_rental_objects(used_vic_html)
    aggregated_data = craigslist_rentals + kijiji_rentals + used_vic_rentals

    df = rentals_to_df(aggregated_data)
    if save:
      df.to_json("data_files/gen_houses.json")
    self.rentals = df
    return df

  def update_rentals(self):
    self.prev_rentals = pd.concat([self.prev_rentals,self.rentals], ignore_index = True).drop_duplicates()
    self.prev_rentals.to_json("data_files/prev_houses.json")
    self.generate_rentals()

  def diff(self):
    if self.rentals.equals(self.prev_rentals):
      return None
    else:
      ls_gen = self.rentals.values.tolist()
      ls_prev = self.prev_rentals.values.tolist()
      tmp = []
      for gen in ls_gen:
        unique = True
        for prev in ls_prev:
          if gen[0] == prev[0]:
            unique = False
        if unique:
          name,cost,beds,distance,location,link = gen
          tmp.append(Rental.Rental(name,cost,beds,distance,location,link))
      return rentals_to_df(tmp)
          
      


