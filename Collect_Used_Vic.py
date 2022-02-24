from bs4 import BeautifulSoup
from Rental import Rental
import re

def collect_rental_objects(html: str):
  """
  Returns a list of Rental objects from Used Vic
  """
  tmp = []
  soup  = BeautifulSoup(html,"html.parser")
  rental_list = __divide_rental_objects(soup)
  for rentals in rental_list:
    name = __extract_name(rentals)
    cost = __extract_cost(rentals)
    beds = __extract_beds(rentals)
    distance = __extract_distance(rentals)
    location = __extract_location(rentals)
    link = __extract_link(rentals)
    tmp.append(Rental(name,cost,beds,distance,location,link))
  return tmp

def __divide_rental_objects(soup: BeautifulSoup) -> list:
  pages = soup.find_all("div","used-item")
  return pages

def __extract_name(soup: BeautifulSoup) -> str:
  name = soup.find("a","ad-list-item-link",string=True).string
  name = name.split(" · ")[-1].strip(" ")
  return name

def __extract_cost(soup: BeautifulSoup) -> int:
  cost = soup.find("a","ad-list-item-link",string=True).string
  match_obj = re.search("^\$(\d{0,2},?\d{3}).*",cost)
  if match_obj:
    cost = int(match_obj.group(1).replace(",",""))
  else:
    cost = None
  return cost

def __extract_beds(soup: BeautifulSoup) -> int:
  beds = soup.find("a","ad-list-item-link",string=True).string.lower()
  beds = beds.replace("-"," ")

  quantity_syn_1 = ["1","one","single","studio","bachelor"]
  quantity_syn_2 = ["2","two"]

  match_obj = re.search(r"(\b\w{1,5}(?= bedroom| bed| bdrm))",beds)
  if match_obj:
    beds = match_obj.group(1)
  for syn in quantity_syn_1:
    if syn in beds:
      return 1
  for syn in quantity_syn_2:
     if syn in beds:
       return 2
  return None


def __extract_distance(soup: BeautifulSoup) -> str:
  return None

def __extract_location(soup: BeautifulSoup) -> str:
  location = [x for x in soup.find_all("div", "col-auto", "text-grey")][1].string
  return location

def __extract_link(soup: BeautifulSoup) -> str:
  link = "https://www.usedvictoria.com" + soup.find("a","ad-list-item-link",href=True)["href"]
  return link