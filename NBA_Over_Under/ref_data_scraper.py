# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 08:22:23 2019

@author: Ken
"""

from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import datetime

#2015-2016 season 
def get_date_range(date1, date2):
    start = datetime.datetime.strptime(date1, "%d-%m-%Y")
    end = datetime.datetime.strptime(date2, "%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    all_dates = [x.strftime("%Y-%m-%d") for x in date_generated]
    return all_dates 

season2015 = get_date_range('02-12-2015','19-06-2016')
season2016 = get_date_range('25-10-2016','12-06-2017')
season2017 = get_date_range('17-10-2017','08-06-2018')
season2018 = get_date_range('16-10-2018','13-06-2019')
season2019 = get_date_range('22-10-2019','10-12-2019')


#2016-2017
start = datetime.datetime.strptime("02-12-2015", "%d-%m-%Y")
end = datetime.datetime.today()
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
all_dates = [x.strftime("%Y-%m-%d") for x in date_generated]

#2017-2018
start = datetime.datetime.strptime("02-12-2015", "%d-%m-%Y")
end = datetime.datetime.today()
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
all_dates = [x.strftime("%Y-%m-%d") for x in date_generated]

#2018-2019
start = datetime.datetime.strptime("02-12-2015", "%d-%m-%Y")
end = datetime.datetime.today()
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
all_dates = [x.strftime("%Y-%m-%d") for x in date_generated]

#2019-Present

def select_date_click(date,browser):
    browser.find_element(By.XPATH,"//button[@class='dropdown-toggle']").click();
    input_element = browser.find_element_by_id('ref-date')
    input_element.clear()
    input_element.send_keys(date)
    input_element.send_keys(Keys.ENTER)
    input_element.send_keys(Keys.ENTER)

def select_date(date,browser):
    input_element = browser.find_element_by_id('ref-date')
    input_element.clear()
    input_element.send_keys(date)
    input_element.send_keys(Keys.ENTER)
    input_element.send_keys(Keys.ENTER)
    
def get_element_txt(xpath,browser):
    elem = browser.find_elements_by_xpath(xpath)
    elem_text = [x.text for x in elem]
    return elem_text

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

browser = webdriver.Chrome(executable_path='/Users/Ken/OneDrive/Documents/chromedriver', chrome_options=option)
browser.get("https://official.nba.com/referee-assignments/")

# Wait 20 seconds for page to load
timeout = 20

try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//h1[@class='entry-title']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

    
try:
    select_date('2015-12-02',browser)
    time.sleep(4)
    titles_element = get_element_txt("//div[@class='nba-refs-content']",browser)
    date_element = get_element_txt("//div[@class='entry-meta']",browser)
    # print out all the titles.
    print('titles:')
    print(titles_element[0].split('/n'))
    print(date_element)
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()
    
titles_element[0].split('\n')
date_element[0]



def refs_from_dates(dates):
    date_game = {}
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    browser = webdriver.Chrome(executable_path='/Users/Ken/OneDrive/Documents/chromedriver', chrome_options=option)
    browser.get("https://official.nba.com/referee-assignments/")
    
    timeout = 20
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//h1[@class='entry-title']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()
    select_date_click(dates[0],browser)
    time.sleep(8)
    titles_element = get_element_txt("//div[@class='nba-refs-content']",browser)
    date_element = get_element_txt("//div[@class='entry-meta']",browser)
    print(dates[0])
    date_game[dates[0]] = titles_element[0].split('\n')
    
    for i in dates:
        try:
            select_date(i,browser)
            time.sleep(6)
            titles_element = get_element_txt("//div[@class='nba-refs-content']",browser)
            date_element = get_element_txt("//div[@class='entry-meta']",browser)
            print(i)
            date_game[i] = titles_element[0].split('\n')
            
        except TimeoutException:
            print("Timed out waiting for page to load")
            browser.quit()
    return date_game
    
game_refs_2015 = refs_from_dates(season2015)
game_refs_2016 = refs_from_dates(season2016)
game_refs_2017 = refs_from_dates(season2017)
game_refs_2018 = refs_from_dates(season2018)
game_refs_2019 = refs_from_dates(season2019)

import json

with open('data_2019.json', 'w') as fp:
    json.dump(game_refs_2019, fp)
    
with open('data_2018.json', 'w') as fp:
    json.dump(game_refs_2018, fp)

with open('data_2017.json', 'w') as fp:
    json.dump(game_refs_2017, fp)

with open('data_2016.json', 'w') as fp:
    json.dump(game_refs_2016, fp)

with open('data_2015.json', 'w') as fp:
    json.dump(game_refs_2015, fp)

def to_dataframe(ref_dict):
    rlist = []
    for i in ref_dict.keys():
        if len(ref_dict[i]) <= 1:
            pass
        else:
            for j in range(len(ref_dict[i])-1):
                rlist.append([i,ref_dict[i][j+1]])
    d_out = pd.DataFrame(rlist)
    d_out.columns = ['date','gameAndRefs']
    return d_out

gr2015 = to_dataframe(game_refs_2015)
gr2016 = to_dataframe(game_refs_2016)
gr2017 = to_dataframe(game_refs_2017)
gr2018 = to_dataframe(game_refs_2018)
gr2019 = to_dataframe(game_refs_2019)

frames = [gr2015,gr2016,gr2017,gr2018,gr2019]

total_data = pd.concat(frames)
total_data.to_csv('games_refs_by_date.csv')

# find_elements_by_xpath returns an array of selenium objects.
#titles_element = browser.find_elements_by_xpath("//div[@class='nba-refs-content']")
#date_element = browser.find_elements_by_xpath("//div[@class='entry-meta']")

# use list comprehension to get the actual repo titles and not the selenium objects.
#titles = [x.text for x in titles_element]
#dates = [x.text for x in date_element]
# print out all the titles.
#print('titles:')
#print(titles, '\n')
#print(dates)