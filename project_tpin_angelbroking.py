# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 23:58:19 2022

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

#SETTING UP TELEGRAM BOT
def telegram(message):
    bot_token = '1860332743:AAH2peiKmw_hQDQ2ICaWzAUbQ0RBHPlUHxk'
    bot_chatID = '1020359820'
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

#MAIL ID AND PASSWORD

GMAIL_USERNAME="amritanshsinggautam@gmail.com"

GMAIL_PASSWORD="vinodsinghgautam"

#ANGEL BROKING PASSWORD

ANGEL_USERNAME="amritanshsinggautam@gmail.com"

ANGEL_PASSWORD="tush@r123456"

#TPIN

CDSL_PIN="250550"


#ANGELBROKING TPIN VERIFICATION
###############################################################################

PORTFOLIO_URL="https://trade.angelbroking.com/portfolio/equity/index_v1?flag=cdsl"



###############################################################################

driver=webdriver.Chrome(executable_path=WEB_DRIVER_LOCATION,options=options)
driver.get(PORTFOLIO_URL)

print("khulgya")


#  filling the user id and password
driver.find_element_by_id('txtUserID').send_keys(ANGEL_USERNAME)

driver.find_element_by_id('txtTradingPassword').send_keys(ANGEL_PASSWORD)

# clicking login button

driver.find_element_by_id("loginBtn").click()

driver.implicitly_wait(60)

print("login ho gya")

from selenium.webdriver.common.action_chains import ActionChains

#PROCEDE TO CDSL

button=driver.find_element_by_class_name("btn.btn-filled.cdslProceed")
driver.implicitly_wait(10)
ActionChains(driver).move_to_element(button).click(button).perform()

print("submit button dab diya")
driver.implicitly_wait(60)

time.sleep(10)


#SWITCH FRAME AND ENTER OTP AND PROCEDE

driver.switch_to.frame(driver.find_element_by_xpath('/html/body/div[10]/div/div/div[2]/iframe'))


driver.find_element_by_id("txtPIN").send_keys(CDSL_PIN)
driver.find_element_by_id("btnCommit").click()
driver.implicitly_wait(60)



# Calculating the current system time and converting to seconds
"""current_time=time.localtime()

current_minute=int(time.strftime("%M", current_time))
current_second=int(time.strftime("%S", current_time))
total_seconds=(current_minute*60)+current_second

total_seconds=total_seconds-50
print(total_seconds)
"""
time.sleep(120)


###############################################################################


pattern='(\d{2}):(\d{2}):(\d{2})'


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

token='tokensing.json'

gmail(token)

#print(OTP)
driver.implicitly_wait(60)
#driver.switch_to.frame(driver.find_element_by_xpath('/html/body/div[10]/div/div/div[2]/iframe'))

driver.find_element_by_id("OTP").send_keys(msg)
driver.implicitly_wait(60)
driver.find_element_by_id("VerifyOTP").click()
driver.implicitly_wait(60)
time.sleep(3)
print("Success")
driver.quit()






