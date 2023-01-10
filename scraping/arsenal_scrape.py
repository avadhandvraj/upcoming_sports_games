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

def get_arsenal_data():
    time.sleep(1) 
    website = 'https://www.espn.com/soccer/team/results/_/id/359/eng.arsenal'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(website) 
    time.sleep(1) 
    matches = driver.find_elements(By.CLASS_NAME, 'Table__TD')
    days = ["Mon,", "Tue,", "Wed,", "Thu,", "Fri,", "Sat,", "Sun,"]
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    matches = [i.text for i in matches]
    time.sleep(1)
    driver.quit()
    time.sleep(1)
    website2 = 'https://www.espn.com/soccer/team/fixtures/_/id/359/eng.arsenal'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(website2) 
    time.sleep(1)
    matches = matches + [i.text for i in driver.find_elements(By.CLASS_NAME, 'Table__TD')]
    # print(matches)
    game_rows = []
    for ind, i in enumerate(matches):
        lines = i.split("\n")
        i = " ".join(lines)
        matches[ind]=i
    for i, j in enumerate(matches):
        if j.split(' ')[0] in days:
            curr = game_row()
            curr.normal_date = matches[i] + " 2023" if  matches[i].split(' ')[1] in months else matches[i] + " 2022" 
            struct_time = strptime(curr.normal_date, "%a, %b %d %Y")
            timestamp = mktime(struct_time)
            curr.date_time_unix = timestamp
            curr.team = matches[i+1] if matches[i+1]!="Arsenal" else matches[i+3]
            curr.home_or_away = "Away" if matches[i+1]!="Arsenal" else "Home"
            if ('PM' in matches[i+4] or 'AM' in matches[i+4]):
                curr.normal_date = curr.normal_date +" "+ str(matches[i+4])
                struct_time = strptime(curr.normal_date, "%a, %b %d %Y %I:%M %p")
                timestamp = mktime(struct_time)
                curr.date_time_unix = timestamp
            else:
                temp =  matches[i+2].split(" ")
                home, away = temp[0], temp[2]
                if int(home) == int(away):
                    curr.result = "Tie"
                elif (int(home) > int(away) and curr.home_or_away == 'Home') or (int(away)>int(home) and curr.home_or_away == 'Away'):
                    curr.result = "W"
                else:
                    curr.result = "L"
                curr.score = '`' + str(matches[i+2])
            game_rows.append(curr)
    game_rows.sort(key=lambda x: x.date_time_unix)
    with open("arsenalData.csv", "w") as l:
        writer = csv.writer(l)
        writer.writerow(['Date', 'Team', 'Score', 'Result', 'Home or Away', 'Unix Timestamp'])
        for game in game_rows:
            writer.writerow(game.turn_to_array())       
        l.close()
    driver.quit()
    return game_rows