import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from BikeTourData import laps
from BikeTourData import summaries

sns.set_theme(
    style="white",
    font="Georgia")


#PART I--cumulative distance
#key insight df
vs_dist = pd.DataFrame({'Cumulative Distance': laps['Cum Distance'], 'HR':laps['Avg HR'],'Speed': laps['Avg Speed'], 'Cum Elevation': laps['Cum Elev'], 
                        'Summary Dist': summaries['Distance']})

def cd_vs_HR():
    sns.regplot(x=vs_dist['Cumulative Distance'], y=vs_dist['HR'], ci=None, scatter_kws={'s':10}, line_kws={'color':'red'})
    plt.show()


def cd_vs_Avg_Sp():
    sns.regplot(x=vs_dist['Cumulative Distance'], y=vs_dist['Speed'], ci=None, scatter_kws={'s':10}, line_kws={'color':'red'})
    plt.show()

def d_vs_day():
    sns.regplot(x=np.arange(1,41), y=([y for y in vs_dist['Summary Dist'] if pd.notna(y)]),ci=None, scatter_kws={'s':20}, line_kws = {'color':'red'})
    plt.xlabel('Day')
    plt.ylabel('Distance Per Day')
    plt.show()

#PART IIa--rest days

def rest(): #1d plot giving ratio of day after rest:day before rest. swarmplot
    def HR():
        day_before_rest_HR = []
        day_after_rest_HR = []
        avg_HR_by_day = laps.groupby('Day')['Avg HR'].mean()
        for i in range(1, len(avg_HR_by_day)):
            if pd.isna(avg_HR_by_day.iloc[i]): #if we're on a rest day
                day_before_rest_HR.append(avg_HR_by_day.iloc[i-1]) #list of hr's on days before rest, includes NaN rn
                day_after_rest_HR.append(avg_HR_by_day.iloc[i+1])
        day_before_rest_HR = np.array([x for x in day_before_rest_HR if pd.notna(x)]) #remove NaN and transform to np array
        day_after_rest_HR = np.array([x for x in day_after_rest_HR if pd.notna(x)]) #remove NaN and transform to np array

        rest_ratio_HR = day_after_rest_HR / day_before_rest_HR
        return rest_ratio_HR
    
    def Speed():
        day_before_rest_Sp = []
        day_after_rest_Sp = []
        avg_Sp_by_day = laps.groupby('Day')['Avg Speed'].mean() #slightly inaccurate bc of non full laps
        for i in range(1,len(avg_Sp_by_day)):
            if pd.isna(avg_Sp_by_day.iloc[i]): #if we're on a rest day
                day_before_rest_Sp.append(avg_Sp_by_day.iloc[i-1]) #list of hr's on days before rest, includes NaN rn
                day_after_rest_Sp.append(avg_Sp_by_day.iloc[i+1])
        day_before_rest_Sp = np.array([x for x in day_before_rest_Sp if pd.notna(x)]) #remove NaN and transform to np array
        day_after_rest_Sp = np.array([x for x in day_after_rest_Sp if pd.notna(x)]) #remove NaN and transform to np array

        rest_ratio_Sp = day_after_rest_Sp / day_before_rest_Sp
        return rest_ratio_Sp
    
    def distance():
        day_before_rest_dist = []
        day_after_rest_dist = []
        avg_dist_by_day = laps.groupby('Day')['Distance'].sum() #total distance for each day
        for i in range(1,len(avg_dist_by_day)):
            if avg_dist_by_day.iloc[i] == 0: #if we're on a rest day
                day_before_rest_dist.append(avg_dist_by_day.iloc[i-1]) #list of hr's on days before rest, includes NaN rn
                day_after_rest_dist.append(avg_dist_by_day.iloc[i+1])
        day_before_rest_dist = np.array([x for x in day_before_rest_dist if (x!=0)]) #remove NaN and transform to np array
        day_after_rest_dist = np.array([x for x in day_after_rest_dist if (x!=0)]) #remove NaN and transform to np array

        rest_ratio_dist = day_after_rest_dist / day_before_rest_dist
        return rest_ratio_dist
    
    temp_df = pd.DataFrame({
    'Ratio': np.concatenate([HR(), Speed(), distance()]),
    'group': ['HR']*len(HR()) + ['Speed']*len(Speed()) + ['Distance']*len(distance())
    })

    sns.swarmplot(x = temp_df.group, y = temp_df.Ratio, size=10)
    plt.hlines(y=1, xmin=-0.2, xmax=2.2,color='red', linestyle='--', zorder=0)
    plt.xlabel("")
    plt.show()

#PART IIb--length of day
#lets let speed be our factor of quality. how did lap speed fall off over the day? plot lap speed vs lap number for all laps. Create a df with col 1 as lap number and col 2 as avg sp
def day_length():
    xvals = laps['Laps']
    yvals = laps['Avg Speed']
    #now find the avg of avg sp for each lap
    xvals_avg = np.arange(1, laps.Laps.max()+1)
    yvals_avg = laps.groupby('Laps')['Avg Speed'].mean()

    sns.scatterplot(x=xvals, y=yvals, s=10)
    sns.lineplot(x=xvals_avg, y=yvals_avg, color='red', marker = 'o')
    plt.show()



