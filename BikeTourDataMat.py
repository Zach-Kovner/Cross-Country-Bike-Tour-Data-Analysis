import numpy as np
import pandas as pd
from BikeTourData import laps


A = pd.concat([laps['Cum Distance'], laps['Change Elev'], laps['Laps'], laps['Wind'], laps['Rain']], axis=1)
A['constant'] =1

