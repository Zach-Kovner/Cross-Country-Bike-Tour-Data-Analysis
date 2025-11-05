import pandas as pd
import numpy as np
from BikeTourData import summaries
from BikeTourData import laps

stats = pd.Series([laps['Cum Distance'].iloc[-1], 
                   laps['Cum Elev'].iloc[-1],
                   len(summaries),
                   52, 
                   laps['Avg HR'].sum() / len(laps['Avg HR']),
                   laps['Cum Distance'].iloc[-1] / (laps['Moving Time'].sum().total_seconds() /3600) ,
                   laps['Cum Distance'].iloc[-1] / len(summaries),
                   laps['Moving Time'].sum(),
                   summaries['Calories'].sum()],
                  index =['Total Distance', 'Total Ascent', 'Total Moving Days', 'Total Days', 'Avg HR', 'Avg Speed', 'Avg mi/day', 'Total Moving Time', 'Total kcal burned'], 
                  name='Stats')

print(stats)