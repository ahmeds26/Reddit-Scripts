from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
from proxy import *
from new_email import *
import time
import csv
import os
import json




def login(username, password):
    login_url = 'https://www.reddit.com/login/'
    driver.get(login_url)
    time.sleep(2)

    email_box = driver.find_element_by_id('loginUsername')
    email_box.send_keys(username)
    password_box = driver.find_element_by_id('loginPassword')
    password_box.send_keys(password)
    login_button = driver.find_element_by_xpath('//button[@type="submit"]')
    login_button.click()
    time.sleep(5)
    
def getUsers(url):
    driver.get(url)
    time.sleep(5)
    try:
        discussion_button = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[1]/div[2]/div[5]/div/button')
        discussion_button.click()
        time.sleep(3)
    except:
        pass
    try:
        view_more_button = driver.find_element_by_id('moreComments-t1_gm4adq8')
        view_more_button.click()
        time.sleep(3)
    except:
        pass
    # scrolling down to the end of page
    last_height_posts = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        page = driver.page_source
        soup = bs(page, 'html.parser')
        users = soup.select('a.f3THgbzMYccGW8vbqZBUH._23wugcdiaj44hdfugIAlnX')
        if len(users) > 1000:
            break
        new_height_posts = driver.execute_script("return document.body.scrollHeight")
        if new_height_posts == last_height_posts:
            break
        last_height_posts = new_height_posts

    users_links = []
    previous_link = ''
    for i in range(0, len(users)):
        user_link = 'https://www.reddit.com' + users[i].get('href')
        if previous_link==user_link:
            continue
        else:
            users_links.append(user_link)
    return users_links
    


def sendMessage(users, limit):
    for l in range(0, limit):
        print('\n>>>> Processing User Link: ' + users[l] + ' ....')
        driver.get(users[l])
        time.sleep(5)
        options_button = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[4]/div[2]/div/div[1]/div/div[6]/div/button')
        options_button.click()
        time.sleep(2)
        message_button = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[4]/div[2]/div/div[1]/div/div[6]/a[1]')
        message_button.click()
        time.sleep(6)
        driver.switch_to.window(driver.window_handles[1])
        subject_text = 'DeFi project'
        for m in range(1, len(list(messages_dict))):
            iframe = driver.find_element_by_class_name('saPujbGMyXRwqISHcmJH9')
            driver.switch_to.frame(iframe)
            
            subject_box = driver.find_element_by_xpath('//input[@name="subject"]')
            subject_box.send_keys(subject_text)
            subject_box.send_keys(Keys.TAB)
            message_box = driver.find_element_by_xpath('/html/body/div[3]/form[2]/div[6]/div/div/div[2]/div/div[1]/textarea')    
            message_box.send_keys(messages_dict[list(messages_dict)[m]])
            driver.switch_to.default_content()
            '''
            iframes = driver.find_elements_by_tag_name('iframe')
            driver.switch_to.frame(iframes[1])
            
            captcha_box = driver.find_element_by_id('recaptcha-anchor')
            captcha_box.click()
            driver.switch_to.default_content()
            '''
            time.sleep(100)
            iframe = driver.find_element_by_class_name('saPujbGMyXRwqISHcmJH9')
            driver.switch_to.frame(iframe)
            send_button = driver.find_element_by_id('send')
            send_button.click()
            time.sleep(1)
            status_message = driver.find_element_by_xpath('/html/body/div[3]/form[2]/span').text
            print('\n>>>>> ' + status_message + ' <<<<<')
            driver.refresh()
            time.sleep(3)
        driver.close()
    

if __name__ == "__main__":
    # Define input directory location
    input_dir = r'C:\Users\PC\Desktop'
    output_dir = r'C:\Users\PC\Desktop'
    output_file_name = 'Sample Reddit Output.csv'
    credentials_file_name = 'credentials.json'
    credentials_json_file = open(os.path.join(input_dir, credentials_file_name))
    credentials_data = json.load(credentials_json_file)
    
    input_file_name = 'Sample Accounts Output.csv'
    input_accounts_reader = csv.reader(open(os.path.join(input_dir, input_file_name), 'r', encoding='utf-8'))
    input_accounts = list(input_accounts_reader)
    input_accounts.pop(0)

    login_email = input_accounts[0][0]
    login_password = input_accounts[0][1]
    
    # Enter discussion url
    input_url = 'https://www.reddit.com/r/wallstreetbets/comments/ld4v2q/daily_discussion_thread_for_february_05_2021/'
    number_of_users = 1
    
    #f = csv.writer(open(os.path.join(output_dir, output_file_name), 'w', newline='', encoding="utf-8-sig"))
    #f.writerow(['User Link', ])
    messages_dict = {'first_message': 'Do you want a DM before a DeFi project launches? https://www.reddit.com/r/WSB_defi/', 
                     'second_message': 'Do you want a DM before a DeFi project launches? https://twitter.com/wsbcommander/status/1356827291783847941?s=21', 
                     'third_message': 'Do you want a DM before a DeFi project launches? https://www.reddit.com/r/WSB_defi/comments/lbj26s/hodl_and_stand_together_against_cefi/?utm_source=share&utm_medium=ios_app&utm_name=iossmf'
    }
    
    # Opening Chrome Driver
    driver = get_chromedriver(use_proxy=True)
    
    print('>>> Logging into Reddit Website...')
    login(login_email, login_password)
    
    print('\n>>> Getting Users Links....')
    users_list = getUsers(input_url)
    print(len(users_list))
    print('\n>>> Iterating over users....')
    sendMessage(users_list, number_of_users)
    
    driver.quit()




    