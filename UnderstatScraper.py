#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 1 17:50:36 2020

@author: doug hagey
"""
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.firefox.options import Options
import requests
import ssl

def scrape_understat(payload):
    url = 'https://understat.com/main/getPlayersStats/'
    headers = {'content-type':'application/json; charset=utf-8',
    'Host': 'understat.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '39',
    'Origin': 'https: // understat.com',
    'Connection': 'keep - alive',
    'Referer': 'https: // understat.com / league / EPL'
    }
    response = requests.post(url, data=payload, headers = headers, verify=True)
    response_json = response.json()
    inner_wrapper = response_json['response']
    json_player_data = inner_wrapper['players']
    return json_player_data

def clean_df(player_df):
    player_df.drop(['id', 'yellow_cards','red_cards', 'xGChain','xGBuildup'], axis=1, inplace=True)
    return(player_df)

#Create Pandas dataframes from each html table
print('Getting data for last 3 matches')
json_player_data = scrape_understat({'league':'EPL', 'season':'2019', 'n_last_matches': '3'})
three_game_table = pd.DataFrame(json_player_data)
three_game_df = clean_df(three_game_table)

print('Getting data for the whole season')
json_player_data = scrape_understat({'league':'EPL', 'season':'2019'})
season_table = pd.DataFrame(json_player_data)
season_df = clean_df(season_table)

print('Getting data for last 5 matches')
json_player_data = scrape_understat({'league':'EPL', 'season':'2019', 'n_last_matches': '5'})
five_game_table = pd.DataFrame(json_player_data)
five_game_df = clean_df(five_game_table)

print('Getting data for last 10 matches')
json_player_data = scrape_understat({'league':'EPL', 'season':'2019', 'n_last_matches': '10'})
ten_game_table = pd.DataFrame(json_player_data)
ten_game_df = clean_df(ten_game_table)

print('Writing csv files')
season_df.to_csv('Understat_EPL_Player_Data_Season.csv', encoding='utf-8', index=False)
three_game_df.to_csv('Understat_EPL_Player_Data_3Game.csv', encoding='utf-8', index=False)
five_game_df.to_csv('Understat_EPL_Player_Data_5Game.csv', encoding='utf-8', index=False)
ten_game_df.to_csv('Understat_EPL_Player_Data_10Game.csv', encoding='utf-8', index=False)