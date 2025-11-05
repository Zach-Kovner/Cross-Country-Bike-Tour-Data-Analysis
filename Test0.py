import pandas as pd

day0 = pd.read_csv("data/csv_s/d01.csv")
day1 = pd.read_csv("data/csv_s/d02.csv")
print(day0.head())
print(day1.head())

day0and1 = pd.concat([day0, day1])

print(day0and1.head())
print('hey')