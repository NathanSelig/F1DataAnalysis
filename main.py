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


# daniels id 817
# lando id = 846
# max id = 830
SELECTEDDRIVERID = 830

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
    if SELECTEDDRIVERID == race['driverId']:
        daniel_race_data_list.append(race)
daniel_race_data = pd.DataFrame(daniel_race_data_list)
# coralation dannies best seasons to his teamsmate and constructor

# get consistentsy of his finishes standard deveation of results
# col can be team


def split_seasons(df):
    sorted_races = hybrid_era_races.sort_values(by=['raceId'])
    sorted_races.rename(columns={'name': 'race_name'}, inplace=True)
 #   sorted_races = sorted_races[sorted_races['year'] < 2022]

    results_with_dates = df.merge(sorted_races, on='raceId')
    results_with_dates['position'] = np.genfromtxt(
        results_with_dates['position'])
    return results_with_dates


daniel_race_data_with_dates = split_seasons(daniel_race_data)
# when was peak dannyric

# did he fall off is it him or the car compare to landos results

# maybe get some qualify results to see if danny out classes his teammate

qualli_results = load_csv('qualifying')
qualli_results = pd.DataFrame([qualli_result
                               for index, qualli_result in qualli_results.iterrows()
                               if qualli_result['driverId'] == SELECTEDDRIVERID])

qualli_results = qualli_results.merge(daniel_race_data, on='raceId')
qualli_results.rename(columns={'position_y': 'finish_position'}, inplace=True)
qualli_results.rename(columns={'position_x': 'qualli_position'}, inplace=True)

races_with_circuit = hybrid_era_races.merge(circuits, on='circuitId')
qualli_results_with_races = qualli_results.merge(
    races_with_circuit, on='raceId')
#TODO see how teams did after daniel left them 
sns.catplot(data=qualli_results_with_races.sort_values(by=['q3']),
            x='q3',y='qualli_position', col = 'circuitRef', col_wrap=3,hue='constructorName'
            )


plt.show()
