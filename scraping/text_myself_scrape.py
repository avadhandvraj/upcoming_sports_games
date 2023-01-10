import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from twilio.rest import Client
import arsenal_scrape, niners_scrape, warriors_scrape, illinoisbball_scrape
from datetime import datetime
import csv
from nba_scrape import nba_game_row
from nfl_scrape import nfl_game_row
import time

nba_teams1 = {'atlanta hawks': 'hawks', 'boston celtics': 'celtics', 'brooklyn nets': 'nets', 'charlotte hornets': 'hornets', 'chicago bulls': 'bulls', 'cleveland cavaliers': 'cavaliers', 'dallas mavericks': 'mavericks', 'denver nuggets': 'nuggets', 'detroit pistons': 'pistons', 'golden state warriors': 'warriors', 'houston rockets': 'rockets', 'indiana pacers': 'pacers', 'los angeles clippers': 'clippers', 'los angeles lakers': 'lakers', 'memphis grizzlies': 'grizzlies', 'miami heat': 'heat', 'milwaukee bucks': 'bucks', 'minnesota timberwolves': 'timberwolves', 'new orleans pelicans': 'pelicans', 'new york knicks': 'knicks', 'oklahoma city thunder': 'thunder', 'orlando magic': 'magic', 'philadelphia 76ers': '76ers', 'phoenix suns': 'suns', 'portland trail blazers': 'trail blazers', 'sacramento kings': 'kings', 'san antonio spurs': 'spurs', 'toronto raptors': 'raptors', 'utah jazz': 'jazz', 'washington wizards': 'wizards'}
nba_teams2={'hawks': 'atlanta hawks', 'celtics': 'boston celtics', 'nets': 'brooklyn nets', 'hornets': 'charlotte hornets', 'bulls': 'chicago bulls', 'cavaliers': 'cleveland cavaliers', 'mavericks': 'dallas mavericks', 'nuggets': 'denver nuggets', 'pistons': 'detroit pistons', 'warriors': 'golden state warriors', 'rockets': 'houston rockets', 'pacers': 'indiana pacers', 'clippers': 'los angeles clippers', 'lakers': 'los angeles lakers', 'grizzlies': 'memphis grizzlies', 'heat': 'miami heat', 'bucks': 'milwaukee bucks', 'timberwolves': 'minnesota timberwolves', 'pelicans': 'new orleans pelicans', 'knicks': 'new york knicks', 'thunder': 'oklahoma city thunder', 'magic': 'orlando magic', '76ers': 'philadelphia 76ers', 'suns': 'phoenix suns', 'trail blazers': 'portland trail blazers', 'kings': 'sacramento kings', 'spurs': 'san antonio spurs', 'raptors': 'toronto raptors', 'jazz': 'utah jazz', 'wizards': 'washington wizards'}
nfl_teams1 = {'new york jets': 'jets', 'new york giants': 'giants', 'los angeles chargers': 'chargers', 'los angeles rams': 'rams', 'chicago bears': 'bears', 'houston texans': 'texans', 'philadelphia eagles': 'eagles', 'dallas cowboys': 'cowboys', 'jacksonville jaguars': 'jaguars', 'san francisco 49ers': '49ers', 'indianapolis colts': 'colts', 'seattle seahawks': 'seahawks', 'denver broncos': 'broncos', 'washington commanders': 'commanders', 'detroit lions': 'lions', 'las vegas raiders': 'raiders', 'baltimore ravens': 'ravens', 'atlanta falcons': 'falcons', 'new orleans saints': 'saints', 'miami dolphins': 'dolphins', 'cincinnati bengals': 'bengals', 'pittsburgh steelers': 'steelers', 'tampa bay buccaneers': 'buccaneers', 'kansas city chiefs': 'chiefs', 'tennessee titans': 'titans', 'carolina panthers': 'panthers', 'arizona cardinals': 'cardinals', 'new england patriots': 'patriots', 'green bay packers': 'packers', 'buffalo bills': 'bills', 'cleveland browns': 'browns', 'minnesota vikings': 'vikings'}
nfl_teams2={'jets': 'new york jets', 'giants': 'new york giants', 'chargers': 'los angeles chargers', 'rams': 'los angeles rams', 'bears': 'chicago bears', 'texans': 'houston texans', 'eagles': 'philadelphia eagles', 'cowboys': 'dallas cowboys', 'jaguars': 'jacksonville jaguars', '49ers': 'san francisco 49ers', 'colts': 'indianapolis colts', 'seahawks': 'seattle seahawks', 'broncos': 'denver broncos', 'commanders': 'washington commanders', 'lions': 'detroit lions', 'raiders': 'las vegas raiders', 'ravens': 'baltimore ravens', 'falcons': 'atlanta falcons', 'saints': 'new orleans saints', 'dolphins': 'miami dolphins', 'bengals': 'cincinnati bengals', 'steelers': 'pittsburgh steelers', 'buccaneers': 'tampa bay buccaneers', 'chiefs': 'kansas city chiefs', 'titans': 'tennessee titans', 'panthers': 'carolina panthers', 'cardinals': 'arizona cardinals', 'patriots': 'new england patriots', 'packers': 'green bay packers', 'bills': 'buffalo bills', 'browns': 'cleveland browns', 'vikings': 'minnesota vikings'}

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

def get_all_data(teams):
    all_rows = []
    for short, long in teams:
        sport = ''
        if long in nba_teams1:
            sport = 'nba'
            data = search_csv(f'{sport}_data_espn/{short}.csv')
            for each_game in data:
                curr = nba_game_row()
                curr.normal_date, curr.team, curr.score, curr.result, curr.home_or_away, curr.date_time_unix = each_game
                all_rows.append((curr, long))
        elif long in nfl_teams1:
            sport = 'nfl'
            data = search_csv(f'{sport}_data_espn/{short}.csv')
            for each_game in data:
                curr = nfl_game_row()
                curr.normal_date, curr.team, curr.score, curr.week, curr.result, curr.home_or_away, curr.date_time_unix = each_game
                all_rows.append((curr, long))
    return all_rows

#take input
check = True
my_teams = []
number = input("Enter your phone number: ")
number = number.replace("-", "")
while check:
    decision = input("Would you like to enter another team? (y/n)")
    decision = True if decision == 'y' else False
    if not decision:
        check = False
    else:
        team = input("Enter Team: ")
        my_teams.append(team)

#parse input
my_teams = [i.lower() for i in my_teams]
teams = []
for i in my_teams:
    if i in nba_teams1:
        teams.append((nba_teams1[i], i))
    elif i in nba_teams2:
        teams.append((i, nba_teams2[i]))
    elif i in nfl_teams1:
        teams.append((nfl_teams1[i], i))
    elif i in nfl_teams2:
        teams.append((i, nfl_teams2[i]))
my_team_data = get_all_data(teams)
my_team_data = [(i, j) for i, j in my_team_data if i.date_time_unix!=""]
now = float(time.time())
times = [float(i.date_time_unix) - now for i, _ in my_team_data]
finalList = []
ret = 'Sports Updates:\n\n'
for ind, i in enumerate(times):
    if i <= 432000 and i>=0:
        finalList.append(my_team_data[ind])
for i, team in finalList:
    date = i.normal_date.split(" ")
    ret+=f'{team} are playing {i.team}'
    ret+='\n'
    ret+=f'{date[0]} {date[1]} {date[2]} at {date[4]} {date[5]}'
    ret+='\n\n'
# Your Twilio credentials
account_sid = 'AC79f5c4e075b511c9db23ae9ea3881384'
auth_token = '83f97935aecf61a79db0e1c4437342da'

# Create a scheduler
scheduler = BlockingScheduler()

# Define the function that will be run every 24 hours
def run_script():
    print(f'Script run at {datetime.now()}')
    # Run your script here
    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Send the text message
    message = client.messages.create(
    body=ret,
    from_='+19716063724',
    to=f'+1{number}'
    )

    print(ret)

# Schedule the function to run every 24 hours
scheduler.add_job(run_script, 'interval', seconds=10)

# Start the scheduler
scheduler.start()

