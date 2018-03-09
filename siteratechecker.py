from datetime import datetime, timedelta
from selenium import webdriver
import re as rx
import time
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Global variable
d_time = ""

#Username

user = input()
#Password
pwd = input()
############################################
#######################################

# Do not forget to change the driverpath
driverpath = '~\\chromedriver.exe'
driver = webdriver.Chrome(driverpath)
# Open up test environment
driver.get('https://randomsite.com/login')
driver.maximize_window()

# Enter Username
emailElem = driver.find_element_by_id('username')
emailElem.send_keys(user)
print('User name entered')

# Enter password
pwdElem = driver.find_element_by_id('password')
pwdElem.send_keys(pwd)
print('Password entered')

# Press submit button to login
time.sleep(0.5)
driver.find_element_by_xpath("//button[@type='submit']").click()
print('Has been logged into CLO site')


# Send email notification function
def email_notif():
   global d_time
   SENDERNAME = 'CLO Quality'
   SENDER = 'RatePageTest@myemail.com'

# Replace recipient@example.com with a "To" address.
# Can add more emails into the list
   RECIPIENT  = ['myemail@user.com']

# Replace smtp_username with your Amazon SES SMTP user name.
   USERNAME_SMTP = "UsernameSMTP"

# Replace smtp_password with your Amazon SES SMTP password.
   PASSWORD_SMTP = "PasswordSMTP"


# Enter your host and port
   HOST = "ourhost.amazonaws.com"
   PORT = 587

# The subject line of the email.
   SUBJECT = 'Interest Rate Information page checker'

# The email body for recipients with non-HTML email clients.
   BODY_TEXT = ("Interest rate information page does not work for " + str(d_time) +
                ".")

# Create message container - the correct MIME type is multipart/alternative.
   msg = MIMEMultipart('alternative')
   msg['Subject'] = SUBJECT
   msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
   msg['To'] = ",".join(RECIPIENT)

# Record the MIME types of both parts - text/plain and text/html.
   part1 = MIMEText(BODY_TEXT, 'plain')

   msg.attach(part1)

   # Try to send the message.
   try:
     server = smtplib.SMTP(HOST, PORT)
     server.ehlo()
     server.starttls()
     #stmplib docs recommend calling ehlo() before & after starttls()
     server.ehlo()
     server.login(USERNAME_SMTP, PASSWORD_SMTP)
     server.sendmail(SENDER, RECIPIENT, msg.as_string())
     server.close()
   # Display an error message if something goes wrong.
   except Exception as e:
     print ("Error: ", e)
   else:
     print ("Email sent!")

def site_checker():
   url = 'https://mywebsite/interestratesinformation'
   driver.get(url)
   print('Check if the website is working')
   contents = ""
   contents = driver.find_element_by_xpath("/html/body/div[1]").text
   content_list = contents.splitlines()

   for i in content_list:
    # Send email when the Interest Rate Information Page does not work
      if rx.search('There is a problem with this part of the service,', i):
         print (i)
         time.sleep(5)
         email_notif()
         return False
   else:
      time.sleep(5)
      print ("Site is working!")
      return True

print('How many days do you want to go back?')


# Default value of 2 for test
# Change n for further test, being n the number of days to loop back

n = 2
print('Checking Interest Rate Information page for ' + str(n) + ' days')

for i in range(n):
  #d = datetime.now() - timedelta(i)
  # datetime() is the date from
  d = datetime(2018, 1, 30) - timedelta(i)
  d_time = d.strftime("%Y%m%d")
  #  driver.get('https://clo-alpha.trepp.com/admin/interestratesinformation/' + str(d_time))
  driver.get('https://mywebsite/interestratesinformation/' + str(d_time))

  if site_checker():
      print('Checking Interest Rate Information page:',d_time)

      # Scrape the page
      # Creates empty content string
      contents = ""
      # Store div contents to contents
      contents = driver.find_element_by_xpath("/html/body/div[1]").text
      # Split the contents one after another (line delimiter) and store intto a list
      content_list = contents.splitlines()
      # A dictionary for each Market Data Curve
      rates_Euribor = {
         "Euribor.1w" : False,
         "Euribor.1m" : False,
         "Euribor.2m" : False,
         "Euribor.3m" : False,
         "Euribor.6m" : False
      }

      rates_USDLibor = {
         "USDLibor.1w" : False,
         "USDLibor.1m" : False,
         "USDLibor.3m" : False,
         "USDLibor.6m" : False
      }
      # Uncomment if needed more checks or add in more elements
      # into the dictionary

      # rates_SEKLibor = {
      #  "SEKLibor.1m" : False,
      #  "SEKLibor.3m" : False,
      #  "SEKLibor.6m" : False

      print('Checks for Market Data Curves: ')

      for j in content_list:
         # Check for Euribors
         if rx.search("Euribor.1m" , j): # Using regex to check for the exact string
            rates_Euribor['Euribor.1m'] = True
         elif rx.search("Euribor.3m", j):
            rates_Euribor['Euribor.3m'] = True
         elif rx.search("Euribor.6m", j):
            rates_Euribor['Euribor.6m'] = True

         #Check for USDLibors
         elif rx.search("USDLibor.1m", j):
            rates_USDLibor['USDLibor.1m'] = True
         elif rx.search("USDLibor.3m", j):
            rates_USDLibor['USDLibor.3m'] = True
         elif rx.search("USDLibor.6m", j):
            rates_USDLibor['USDLibor.6m'] = True


      # Print findings of test for Euribors
      print("=====Findings=====")
      for i, j in rates_Euribor.items():
         print(i, ':', j)

      # Print findings of test for USDLibors
      print("=====Findings=====")
      for i, j in rates_USDLibor.items():
         print(i, ':', j)

      print('Finished checking: '+ str(d_time) + '. No other issues found...')
      print("===========================================================")

      ##END OF PROGRAM
      print('\t*****PROGRAM FINISHED*****')
