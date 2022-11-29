import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import seaborn.objects as so


def load_csv(filename):
    return pd.read_csv(f'DATA\{filename}.csv')


def get_hybrid_data(filename):
    races = load_csv(filename)
    # sort races in ascending order by the 2 collumn
    races.sort_values(by=['year'])
    # make copy with values greater than 2014
    c = races.iloc[:, 1] > 2013  # when hybrid era started
    hybrid_races = races[c]
    return hybrid_races


# daniels id
DANIELRICID = 817

circuits = load_csv('circuits')
results = load_csv('results')
hybrid_era_races = get_hybrid_data('races')
constuctors = load_csv('constructors')
# take races that have the race id from hybrid_era_races
hybrid_era_results_list = [finish
                           for index, finish in results.iterrows()
                           if finish['raceId'] in hybrid_era_races['raceId']]
hybrid_era_results = pd.DataFrame(hybrid_era_results_list)
# only get hybrid era constructors
hybrid_era_constructors_list = [team
                                for index, team in constuctors.iterrows()
                                if team['constructorId'] in hybrid_era_results['constructorId'].values]
hybrid_era_constructors = pd.DataFrame(hybrid_era_constructors_list)

# connnect data of constructor name and adds easy creation of driver later on
# make dict of constructorId and name
hybrid_era_constructors_dict = {}
for team in hybrid_era_constructors_list:
    hybrid_era_constructors_dict[team.constructorId] = team.constructorRef
# now add the constructorRef to the DF based on the "key" which is the ID
consturctor_name = []
for index, team in hybrid_era_results.iterrows():
    consturctor_name.append(
        hybrid_era_constructors_dict.get(team['constructorId']))
hybrid_era_results['constructorName'] = consturctor_name
# only get races that dannyric was in ID = 817
daniel_race_data_list = []
for index, race in hybrid_era_results.iterrows():
    if DANIELRICID == race['driverId']:
        daniel_race_data_list.append(race)
daniel_race_data = pd.DataFrame(daniel_race_data_list)
# coralation dannies best seasons to his teamsmate and constructor
dan_fastest_lap_list = daniel_race_data['fastestLapSpeed'].to_numpy()
"""sns.scatterplot(data=daniel_race_data,
                x='raceId', y='constructorName',
                hue=np.around(np.genfromtxt(dan_fastest_lap_list)),
                )
plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
"""
# get consistentsy of his finishes standard deveation of results
# only get races he finishes


def status_1_races(df):
    clean_race_status_code = 1
    df = df[df['statusId'] < 2]
    df['statusId'].astype(float)
    return(df.sort_values(by='position'))


sns.catplot(data=status_1_races(daniel_race_data),
            x='position', y='laps', col='constructorName')
# when was peak dannyric

# did he fall off is it him or the car compare to landos results

# maybe get some qualify results to see if danny out classes his teammate


plt.show()
