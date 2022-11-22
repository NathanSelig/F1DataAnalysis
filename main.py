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


def get_hybrid_circuits(filename):
    # compare circuits id from races.csv to circuit id from circuits.csv
    pass

#daniels id
DANIELID = 817

circuits = load_csv('circuits')
results = load_csv('results')
hybrid_era_races = get_hybrid_data('races')
constuctors = load_csv('constructors')
# take races that have the race id from hybrid_era_races
hybrid_era_results_list = [finish for index, finish in results.iterrows()
                           if finish['raceId'] in hybrid_era_races['raceId']]
hybrid_era_results = pd.DataFrame(hybrid_era_results_list)
# only get hybrid era constructors
hybrid_era_constructors_list = [team for index, team in constuctors.iterrows()
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
daniel_race_data = []
for index,race in hybrid_era_results.iterrows():
    if DANIELID in hybrid_era_results['driverID'].values:
        daniel_race_data.append(race)


plt.show()
