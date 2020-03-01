#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 17:50:36 2019

@author: doug hagey
"""
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.firefox.options import Options

#use selenium to scrape player data from Understat.com using all 4 filter options for "games"
try:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get('https://understat.com/league/EPL')
    # Default Table = All
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[1]/div[2]').click()
    driver.find_element_by_xpath('//div[2]/div/ul/li[1]').click()
    print('Getting Season Player Data')
    season_playertable = driver.find_element_by_xpath('//*[@id="league-players"]').get_attribute('innerHTML')
    time.sleep(5)
    # Get data for last 3 games
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[1]/div[2]').click()
    driver.find_element_by_xpath('//div[2]/div/ul/li[2]').click()
    time.sleep(5)
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[1]/button/i').click()
    time.sleep(5)
    print('Getting Player Data For Last 3 Games')
    three_game_playertable =driver.find_element_by_xpath('//*[@id="league-players"]').get_attribute('innerHTML')
    # Get data for last 5 games
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[1]/div[2]').click()
    time.sleep(5)
    driver.find_element_by_xpath('//div[2]/div/ul/li[3]').click()
    time.sleep(5)
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[1]/button/i').click()
    time.sleep(5)
    print('Getting Player Data For Last 5 Games')
    five_game_playertable =driver.find_element_by_xpath('//*[@id="league-players"]').get_attribute('innerHTML')
    # Get data for last 10 games
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[1]/div[2]').click()
    time.sleep(5)
    driver.find_element_by_xpath('//div[2]/div/ul/li[4]').click()
    time.sleep(5)
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div[1]/button/i').click()
    time.sleep(5)
    print('Getting Player Data For Last 10 Games')
    ten_game_playertable =driver.find_element_by_xpath('//*[@id="league-players"]').get_attribute('innerHTML')
    time.sleep(5)
    driver.close()
except Exception as e:
    print('Encountered a problem')
    driver.close()

#Create Pandas dataframes from each html table
season_df = pd.read_html(season_playertable)[0]
three_game_df = pd.read_html(three_game_playertable)[0]
five_game_df = pd.read_html(five_game_playertable)[0]
ten_game_df = pd.read_html(ten_game_playertable)[0]

print('Writing csv files')
season_df.to_csv('Understat_EPL_Player_Data_Season.csv', encoding='utf-8', index=False)
three_game_df.to_csv('Understat_EPL_Player_Data_3Game.csv', encoding='utf-8', index=False)
five_game_df.to_csv('Understat_EPL_Player_Data_5Game.csv', encoding='utf-8', index=False)
ten_game_df.to_csv('Understat_EPL_Player_Data_10Game.csv', encoding='utf-8', index=False)