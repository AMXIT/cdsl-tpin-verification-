# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 23:57:05 2022

@author: Amritansh S
"""
###############################################################################
#ALL IMPORTS 

from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import re
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#import config
#import easyimap as e
#import email.utils#
import bs4 as bs
from bs4 import NavigableString, Tag
import re

# import for telegram message
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

import requests

#import for totp
import pyotp

#SETTING UP TELEGRAM BOT
def telegram(message):
    bot_token = '?'
    bot_chatID = '?'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '*&parse_mode=Markdownv2&text=' + message
    
    response = requests.get(send_text)
    
    return response.json()


###############################################################################

#MAIL GETTING CODE GMAIL
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def gmail(token):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    global msg
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token):
        creds = Credentials.from_authorized_user_file(token, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    """if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())"""

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me',maxResults=1,labelIds=['INBOX'],q="from:edis@cdslindia.co.in is:unread").execute()
    message = results.get('messages', [])[0]

    if not message:
        print('No messages from CDSL found.')
    else:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        #print("Your latest message from CDSL :")
        email_data=msg['payload']['headers']
        for values in email_data:
            name=values["name"]
            if name == "From":
                from_name = values["value"]
                print(msg['snippet'])
                matchOTP = re.search('(\d{6})', str(msg['snippet']))
                msg=int(matchOTP.group())
                print(matchOTP.group())

###############################################################################


WEB_DRIVER_LOCATION = r"C:\Users\amrit\Downloads\Compressed\chromedriver_win32\chromedriver.exe"

#WEB_DRIVER_LOCATION = '/usr/bin/chromedriver'


#CHROME OPTIONS

options = webdriver.ChromeOptions()
options.add_argument("--headless")
#options.add_argument("--window-size=2200,1200")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("--window-size=1920,1080")

###############################################################################


###############################################################################

#ZERODHA TPIN AUTHENTICATION CODE

telegram("started zerodha ")

#PASSWORDS AND USERNAME

KITE_USERNAME=""
KITE_PASSWORD=""
#KITE_PIN=""
TOTP_COUPON=""
CDSL_PIN=""

WEB_DRIVER_LOCATION = r"C:\Users\amrit\Downloads\Compressed\chromedriver_win32\chromedriver.exe"

#WEB_DRIVER_LOCATION = '/usr/bin/chromedriver'

###############################################################################

# BROKER LINKS

KITE_URL="https://kite.zerodha.com/"
HOLDINGS_URL="https://kite.zerodha.com/holdings"


driver=webdriver.Chrome(executable_path=WEB_DRIVER_LOCATION,options=options)
driver.maximize_window()

# navigating to kite url
driver.get(HOLDINGS_URL)

#  filling the user id and password
driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div/div/form/div[2]/input").send_keys(KITE_USERNAME)
driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div/div/form/div[3]/input").send_keys(KITE_PASSWORD)
driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div/div/form/div[4]/button").click()
driver.implicitly_wait(60)
time.sleep(2)

# entering security pin
#GET TOTP
time.sleep(2)
totp = pyotp.TOTP(TOTP_COUPON)
KITE_PIN=totp.now()
driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div/div/form/div[2]/input").send_keys(KITE_PIN)
#driver.find_element_by_id('pin').send_keys(KITE_PIN)
driver.find_element_by_class_name("button-orange").click()


#driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div/div/form/div[2]/div/input").send_keys(KITE_PIN)
#driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div/div/form/div[3]/button").click()

driver.implicitly_wait(60)
time.sleep(2)

# selecting "Authorisation" option

driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div/section/div/div/div/span[2]/a[1]").click()

time.sleep(2)
driver.implicitly_wait(60)
kite_window=driver.window_handles[0]

#driver.find_element_by_class_name("button.button-blue").click()
driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div[2]/div/div/div[3]/div/button[1]").click()

time.sleep(2)
driver.implicitly_wait(60)

# Switching to CDSL page
cdsl_window=driver.window_handles[1]
driver.switch_to.window(cdsl_window)
driver.implicitly_wait(120)
time.sleep(4)



# Selecting "Continue to CDSL"
driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/button").click()
time.sleep(3)



# Entering TPIN
driver.find_element_by_id("txtPIN").send_keys(CDSL_PIN)
driver.find_element_by_id("btnCommit").click()
driver.implicitly_wait(120)


time.sleep(120)

token='token.json'

gmail(token)

#print(OTP)
driver.implicitly_wait(60)
driver.switch_to.window(cdsl_window)
driver.implicitly_wait(60)
driver.find_element_by_id("OTP").send_keys(msg)
driver.implicitly_wait(60)
driver.find_element_by_id("VerifyOTP").click()
driver.implicitly_wait(60)
time.sleep(3)
print("Success")
driver.quit()
telegram("successfull")

