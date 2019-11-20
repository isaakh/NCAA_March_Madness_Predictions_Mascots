import json
from bs4 import BeautifulSoup
import sqlite3
import http.client
import matplotlib.pyplot as plt
import csv

api_key = "k9qdkxn79vg4jh7xrd4whkef"

# -- Create a connection to Sportradar and request data from a given link using the API key.
conn = http.client.HTTPSConnection("api.sportradar.us")
conn.request("GET", "/ncaamb/trial/v4/en/seasons/2018/reg/standings.xml?api_key={}".format(api_key))
res = conn.getresponse()

# -- Read the response from the API request and decode it.
data = res.read()
data2 = data.decode("utf-8")

# -- Open the mascots.csv file, turn it into a reader object, and add all the
# NCAA teams into a list (including D1, D2, and D3 teams).
team_list = []
infile = open('mascots.csv', 'r')
reader = csv.reader(infile, delimiter = ',')
for row in reader:
    team_list.append(row[2])
infile.close()

# -- Use BeautifulSoup to parse the XML response and create a list of all D1 teams only.
data3 = BeautifulSoup(data2, features='xml')
teams = data3.find_all('team')
d1_teams = []
for team in teams:
    market = team.get('market')
    if market in team_list:
        d1_teams.append(team)


# -- Create a list of lists, with each sub-list containing each D1 team's
# name, # of wins, and # of losses.
json_team_list = []
for t in d1_teams:
    tName = t.get('market') + ' ' + t.get('name')
    tWins = t.get('wins')
    tLosses = t.get('losses')
    json_team_list.append([tName, int(tWins), int(tLosses)])


# -- Caches the list of lists into a JSON file which can be used later
# (as opposed to having to make another request to Sportradar).
team_cache = json.dumps(json_team_list)
infile2 = open('NCAA_teams.json', 'w')
infile2.write(team_cache)
infile2.close()


# -- Load the cache file, set up and create the SQLite file, and insert the data
# in the cache file into it.
cache_file = open('NCAA_teams.json', 'r')
cache_data = cache_file.read()
cache_list = json.loads(cache_data)
cache_file.close()
conn = sqlite3.connect('NCAA_teams.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Teams (name TEXT, wins INTEGER, losses INTEGER)')
for t in cache_list:
    cur.execute('INSERT INTO Teams (name, wins, losses) VALUES (?, ?, ?)', (t[0], t[1], t[2]))
    conn.commit()
