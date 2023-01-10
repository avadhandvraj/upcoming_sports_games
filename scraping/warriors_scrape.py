from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import time
from time import mktime, strptime

class game_row():
    def __init__(self, team="", home_or_away="", score="", date_time_unix="", result="", normal_date = ""):
        self.team = team
        self.home_or_away = home_or_away
        self.score = score
        self.date_time_unix = date_time_unix
        self.result = result
        self.normal_date = normal_date
    
    def turn_to_array(self):
        return [self.normal_date, self.team, self.score, self.result, self.home_or_away, self.date_time_unix]

def get_warriors_data():
    time.sleep(1) 
    website = 'https://www.espn.com/nba/team/schedule/_/name/gs/golden-state-warriors'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(website) 
    time.sleep(1) 
    matches = driver.find_elements(By.CLASS_NAME, 'Table__TD')
    days = ["Mon,", "Tue,", "Wed,", "Thu,", "Fri,", "Sat,", "Sun,"]
    matches = [i.text for i in matches]
    game_rows = []
    for i, j in enumerate(matches):
        if j.split(' ')[0] in days:
            curr = game_row()
            curr.normal_date = str(matches[i])
            curr.team = matches[i+1][2:] if matches[i+1][0]=='@' else matches[i+1][3:]
            curr.home_or_away = "Away" if matches[i+1][0]=='@' else "Home"
            if ('PM' in matches[i+2] or 'AM' in matches[i+2]):
                curr.normal_date = curr.normal_date + " 2023 " + str(matches[i+2]) if curr.normal_date.split(' ')[1] in ['Jan', 'Feb', 'Mar', 'Apr'] else curr.normal_date + " 2022 " + str(matches[i+2])
                struct_time = strptime(curr.normal_date, "%a, %b %d %Y %I:%M %p")
                timestamp = mktime(struct_time)
                curr.date_time_unix = timestamp
            else:
                curr.result = str(matches[i+2][0])
                curr.score = '`' + str(matches[i+2][1:])
            game_rows.append(curr)
    with open("WarriorsData.csv", "w") as l:
        writer = csv.writer(l)
        writer.writerow(['Date', 'Team', 'Score', 'Result', 'Home or Away', 'Unix Timestamp'])
        for game in game_rows:
            writer.writerow(game.turn_to_array())       
        l.close()
    driver.quit()
    return game_rows
