import datetime
from datetime import datetime
import csv
from data_collection_tools import game_row
import time
from etext import send_sms_via_email #https://github.com/AlfredoSequeida/etext
import os

def get_all_team_names():
    leagues = ['nba', 'nfl']
    all_info = []
    for league in leagues:
        # Path to the directory
        directory = f'{league}_api_data'
        # Create an empty list to store the filenames
        filenames = []
        # Use the os.listdir function to get a list of all the files in the directory
        for file in os.listdir(directory):
            # Check if the file is a file (not a directory)
            if os.path.isfile(os.path.join(directory, file)):
                # Add the filename to the list
                filenames.append(file)
        filenames.remove('.DS_Store')
        for i in range(len(filenames)):
            file = filenames[i]
            file = " ".join(file.split('.')[0].split("-"))
            filenames[i] = file
        all_info.append(filenames)
        # The filenames are now stored in the filenames list
    return all_info

def search_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        # Create a CSV reader object
        reader = csv.reader(file)
        # Skip the header row
        next(reader)        
        # Iterate over the rows in the file
        for row in reader:
            # Convert each value to a float and append it to the data list
            data.append([x for x in row])
        file.close()
    return data

def find_files(name, path):
    matching_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == name:
                subfolder = root.replace(path, '')
                matching_files.append((subfolder, file))
    return matching_files

def get_all_data(teams):
    all_rows = []
    for league_input, team_input in teams:
        team_name = "-".join(team_input.split(" "))
        league_name = "-".join(league_input.split(" "))
        # files = find_files(f'{team_name}.csv', 'data/')
        csv_data = search_csv(f'data/{league_name}_api_data/{team_name}.csv')
        for each_game in csv_data:
            curr = game_row()
            curr.normal_date, curr.team, curr.opponent, curr.score, curr.result, curr.home_or_away, curr.date_time_unix, curr.image= each_game
            all_rows.append(curr)
    return all_rows

def convert_to_cap(word):
    w = word.split(" ")
    for ind, i in enumerate(w):
        w[ind] = i[0:1].upper() + i[1:]
    return " ".join(w)

def text_number(message, number, provider, days):
    number = "3312296253"
    message = '\n' +'\n' + '\n' + message

    sender_credentials = ("upcomingsportsgames@gmail.com", "qjbkmtchztfawqhc")
    print(message)
    send_sms_via_email(number, message, provider, sender_credentials, subject=f'Sports over the next {days} days')

def text_about_updates(provider, my_teams = [], number = "", days = 4):
    #take input
    check = True
    if number == "":
        number = input("Enter your phone number: ")
        number = number.replace("-", "")
    if my_teams == []:
        while check:
            league = input("Enter the League your team is in: ").lower()
            team = input("Enter your Team: ").lower()
            my_teams.append((league, team))
            decision = input("Would you like to enter another team? (y/n): ")
            decision = True if decision.lower() == 'y' else False
            if not decision:
                check = False
    #parse input
    my_team_data = get_all_data(my_teams)
    now = float(time.time())
    times = [float(i.date_time_unix) - now for i in my_team_data]
    finalList = []
    message = ''
    message+=''
    for ind, i in enumerate(times):
        if i <= 86400*days and i>=0: #8640 seconds in a day
            finalList.append(my_team_data[ind])
    for each_team in finalList:
        team_name, opponent_name = convert_to_cap(each_team.team), convert_to_cap(each_team.opponent)
        date = datetime.fromtimestamp(float(each_team.date_time_unix))
        formatted_date = date.strftime("%A, %B %d %I:%M %p")
        format_game = f'{team_name} @ {opponent_name}' if each_team.home_or_away == 'away' else f'{opponent_name} @ {team_name}' 
        message+=format_game
        message+='\n'
        message+=f'{formatted_date}'
        message+='\n\n'
    text_number(message, number, provider, days)
    
if __name__ == "__main__":
    text_about_updates(my_teams = [("premier league", "arsenal"), ("uefa europa league", "arsenal"), ("fa cup", "arsenal"), ("international", "usa"), ("nba", "golden state warriors"), ("nfl", "san francisco 49ers"), ("ncaaf", "illinois"), ("ncaamb", "illinois")], number = "3312296253", days = 5, provider = 'T-Mobile')


#~/opt/anaconda3/envs/text_myself/bin/python3 ~/Desktop/text_myself/text_myself_api.py
