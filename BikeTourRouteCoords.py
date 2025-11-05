import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from BikeTourData import ps


#COORDINATE MAP OF ROUTE
x_coord = ps.lat
y_coord = ps.long

plt.scatter(x_coord, y_coord, s=1)
plt.xlim(-130, -70)
plt.ylim(30, 50)
plt.show()


