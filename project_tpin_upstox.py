# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 00:46:04 2022

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

import bs4 as bs
from bs4 import NavigableString, Tag
import re

# import for telegram message
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

import requests

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


###############################################################################


WEB_DRIVER_LOCATION = r"C:\Users\amrit\Downloads\Compressed\chromedriver_win32\chromedriver.exe"

#WEB_DRIVER_LOCATION = '/usr/bin/chromedriver'

#ID AND PASSWORDS

UPSTOX_USERNAME="?"
UPSTOX_PASSWORD="?"
UPSTOX_PIN="?"

CDSL_PIN="?"

#BROKER URL

UPSTOX_URL="https://login-v2.upstox.com/"

#CHROME OPTIONS

options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_argument("--window-size=2200,1200")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
driver=webdriver.Chrome(executable_path=WEB_DRIVER_LOCATION,options=options)


# navigating to upstox url
driver.get(UPSTOX_URL)
driver.implicitly_wait(60)


#  filling the user id and password
driver.find_element_by_id('userCode').send_keys(UPSTOX_USERNAME)
driver.implicitly_wait(60)


driver.find_element_by_xpath('/html/body/main/div/div[2]/div/div/form/div[4]/div/div/div/input').send_keys(UPSTOX_PASSWORD)

# clicking login button
driver.find_element_by_id("submit-btn").click()
driver.implicitly_wait(60)

driver.find_element_by_id('yob').send_keys(UPSTOX_PIN)
driver.implicitly_wait(60)

#exiting STUPIDITY

driver.find_element_by_xpath('/html/body/main/div[1]/div[2]/div[2]/div[4]/button[1]/div/div').click()

driver.implicitly_wait(60)

# OPENING HOLDINGS

driver.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/section/div/div[2]/div/div/div/div[1]/div[3]').click()

driver.implicitly_wait(60)


#OPENING SELL PANNEL
driver.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/section/div/div[2]/div/div/div/div[2]/div/div/table/tbody/tr[1]/td[10]').click()

driver.implicitly_wait(60)

#SELL BUTTON
time.sleep(3)

driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/div[1]/div/div/div[2]').click()

driver.implicitly_wait(60)
#NSE OR BSE
time.sleep(1)

driver.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div[1]').click()
driver.implicitly_wait(60)
#REVIEW SELL ORDER


driver.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/div/div/div/form/div[2]/button').click()
time.sleep(5)
#CDS WINDOW

cdsl_window=driver.window_handles[1]
driver.switch_to.window(cdsl_window)
driver.implicitly_wait(120)
time.sleep(4)

#CONTINUE TO CDSL

driver.find_element_by_xpath('/html/body/main/div[1]/div[2]/div[2]/div[2]/div[2]').click()
driver.implicitly_wait(60)

# ENTER TPIN AND NEXT

driver.find_element_by_id("txtPIN").send_keys(CDSL_PIN)
driver.find_element_by_id("btnCommit").click()
driver.implicitly_wait(60)

time.sleep(120)

token='token.json'

gmail(token)

# OTP ENTERING IN THE INPUT

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

