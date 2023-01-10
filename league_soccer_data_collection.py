from data_collection_tools import *

year = '2022'
league_ids=[2, 39, 140, 253, 61, 78, 45, 3]
# uefa champions league, premier league, la liga, MLS, Ligue 1, Bundesliga, FA Cup, uefa Europa League
num_leagues_before_international = 0
#change this if you add more leagues before the international teams
league_soccer_data_collection(league_ids, year) 