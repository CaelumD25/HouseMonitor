from bs4 import BeautifulSoup
from house import HousingInfo
import re

def extract_price(price: str):
    try:
        price = price.replace("$", "")
        price = price.replace(".00", "")
        price = price.replace(",", "")
        return int(price)
    except ValueError:
        return "Barter for"
    except AttributeError:
        return "Barter for"

def extract_str(title):
    return title.replace("\n","").replace("\t","").strip(" ")

def extract_int(distance):
    try:
        distance = re.match("\D*(\d+)\D*", distance)
        if distance == None:
          raise TypeError
        distance = distance.group(1)
        return int(distance)
    except TypeError:
        return -1

def gen_kijiji_obj(kijiji_result:str):
    soup = BeautifulSoup(
        BeautifulSoup(kijiji_result, "html.parser").prettify(), "html.parser")
    objs = soup.find_all("div", "search-item")
    housing_objs = []
    for obj in objs:
        cur = HousingInfo()
        cur.set_name(extract_str(obj.find("a", "title").string))
        cur.set_link("https://www.kijiji.ca" + obj.find("a", "title")["href"])
        cur.set_cost(extract_price(obj.find("div", "price").string))
        cur.set_dist(extract_int(obj.find("div", "distance").string))
        cur.set_loc(extract_str(obj.find("div", "location").span.string))
        try:
          bedrooms = obj.find("span","bedrooms").contents[-1]
          cur.set_beds(extract_int(bedrooms.string))
        except AttributeError:
          cur.set_beds("Not Listed")
        housing_objs.append(cur)
    return housing_objs

