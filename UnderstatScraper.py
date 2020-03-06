#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 1 17:50:36 2020

@author: doug hagey
"""

import pandas as pd
import requests

def scrape_understat(payload):
    #Build request using url, headers (mimicking what Firefox does normally)
    #Works best with verify=True as you won't get the ssl errors. Payload is 
    #taylored for each request
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

def clean_df(player_df, weeks):
    # Get rid of the columns that we don't care about
    #player_df.drop(['yellow_cards','red_cards', 'xGChain','xGBuildup','games','time'], axis=1, inplace=True)
    player_df  = player_df.rename(columns={'goals':'goals_'+weeks,'xG':'xG_'+weeks,'assists':'assists_'+weeks, 'xA':'xA_'+weeks, 'shots':'shots_'+weeks, 'key_passes':
        'key_passes_'+weeks,'npg':'npg_'+weeks,'npxG':'npxG_'+weeks})
    if weeks != '3wks':
        player_df.drop(['position','team_title'], axis=1, inplace=True)
    return(player_df)

#Create Pandas dataframes from each html table
print('Getting data for last 3 matches')
json_player_data = scrape_understat({'league':'EPL', 'season':'2019', 'n_last_matches': '3'})
three_game_table = pd.DataFrame(json_player_data)
three_game_df = clean_df(three_game_table,'3wks')
#Replace Position indentifiers with something more useful
three_game_df['position'] = three_game_df['position'].str.slice(0,1)
position_map = {'D':'DEF', 'F':'FWD', 'M':'MID', 'G':'GK', 'S':'FWD'}
three_game_df = three_game_df.replace({'position': position_map})


print('Getting data for the whole season')
json_player_data = scrape_understat({'league':'EPL', 'season':'2019'})
season_table = pd.DataFrame(json_player_data)
season_df = clean_df(season_table, 'season')

print('Getting data for last 5 matches')
json_player_data = scrape_understat({'league':'EPL', 'season':'2019', 'n_last_matches': '5'})
five_game_table = pd.DataFrame(json_player_data)
five_game_df = clean_df(five_game_table, '5wks')

print('Getting data for last 10 matches')
json_player_data = scrape_understat({'league':'EPL', 'season':'2019', 'n_last_matches': '10'})
ten_game_table = pd.DataFrame(json_player_data)
ten_game_df = clean_df(ten_game_table, '10wks')

print('Merging Tables')
EPL_player_df = pd.merge(three_game_df, season_df, on=['id','player_name'])
EPL_player_df = pd.merge(EPL_player_df, five_game_df, on=['id','player_name'])
EPL_player_df = pd.merge(EPL_player_df, ten_game_df, on=['id','player_name'])

print('Writing CSV File')
EPL_player_df.to_csv('Understat_EPL_Player_Data_Combined.csv', encoding='utf-8', index=False)
