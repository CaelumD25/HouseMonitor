import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
import pandas as pd
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

def connect_to_server():
  try:
    sender_email = "uvicrentalsearch@gmail.com"
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
    server.login(sender_email, str(os.environ['rental_pass']))
    print("Email Successfully Logged in:\n",str(server))
    return server
  except:
    sys.exit("Likely an auth error, try https://accounts.google.com/DisplayUnlockCaptcha")

class Email_Rentals:
  def __init__(self, recipients = []):
    self.recipients = recipients
    self.cards_html = None
    self.num_rentals = 0
    self.html = None

  def gen_cards(self,rentals: pd.DataFrame):
    rentals = rentals.values.tolist()
    html = ""
    for name,cost,beds,distance,location,link in rentals:
      html += construct_card(name,link,cost,beds,location,distance)
    self.cards_html = html
    self.num_rentals = len(rentals)

  def gen_html(self, rentals: pd.DataFrame):
    self.gen_cards(rentals)
    with open('html_files/template.html', 'r') as html:
      contents = html.read()
      soup = BeautifulSoup(contents, 'html.parser')
    html.close()
    rentals = soup.find("div","rental-items")
    cards = BeautifulSoup(self.cards_html,"html.parser")
    rentals.append(cards)
    number_rentals = soup.find(id="new-rentals")
    number_rentals.append(str(self.num_rentals)+ " New Rentals")
    self.html = soup.prettify()

  def send_email(self,rentals: pd.DataFrame):
    server = connect_to_server()
    sender_email = "uvicrentalsearch@gmail.com"
    for receiver_email in self.recipients:
      message = MIMEMultipart("alternative")
      message["Subject"] = "New Rentals"
      message["From"] = sender_email
      message["To"] = receiver_email
    
      # Create the plain-text and HTML version of your message
      if self.html is None:
        self.gen_html(rentals)
        
      message.attach(MIMEText(self.html, "html"))
    
      server.sendmail(sender_email, receiver_email, message.as_string())
      print("Email sent to",receiver_email)
      server.quit()