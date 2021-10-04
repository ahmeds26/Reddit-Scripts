from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from proxy import *
from new_email import *
from datetime import datetime
import deathbycaptcha
import pyperclip
import requests
import random
import time
import csv
import os
import json


def solveCaptcha():
    Captcha_dict = {
            'proxy': '', 
            'proxytype': '', 
            'googlekey': '6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC', 
            'pageurl': 'https://www.reddit.com/register/'}
            
    json_Captcha = json.dumps(Captcha_dict)

    #client = deathbycaptcha.SocketClient(username, password, authtoken)
    # to use http client client = deathbycaptcha.HttpClient(username, password)
    client = deathbycaptcha.HttpClient(username, password, authtoken)

    tokenContainer = ''

    try:
        balance = client.get_balance()
        print(balance)

        # Put your CAPTCHA type and Json payload here:
        captcha = client.decode(type=4, token_params=json_Captcha)
        if captcha:
            # The CAPTCHA was solved; captcha["captcha"] item holds its
            # numeric ID, and captcha["text"] item its list of "coordinates".
            #print ("CAPTCHA %s solved: %s" % (captcha["captcha"], captcha["text"]))
            
            tokenContainer = captcha['text']
            if '':  # check if the CAPTCHA was incorrectly solved
                client.report(captcha["captcha"])
    except deathbycaptcha.AccessDeniedException:
        # Access to DBC API denied, check your credentials and/or balance
        print ("error: Access to DBC API denied," +
               "check your credentials and/or balance")
    return tokenContainer
    
def createAccount(email):
    #driver.execute_script("window.open();")
    #driver.switch_to.window(driver.window_handles[1])
    reddit_url = 'https://www.reddit.com/register/'
    driver.get(reddit_url)
    time.sleep(5)
    email_box = driver.find_element_by_id('regEmail')
    email_box.send_keys(email)
    continue_button = driver.find_element_by_xpath('//button[@type="submit"]')
    continue_button.click()
    time.sleep(5)

    username = email.split('@')[0]
    username_box = driver.find_element_by_id('regUsername')
    username_box.send_keys(username)
    time.sleep(3)
    password_box = driver.find_element_by_id('regPassword')
    if len(email.split('@')[0]) < 8:
        password = email.split('@')[0] + 'password'
        password_box.send_keys(password)
        time.sleep(3)
    else:
        password = email.split('@')[0]
        password_box.send_keys(password)
        time.sleep(3)
    tokenContainer = solveCaptcha()
    try:
        driver.switch_to.frame(driver.find_elements_by_tag_name('iframe')[0])
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, "rc-anchor-container")))
        driver.switch_to.default_content()
    except:
        error_message = 'Reddit Website Hanged!... Moving on...'
        return error_message
    driver.execute_script("document.getElementById('g-recaptcha-response').innerHTML='{}'".format(tokenContainer))
    
    time.sleep(5)

    signup_button = driver.find_element_by_class_name('SignupButton')
    signup_button.click()
    time.sleep(10)
    finish_button = driver.find_element_by_class_name('SubscribeButton')
    finish_button.click()
    time.sleep(15)
    account_tuple = (username, password)
    return account_tuple
    
    
def verifyAccount(verify_link):
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(verify_link)
    time.sleep(3)
    try:
        verify_email = driver.find_element_by_class_name('verify-button')
        verify_email.click()
        status_message = driver.find_element_by_class_name('result-status').text
        print(status_message)
    except:
        status_message = "Success!"
        print(status_message)
    time.sleep(3)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)
    
if __name__ == "__main__":
    # Define input directory location
    input_dir = r'C:\Users\PC\Desktop\Gary'
    output_dir = r'C:\Users\PC\Desktop\Gary'
    output_file_name = 'Sample Accounts Output'
    credentials_file_name = 'credentials.json'
    credentials_json_file = open(os.path.join(input_dir, credentials_file_name))
    credentials_data = json.load(credentials_json_file)
    
    # Put your DBC account username and password here.
    username = credentials_data["DBC_username"]
    password = credentials_data["DBC_password"]
    
    # you can use authtoken instead of user/password combination
    # activate and get the authtoken from DBC users panel
    authtoken = ""
    
    number_of_accounts = 5
    
    f = csv.writer(open(os.path.join(output_dir, '{}.csv'.format(output_file_name)), 'w', newline='', encoding="utf-8-sig"))
    f.writerow(['Reddit Username', 'Reddit Password'])
    
    for i in range(0, number_of_accounts):
        driver = get_chromedriver(use_proxy=True)
        # Getting new email
        print('>>>>\n Getting New Temp Email...')
        current_email = getEmail()
        
        # Creating new Reddit account
        print('>>>>>\n Creating New Reddit Account...')
        account_credentials = createAccount(current_email)
        if account_credentials=='Reddit Website Hanged!... Moving on...':
            driver.quit()
            time.sleep(5)
            continue
        
        # Verifying Reddit account
        print('>>>>>\n Verifying Reddit Account...')
        verify_link = verifyLink(current_email)
        verifyAccount(verify_link)
        print('>>>>\n Reddit Account Verified...')
        f.writerow(list(account_credentials))
        driver.quit()
        time.sleep(5)