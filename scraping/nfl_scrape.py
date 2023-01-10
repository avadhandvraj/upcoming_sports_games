from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import time
from time import mktime, strptime

class nfl_game_row():
    def __init__(self, week="", team="", home_or_away="", score="", date_time_unix="", result="", normal_date = ""):
        self.week = week
        self.team = team
        self.home_or_away = home_or_away
        self.score = score
        self.date_time_unix = date_time_unix
        self.result = result
        self.normal_date = normal_date
    
    def turn_to_array(self):
        return [self.normal_date, self.team, self.score, self.week, self.result, self.home_or_away, self.date_time_unix]

def get_nfl_espn_data(city_abbr, team_name):
    time.sleep(1) 
    website = f'https://www.espn.com/nfl/team/schedule/_/name/{city_abbr}'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(website) 
    time.sleep(1) 
    matches = driver.find_elements(By.CLASS_NAME, 'Table__TD')
    weeknums = [str(i) for i in range(18)]
    matches = [i.text for i in matches]
    game_rows = []
    for i, j in enumerate(matches):
        if j in weeknums:
            curr = nfl_game_row()
            curr.normal_date = str(matches[i+1])
            curr.week = str(matches[i])
            curr.team = matches[i+2][2:] if matches[i+2][0]=='@' else matches[i+2][3:]
            if curr.team == "":
                game_rows.append(curr)
                continue
            curr.home_or_away = "Away" if matches[i+2][0]=='@' else "Home"
            if ('PM' in matches[i+3] or 'AM' in matches[i+3]):
                curr.normal_date = curr.normal_date + " 2023 " + str(matches[i+3]) if curr.normal_date.split(' ')[1] in ['Jan, Feb'] else curr.normal_date + " 2022 " + str(matches[i+3])
                struct_time = strptime(curr.normal_date, "%a, %b %d %Y %I:%M %p")
                timestamp = mktime(struct_time)
                curr.date_time_unix = timestamp
            else:
                curr.result = str(matches[i+3][0])
                curr.score = '`' + str(matches[i+3][1:])
            game_rows.append(curr)
    game_rows.sort(key = lambda x: int(x.week))
    with open(f'nfl_data/{team_name}.csv', "w") as l:
        writer = csv.writer(l)
        writer.writerow(['Date', 'Team', 'Score', 'Week', 'Result', 'Home or Away', 'Unix Timestamp'])
        for game in game_rows:
            writer.writerow(game.turn_to_array())       
        l.close()
    driver.quit()
    return game_rows

def main():
    nfl_teams = {'new york jets': 'nyj', 'new york giants': 'nyg', 'los angeles chargers': 'lac', 'los angeles rams': 'lar','chicago bears': 'chi', 'houston texans': 'hou', 'philadelphia eagles': 'phi', 'dallas cowboys': 'dal', 'jacksonville jaguars': 'jax', 'san francisco 49ers': 'sf', 'indianapolis colts': 'ind', 'seattle seahawks': 'sea', 'denver broncos': 'den', 'washington commanders': 'wsh', 'detroit lions': 'det', 'las vegas raiders': 'lv', 'baltimore ravens': 'bal', 'atlanta falcons': 'atl', 'new orleans saints': 'no', 'miami dolphins': 'mia', 'cincinnati bengals': 'cin', 'pittsburgh steelers': 'pit', 'tampa bay buccaneers': 'tb', 'kansas city chiefs': 'kc', 'tennessee titans': 'ten', 'carolina panthers': 'car', 'arizona cardinals': 'ari', 'new england patriots': 'ne', 'green bay packers': 'gb', 'buffalo bills': 'buf', 'cleveland browns': 'cle', 'minnesota vikings': 'min'}
    for k,v in nfl_teams.items():
        get_nfl_espn_data(v, k.split(' ')[-1])