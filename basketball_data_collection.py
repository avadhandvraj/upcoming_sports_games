from data_collection_tools import *

year='2022-2023'
leagues = [('12', 'nba'), ('116', 'ncaamb')]
for league_id, league_name in leagues:
    basketball_data_collection(league_id, league_name, year)