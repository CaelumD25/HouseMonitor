from bs4 import BeautifulSoup
from Rental import Rental
import re

def collect_rental_objects(html: str):
  """
  Returns a list of Rental objects from Kijiji
  """
  tmp = []
  soup  = BeautifulSoup(html,"html.parser")
  rental_list = __divide_rental_objects(soup)

  for rentals, rental_info in rental_list:
    name = __extract_name(rentals)
    cost = __extract_cost(rentals)
    beds = __extract_beds(rental_info)
    distance = __extract_distance(rentals)
    location = __extract_location(rentals)
    link = __extract_link(rentals)
    tmp.append(Rental(name,cost,beds,distance,location,link))
  return tmp

def __divide_rental_objects(soup: BeautifulSoup) -> list:

  return zip(soup.find_all("div","info-container"),soup.find_all("div","rental-info"))

def __extract_name(soup: BeautifulSoup) -> str:
  name = soup.find("a","title").string.strip(" \n")
  return name

def __extract_cost(soup: BeautifulSoup) -> int:
  cost = str([x for x in soup.select("div.price")[0].stripped_strings][0])
  match_obj = re.match("\$(\d{0,2},?\d{3})\.00",cost)
  if match_obj:
    cost = int(match_obj.group(1).replace(",",""))
  else:
    cost = None
  return cost

def __extract_beds(soup: BeautifulSoup) -> int:
  try:
    beds = [x for x in soup.find("span","bedrooms").stripped_strings][0]
    beds =  beds.replace("Beds:\n","").replace(" + Den","").strip(" ")
    if beds == "Bachelor/Studio":
      beds = 1
    beds = int(beds)
  except Exception:
    beds = None
  return beds

def __extract_distance(soup: BeautifulSoup) -> str:
  distance = soup.find("div","distance").string.strip(" \n")
  return distance

def __extract_location(soup: BeautifulSoup) -> str:
  location = [x for x in soup.find("div","location").stripped_strings][0]
  return location

def __extract_link(soup: BeautifulSoup) -> str:
  link = "https://www.kijiji.ca" + soup.find("a","title")["href"]
  return link