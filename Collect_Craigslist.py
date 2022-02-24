from bs4 import BeautifulSoup
from Rental import Rental
import re

def collect_rental_objects(html: str):
  """
  Returns a list of Rental objects from Craigslist
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
  return soup.find_all("li","result-row")

def __extract_name(soup: BeautifulSoup) -> str:
  return str(soup.find("a","result-title").string)

def __extract_cost(soup: BeautifulSoup) -> int:
  cost = soup.find("span","result-price").string
  # For format of "$1,000"
  cost = cost.replace("$","").replace(",","")
  return int(cost)

def __extract_beds(soup: BeautifulSoup) -> int:
  # For the format "1br - 765ft"
  try:
    beds = str(soup.select("span.housing")[0])
    beds = int(re.search("(\d)br",beds).group(1))
  except Exception:
    beds = None
  return beds

def __extract_distance(soup: BeautifulSoup) -> str:
  distance = str(soup.find("span","maptag").string)
  # For the format "1.4km"
  return distance

def __extract_location(soup: BeautifulSoup) -> str:
  location = soup.find("span","result-hood").string.strip(" ()")
  if len(location) <= 1:
    return None
  return location

def __extract_link(soup: BeautifulSoup) -> str:
  link = soup.find("a","result-title")["href"]
  return link