import os
import re
import csv 
import json
import collections
from collections import defaultdict
from datetime import datetime
import requests
import PIL
from PIL import Image
import requests
from io import BytesIO

class game_row():
    def __init__(self, team="", opponent = "", home_or_away="", score="", date_time_unix="", result="", normal_date = "", image=""):
        self.team = team
        self.opponent = opponent
        self.home_or_away = home_or_away
        self.score = score
        self.date_time_unix = date_time_unix
        self.result = result
        self.normal_date = normal_date
        self.image = image

    def turn_to_array(self):
        return [self.normal_date, self.team, self.opponent, self.score, self.result, self.home_or_away, self.date_time_unix, self.image]

def international_soccer_data_collection(league_ids, year):
    key = '8761add519b3bd6803a73cceea02f369'
    league_name = 'international'
    international_data = defaultdict(list)
    delete_files(league_name)
    for id in league_ids:
        link = f'https://v3.football.api-sports.io/fixtures?team={id}&season={year}'
        headers = {
            "x-rapidapi-key": key
        }
        response1 = requests.request("GET", link, headers=headers)
        quote1 = json.loads(response1.text)
        for i in quote1['response']:
            home = game_row()
            away = game_row()        
            homeName, homeImageUrl = i['teams']['home']['name'].lower(), i['teams']['home']['logo'] 
            awayName, awayImageUrl = i['teams']['away']['name'].lower(), i['teams']['away']['logo'] 
            home.team, home.opponent, home.home_or_away, home.date_time_unix, home.image = homeName, awayName, 'home', i['fixture']['timestamp'], homeImageUrl
            away.team, away.opponent, away.home_or_away, away.date_time_unix, away.image = awayName, homeName, 'away', i['fixture']['timestamp'], awayImageUrl
            date = datetime.fromtimestamp(float(home.date_time_unix))
            formatted_date = date.strftime("%A, %B %d %I:%M %p")
            home.normal_date, away.normal_date = formatted_date, formatted_date
            if i['fixture']['status']['long']!='Not Started' and i['fixture']['status']['long']!=None and i['goals']['home']!=None:
                home_result, away_result, score = '', '', ''
                home_total, away_total = int(i['goals']['home']), int(i['goals']['away'])
                if home_total == away_total:
                    if i['score']['extratime']['home'] == None or i['score']['penalty']['home'] == None:
                        score = f'{away_total} - {home_total}'
                        home_result, away_result = 'tie', 'tie'
                    else:
                        home_pk, away_pk = int(i['score']['penalty']['home']), int(i['score']['penalty']['away'])
                        score = f'{away_total}({away_pk}) - {home_total}({home_pk})'
                        home_result, away_result = 'W' if home_pk>away_pk else 'L', 'W' if home_pk<away_pk else 'L'
                else:
                    score = f'{away_total} - {home_total}'
                    if i['score']['extratime']['home'] != None:
                        score+=" ET"
                    home_result, away_result = 'W' if home_total>away_total else 'L', 'W' if home_total<away_total else 'L'
                home.score, away.score = score, score
                home.result, away.result = home_result, away_result
            if not does_game_row_already_exist(home, international_data[home.team]):
                international_data[home.team].append(home)
            if not does_game_row_already_exist(away, international_data[away.team]):
                international_data[away.team].append(away)
        
    for team_name, game_rows in international_data.items():
        write_csv(team_name, game_rows, league_name)
        save_image(team_name, game_rows, league_name)
        
def does_game_row_already_exist(game_row, game_rows):
    for i in game_rows:
        if game_row.date_time_unix == i.date_time_unix:
            return True
    return False
    
def league_soccer_data_collection(league_ids, year):
    key = '8761add519b3bd6803a73cceea02f369'
    for id in league_ids:
        league_data = defaultdict(list)
        link = f'https://v3.football.api-sports.io/fixtures?league={id}&season={year}'
        headers = {
            "x-rapidapi-key": key
        }
        print(id)
        response1 = requests.request("GET", link, headers=headers)
        quote1 = json.loads(response1.text)
        league_name = quote1['response'][0]['league']['name'].lower() 
        #Change numleages to the number of leagues you have if you add more leagues/tournaments before the international teams
        league_name = "-".join(league_name.split(" ")).lower()
        delete_files(league_name)
        for i in quote1['response']:
            home = game_row()
            away = game_row()        
            homeName, homeImageUrl = i['teams']['home']['name'].lower(), i['teams']['home']['logo'] 
            awayName, awayImageUrl = i['teams']['away']['name'].lower(), i['teams']['away']['logo'] 
            home.team, home.opponent, home.home_or_away, home.date_time_unix, home.image = homeName, awayName, 'home', i['fixture']['timestamp'], homeImageUrl
            away.team, away.opponent, away.home_or_away, away.date_time_unix, away.image = awayName, homeName, 'away', i['fixture']['timestamp'], awayImageUrl
            date = datetime.fromtimestamp(float(home.date_time_unix))
            formatted_date = date.strftime("%A, %B %d %I:%M %p")
            home.normal_date, away.normal_date = formatted_date, formatted_date
            if i['fixture']['status']['long']!='Not Started' and i['fixture']['status']['long']!=None and i['goals']['home']!=None:
                home_result, away_result, score = '', '', ''
                home_total, away_total = int(i['goals']['home']), int(i['goals']['away'])
                if home_total == away_total:
                    if i['score']['extratime']['home'] == None or i['score']['penalty']['home'] == None:
                        score = f'{away_total} - {home_total}'
                        home_result, away_result = 'tie', 'tie'
                    else:
                        home_pk, away_pk = int(i['score']['penalty']['home']), int(i['score']['penalty']['away'])
                        score = f'{away_total}({away_pk}) - {home_total}({home_pk})'
                        home_result, away_result = 'W' if home_pk>away_pk else 'L', 'W' if home_pk<away_pk else 'L'
                else:
                    score = f'{away_total} - {home_total}'
                    if i['score']['extratime']['home'] != None:
                        score+=" ET"
                    home_result, away_result = 'W' if home_total>away_total else 'L', 'W' if home_total<away_total else 'L'
                home.score, away.score = score, score
                home.result, away.result = home_result, away_result
            league_data[home.team].append(home)
            league_data[away.team].append(away)
        
        for team_name, game_rows in league_data.items():
            write_csv(team_name, game_rows, league_name)
            save_image(team_name, game_rows, league_name)
        
def basketball_data_collection(league_id, league_name, year):
    league_name = "-".join(league_name.split(" ")).lower()
    college_teams = defaultdict(list)
    key = '8761add519b3bd6803a73cceea02f369'
    link = f'https://v1.basketball.api-sports.io/games?league={league_id}&season={year}'
    headers = {
        "x-rapidapi-key": key
    }
    response1 = requests.request("GET", link, headers=headers)
    quote1 = json.loads(response1.text)
    for i in quote1['response']:
        home = game_row()
        away = game_row()        
        homeName, homeImageUrl = i['teams']['home']['name'].lower(), i['teams']['home']['logo']
        awayName, awayImageUrl = i['teams']['away']['name'].lower(), i['teams']['away']['logo']
        home.team, home.opponent, home.home_or_away, home.date_time_unix, home.normal_date, home.image = homeName, awayName, 'home', i['timestamp'], i['date'], homeImageUrl
        away.team, away.opponent, away.home_or_away, away.date_time_unix, away.normal_date, away.image = awayName, homeName, 'away', i['timestamp'], i['date'], awayImageUrl
        if i['status']['long']!='Not Started' and i['status']['long']!=None:
            awayScore, homeScore = i['scores']['away']['total'], i['scores']['home']['total']
            score = str(awayScore) + ' - ' + str(homeScore)
            home.score, away.score = score, score
            if homeScore == awayScore:
                home.result, away.result = "tie", 'tie'
            elif homeScore > awayScore:
                home.result, away.result = "W", "L"
            elif homeScore < awayScore:
                home.result, away.result = "L", "W"
        college_teams[home.team].append(home)
        college_teams[away.team].append(away)

    delete_files(league_name)
    for team_name, game_rows in college_teams.items():
        write_csv(team_name, game_rows, league_name)
        save_image(team_name, game_rows, league_name)

def football_data_collection(league_id, league_name, year):
    league_name = "-".join(league_name.split(" ")).lower()
    football_teams = defaultdict(list)
    allowed_stages = {'Regular Season', 'Pre Season', 'FBS (Division I-A)', 'FCS (Division I-AA)'}
    key = '8761add519b3bd6803a73cceea02f369'
    link = f'https://v1.american-football.api-sports.io/games?league={league_id}&season={year}'
    headers = {
        "x-rapidapi-key": key
    }
    response1 = requests.request("GET", link, headers=headers)
    quote1 = json.loads(response1.text)
    for i in quote1['response']:
        if i['game']['stage'] in allowed_stages and i['teams']['home']['name']!=None:
            home = game_row()
            away = game_row()        
            homeName, homeImageUrl = i['teams']['home']['name'].lower(), i['teams']['home']['logo'] 
            awayName, awayImageUrl = i['teams']['away']['name'].lower(), i['teams']['away']['logo']
            home.team, home.opponent, home.home_or_away, home.date_time_unix, home.normal_date, home.image = homeName, awayName, 'home', i['game']['date']['timestamp'], i['game']['date']['date'], homeImageUrl
            away.team, away.opponent, away.home_or_away, away.date_time_unix, away.normal_date, away.image = awayName, homeName, 'away', i['game']['date']['timestamp'], i['game']['date']['date'], awayImageUrl
            if i['game']['status']['long']!='Not Started' and i['game']['status']['long']!=None:
                awayScore, homeScore = i['scores']['away']['total'], i['scores']['home']['total']
                score = str(awayScore) + ' - ' + str(homeScore)
                home.score, away.score = score, score
                if homeScore == awayScore:
                    home.result, away.result = "tie", 'tie'
                elif homeScore > awayScore:
                    home.result, away.result = "W", "L"
                elif homeScore < awayScore:
                    home.result, away.result = "L", "W"
            football_teams[home.team].append(home)
            football_teams[away.team].append(away)

    delete_files(league_name)
    for team_name, game_rows in football_teams.items():
        write_csv(team_name, game_rows, league_name)
        save_image(team_name, game_rows, league_name)

def delete_files(league):
    folder_path = f'data/{league}_api_data'
    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Iterate over the list of files
    for file in files:
        # Construct the full file path
        file_path = os.path.join(folder_path, file)

        # Check if the file is a regular file (not a directory)
        if os.path.isfile(file_path):
            # Delete the file
            os.unlink(file_path)

def write_csv(team_name, game_rows, league_name):
    team_name = re.sub(r'[^A-Za-z0-9]', '-', team_name)
    league_name = "-".join(league_name.split(" ")).lower()
    for i in range(len(team_name)):
        if team_name[i] == '-':
            continue
        if not team_name[i].isalnum(): 
            team_name = team_name[:i] + "-" + team_name[i+1:]
    # Check if the CSV file exists
    if not os.path.exists(f'data/{league_name}_api_data/{team_name}.csv'):
        # The file does not exist, so create it
        f = open(f'data/{league_name}_api_data/{team_name}.csv', 'w')
        writer = csv.writer(f)
        writer.writerow(['Date', 'Team', 'Opponent','Score', 'Result', 'Home or Away', 'Unix Timestamp', "Image Url"])
        f.close()

    # Open the CSV file in append mode
    f = open(f'data/{league_name}_api_data/{team_name}.csv', 'a')

    # Create a writer object
    writer = csv.writer(f)

    # Write some rows of data to the CSV file
    
    for game in game_rows:
        writer.writerow(game.turn_to_array())  

    # Close the CSV file
    f.close()

def save_image(team_name, game_rows, league_name):
    # Get the image from the URL
    imageUrl = game_rows[0].image
    team_name = re.sub(r'[^A-Za-z0-9]', '-', team_name)
    league_name = "-".join(league_name.split(" ")).lower()

    # Save the image to a file
    path = f'data/{league_name}_api_data/images/{team_name}.png'
    if not os.path.exists(path) and is_image_url(imageUrl):
        # Save the image to the file
        response = requests.get(imageUrl)
        # Open the image as a PIL Image object
        image = Image.open(BytesIO(response.content))
        image.save(path)

def is_image_url(url):
    # Send a HEAD request to the URL
    response = requests.head(url)

    # Check the "Content-Type" header of the response
    if response.headers.get("Content-Type").startswith("image"):
        # The URL is a valid image URL
        return True
    else:
        # The URL is not a valid image URL
        return False
