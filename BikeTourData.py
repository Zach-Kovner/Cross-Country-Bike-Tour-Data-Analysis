import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
#intro
M = 2147483647

#lap data summaries
lap_data_list = sorted(glob.glob('data/csv_s/*.csv')) 
ld_combined = pd.concat((pd.read_csv(f) for f in lap_data_list), ignore_index = True) #includes daily summary
summaries = ld_combined.loc[ld_combined.Laps=='Summary'].reset_index(drop=True) #summary data only
summaries['Calories'] = summaries['Calories'].replace(',','',regex=True).astype(int)


laps = ld_combined.loc[ld_combined.Laps != 'Summary'].reset_index(drop=True) #lap data only, no summaries

laps['Total Ascent'] = laps['Total Ascent'].replace(',', '', regex=True).astype(int)
laps['Total Descent'] = laps['Total Descent'].replace(',', '', regex=True).astype(int)
laps['Change Elev'] = laps['Total Ascent'] - laps['Total Descent'].replace(',', '', regex=True).astype(int)

laps['Cum Distance'] = laps['Distance'].cumsum()
laps['Cum Elev'] = laps['Total Ascent'].cumsum() + 400

laps['Moving Time'] = laps['Moving Time'].apply(lambda x: x if x.count(':') == 2 else '00:' + x)
laps['Moving Time'] = pd.to_timedelta(laps['Moving Time'])

laps['Day'] = 1
laps['Laps']= laps['Laps'].astype(int)

#adding rest days

laps['Rest'] = False

def insert_rest(): #given day #, inserts full row of zeros for rest day
    new_row = pd.DataFrame({'Laps': [np.nan],  'Time':[np.nan], 
               'Cumulative Time':[np.nan],  'Distance':[np.nan],  'Avg Speed':[np.nan], 'Avg HR':[np.nan],  'Max HR':[np.nan],
                   'Total Ascent': [np.nan],  'Total Descent': [np.nan], 'Calories':[np.nan],  'Max Speed':[np.nan],     'Moving Time':[np.nan],  'Avg Moving Speed':[np.nan],
                       'Change Elev':[np.nan],  'Cum Distance':[np.nan],  'Cum Elev':[np.nan],  'Day':[np.nan], 'Rest':True})
    return new_row

#adding rest days
laps = pd.concat([laps.iloc[:43], insert_rest(), laps.iloc[43:]], ignore_index=True) #day 5
laps = pd.concat([laps.iloc[:190], insert_rest(), insert_rest(), laps.iloc[190:]], ignore_index=True) #day 15,16
laps = pd.concat([laps.iloc[:257], insert_rest(), laps.iloc[257:]], ignore_index=True) #day 20
laps = pd.concat([laps.iloc[:386], insert_rest(), laps.iloc[386:]], ignore_index=True) #day 27
laps = pd.concat([laps.iloc[:398], insert_rest(), insert_rest(), laps.iloc[398:]], ignore_index=True) #day 29,30
laps = pd.concat([laps.iloc[:418], insert_rest(), laps.iloc[418:]], ignore_index=True) #day 32
laps = pd.concat([laps.iloc[:494], insert_rest(), insert_rest(), insert_rest(), laps.iloc[494:]], ignore_index=True) #day 37,8,9
laps = pd.concat([laps.iloc[:616], insert_rest(), laps.iloc[616:]], ignore_index=True) #day 47


for i in range(1, len(laps)):
    current_lap = laps.loc[i, 'Laps']
    prev_lap = laps.loc[i-1, 'Laps']
    
    if (pd.isna(current_lap)):
        laps.loc[i, 'Day'] = laps.loc[i-1, 'Day'] + 1
    elif (current_lap < prev_lap) | (pd.isna(prev_lap)):
        laps.loc[i, 'Day'] = laps.loc[i-1, 'Day'] + 1
    else:
        laps.loc[i, 'Day'] = laps.loc[i-1, 'Day']



#full .fit -> .csv position data
pos_data_list = sorted(glob.glob('data/fit_s/*csv'))
ps = pd.concat((pd.read_csv(f) for f in pos_data_list), ignore_index = True)
ps = ps.rename(columns={'timestamp': 'long'})
ps = ps.rename(columns={'position_lat': 'lat'})
ps=ps.rename(columns={'cadence':'dist'})

ps.long = ps.long.replace(M, np.nan)
ps.lat = ps.lat.replace(M, np.nan)

