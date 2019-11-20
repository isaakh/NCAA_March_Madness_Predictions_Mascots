import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# -- Read the mascots.csv file into a pandas DataFrame object.
mascots = pd.read_csv('mascots.csv')

# -- Change the columns of the DataFrame into ones that we can work with more easily.
mascots.columns = ['unamed', 'id', 'market', 'name_half', 'mascot', 'mascot_name', 'mascot_common_name', 'tax_subspecies', 'tax_species', 'tax_genus', 'tax_family', 'tax_order', 'tax_class', 'tax_phylum', 'tax_kingdom', 'tax_domain', 'non_tax_type']
mascots['name'] = mascots['market'] + ' ' + mascots['name_half']

# -- Create a dictionary containing all unique D1 mascot names and the frequency that they
# occur in the DataFrame.
team_count_dict = {}
for m in mascots['name_half']:
    team_count_dict[m] = team_count_dict.get(m, 0) + 1

# -- Create a copy of the DataFrame object (just to be secure).
mascots2 = mascots.copy()

# -- Define a function that, when passed in a mascot name, returns the number of D1 teams
# who have that name (based on the dictionary we just created).
def get_count(x):
    team_dict = {'Golden Hurricane': 1, 'Sun Devils': 1, 'Dragons': 1, 'Braves': 2, 'Golden Griffins': 1, 'Wolverines': 2, 'Flames': 2, 'Phoenix': 2, 'Delta Devils': 1, 'Demon Deacons': 1, 'Demons': 1, 'Islanders': 1, 'Waves': 1, 'Fighting Illini': 1, 'Billikens': 1, 'Hilltoppers': 1, 'Aggies': 5, 'Titans': 2, 'Jaspers': 1, 'Jayhawks': 1, 'Chippewas': 1, 'Blazers': 1, 'Tribe': 1, 'Blue Raiders': 1, 'Blue Demons': 1, 'Blue Devils': 2, 'Horned Frogs': 1, 'Anteaters': 1, 'Spiders': 1, 'Cardinal': 1, 'Rebels': 2, 'Spartans': 5, 'Governors': 1, 'Red Flash': 1, 'Highlanders': 3, 'Pioneers': 2, 'Explorers': 1, 'Dukes': 2, 'Cornhuskers': 1, 'Trojans': 3, 'Vikings': 2, 'Gaels': 2, 'Commodores': 1, 'Mountaineers': 3, 'Red Raiders': 1, 'Vandals': 1, 'Boilermakers': 1, 'Gauchos': 1, 'Norse': 1, '49ers': 2, 'Colonials': 2, 'Quakers': 1, 'Cowboys': 3, 'Privateers': 1, 'Friars': 1, 'Crusaders': 2, 'Sooners': 1, 'Toreros': 1, 'Hatters': 1, 'Lumberjacks': 2, 'Pirates': 3, 'Colonels': 2, 'Matadors': 1, 'Seminoles': 1, 'Dons': 1, 'Pilots': 1, 'Musketeers': 1, 'Crimson': 1, 'Warriors': 1, 'Buccaneers': 2, 'Patriots': 1, 'Aztecs': 1, 'Big Green': 1, 'Cavaliers': 1, 'Rockets': 1, 'Scarlet Knights': 1, 'Raiders': 2, 'Fighting Irish': 1, 'Blue Hose': 1, 'Minutemen': 1, 'Paladins': 1, 'Flyers': 1, 'Knights': 2, 'Miners': 1, 'Aces': 1, 'Golden Gophers': 1, 'Beavers': 1, 'Sycamores': 1, 'Lions': 3, 'Monarchs': 1, 'Golden Lions': 1, 'Pride': 1, 'Nittany Lions': 1, 'Ramblers': 1, 'Lobos': 1, 'Red Wolves': 1, 'Bonnies': 1, 'Seawolves': 1, 'Wolfpack': 1, 'Wolf Pack': 1, 'Tigers': 13, 'Badgers': 1, 'Bobcats': 4, 'Cougars': 6, 'Catamounts': 2, 'Coyotes': 1, 'Jaguars': 3, 'Bearkats': 1, 'Bearcats': 2, 'Leopards': 1, 'Panthers': 7, 'Golden Panthers': 1, 'Red Foxes': 1, 'Wildcats': 10, 'Bears': 7, 'Black Bears': 1, 'Bruins': 2, 'Big Red': 1, 'Mean Green': 1, 'Mocs': 1, 'Grizzlies': 1, 'Golden Grizzlies': 1, 'Golden Bears': 1, 'Bengals': 1, 'Bulldogs': 14, 'Saints': 1, 'Terriers': 3, 'Huskies': 5, "Runnin' Bulldogs": 1, 'Terrapins': 1, 'Retrievers': 1, 'Greyhounds': 1, 'Salukis': 1, 'Great Danes': 1, 'Hoyas': 1, 'Volunteers': 1, 'Leathernecks': 1, 'Hoosiers': 1, 'Shockers': 1, 'Rattlers': 1, "Ragin' Cajuns": 1, 'Gators': 1, 'Jackrabbits': 1, 'Orange': 1, 'Buckeyes': 1, 'Fightin Blue Hens': 1, 'Gamecocks': 2, 'Chanticleers': 1, 'Peacocks': 1, 'Hokies': 1, 'Hornets': 3, 'Yellow Jackets': 1, 'Crimson Tide': 1, 'Mastodons': 1, 'Ducks': 1, 'Stags': 1, 'Midshipmen': 1, 'Buffaloes': 1, 'Bison': 3, 'Thundering Herd': 1, 'Bisons': 1, 'Rams': 4, 'Tar Heels': 1, 'Fighting Camels': 1, 'Dolphins': 1, 'Longhorns': 1, 'Bulls': 2, 'Mavericks': 2, 'Razorbacks': 1, 'Antelopes': 1, 'Roadrunners': 2, 'Owls': 4, 'Keydets': 1, 'Zips': 1, 'Kangaroos': 1, 'Falcons': 2, 'Bluejays': 1, 'Cardinals': 4, 'Redbirds': 1, 'Cyclones': 1, 'Blackbirds': 1, 'Red Storm': 1, 'Thunderbirds': 1, 'Hurricanes': 1, 'Green Wave': 1, 'Black Knights': 1, 'Mustangs': 2, 'Vaqueros': 1, 'Racers': 1, 'Broncos': 3, 'Broncs': 1, 'Lancers': 1, 'Fighting Hawks': 1, 'Skyhawks': 1, 'RedHawks': 1, 'Hawks': 4, 'River Hawks': 1, 'Warhawks': 1, 'Mountain Hawks': 1, 'Hawkeyes': 1, 'Redhawks': 2, 'Eagles': 10, 'Purple Eagles': 1, 'Ospreys': 1, 'Seahawks': 2, 'Golden Eagles': 4, 'Golden Flashes': 1, 'Utes': 1, 'Penguins': 1}
    if x in team_dict:
        return team_dict[x]

# -- Use our get_count function to create a new column in the DataFrame that shows how
# many teams share the same mascot name. We only want to work with teams that have
# 3 or more teams who share the same name, so create a new DataFrame containing only
# only entries who fulfill this criteria.
mascots2['count'] = mascots2['name_half'].apply(get_count)
mascots3 = mascots2[mascots2['count'] >= 3]

# -- Connect to our SQLite file.
conn = sqlite3.connect('NCAA_teams.sqlite')

# -- Select all data points from this SQLite file and read them into a DataFrame.
teams = pd.read_sql_query('SELECT * FROM Teams', conn)

# -- Merge the teams DataFrame with our manipulated mascots DataFrame. Use an inner
# merge so that only teams whose name appears in both DataFrames are used.
merged_data2 = pd.merge(teams, mascots3[['id', 'name_half', 'mascot', 'mascot_name', 'name']], on='name', how='inner')

# -- Group the merged DataFrame by mascot name and create a pandas Series object
# showing the mascot name and the number of average wins for all teams who have that
# mascot name. Sort this series in descending order.
final_data = merged_data2.groupby(['name_half']).wins.mean().sort_values(ascending=False)

# -- Create a barplot of this Series object using matplotlib.
final_data.plot(kind='bar')
plt.xlabel('Mascot Name')
plt.ylabel('Count')
plt.show()
