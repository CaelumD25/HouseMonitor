import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from house_collection import HouseCol
import sys

def construct_card(name,link,cost,beds,location,distance):
  card = """
  <div class="row rental-item">
    <hr />
    <h4>
      <a style="font-size: 1.2em;" class="title" href="{}">{}</a>
    </h4>
    <div class="row">
      <p class="cost">Cost: {}</p>
      <p class="beds">Beds: {}</p>
      <p class="location">Location: {}</p>
      <p class="distance">Distance from UVic(km): {}</p>
    </div>
  </div>
  """.format(link,name,cost,beds,location,distance)
  return card

def add_cards(housing_objs:HouseCol):
  new_cards = housing_objs.update()
  html = ""
  num = 0
  for obj in new_cards:
    html += construct_card(obj.get_name(),obj.get_link(),obj.get_cost(),obj.get_beds(),obj.get_loc(),obj.get_dist())
    num += 1
  return html, num

def create_rental_html(housing_objs:HouseCol,):
  cards, num = add_cards(housing_objs)
  with open('html_files/template.html', 'r') as html:
    contents = html.read()
    soup = BeautifulSoup(contents, 'html.parser')
  html.close()
  rentals = soup.find("div","rental-items")
  cards = BeautifulSoup(cards,"html.parser")
  rentals.append(cards)
  number_rentals = soup.find(id="new-rentals")
  number_rentals.append(str(num)+ " New Rentals")
  return soup, num
  
def connect_to_server():
  try:
    sender_email = "uvicrentalsearch@gmail.com"
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
    server.login(sender_email, str(os.environ['rental_pass']))
    return server
  except:
    sys.exit("Likely an auth error, try https://accounts.google.com/DisplayUnlockCaptcha")

def send_rental_email(html:str,server):
  sender_email = "uvicrentalsearch@gmail.com"
  receiver_email = "caelumdudek25@gmail.com"

  message = MIMEMultipart("alternative")
  message["Subject"] = "New Rentals"
  message["From"] = sender_email
  message["To"] = receiver_email

  # Create the plain-text and HTML version of your message

  message.attach(MIMEText(html, "html"))

  try:
    server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
  except:
    sys.exit("Failed Sending Mail")
  
      
