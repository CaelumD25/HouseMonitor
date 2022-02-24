import requests
import pandas as pd
from house import HousingInfo
from kijiji import gen_kijiji_obj
from craigs import gen_craigs_obj
from used import gen_used_obj
import shutil

# TODO Fix
def Diff():
  df_cur = pd.read_json("data_files/gen_houses.json")
  df_prev = pd.read_json("data_files/prev_houses.json")
  df_diff = pd.concat([df_cur,df_prev]).drop_duplicates(keep=False)

  print("cur\n",df_cur.head())
  print("prev\n",df_prev.head())
  print("Diff: ", len(df_diff))
  for x in range(len(df_diff)):
    nxt = next(df_diff.iterrows())
    print(nxt["name"])
  

class HouseCol:
  def __init__(self):
    

    self.kijiji = "https://www.kijiji.ca/b-for-rent/victoria-bc/c30349001l1700173?ll=48.463407%2C-123.311694&address=University+of+Victoria%2C+Victoria%2C+British+Columbia&radius=4.0"

    self.used_vic = "https://www.usedvictoria.com/real-estate-rentals?lat=48.464726505426725&lon=-123.31363677978517&ca=%7B%227%22%3A%5B%220%22,%222%22%5D,%228%22%3A%5B%221%22,%221%22%5D%7D&radius=5000&xflags=wanted"

    self.tmp = []
    self.length = 0

  def gen(self):
    craigs_results = requests.get(self.craigslist).text
    self.tmp = gen_craigs_obj(craigs_results)

    kijiji_results = requests.get(self.kijiji).text
    self.tmp = self.tmp + gen_kijiji_obj(kijiji_results)

    used_vic_results = requests.get(self.used_vic).text
    self.tmp = self.tmp + gen_used_obj(used_vic_results)
    
    df = pd.DataFrame(columns=self.tmp[0].get_dict())
    
    for ind, entry in enumerate(self.tmp):
      ls = [entry.get_dict()[x] for x in entry.get_keys()]
      df.loc[ind] = ls
    
    try:
      shutil.copyfile("data_files/gen_houses.json","data_files/prev_houses.json")
    except FileNotFoundError:
      pass

    df.to_json("data_files/gen_houses.json")
    
  def __len__(self):
    return self.length

  def get_entries(self):
    return self.stored



