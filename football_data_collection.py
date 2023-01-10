from data_collection_tools import *

year='2022'
leagues = [('1', 'nfl'), ('2', 'ncaaf')]
for league_id, league_name in leagues:
    football_data_collection(league_id, league_name, year)
