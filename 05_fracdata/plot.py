import pandas as pd
import matplotlib.pyplot as plt

filepath = r'C:\Users\Borisenko\PycharmProjects\miscellaneous\05_fracdata\dataset\HZEM-141204\HZEM-141204 Stage 10 ASCII.txt'

signal = pd.read_csv(filepath, delimiter='\t', low_memory=False, usecols=['AcqTime', 'TR_PRESS', 'SLURRYRATE', 'PROP_CON'],
                     skiprows=[1, 2]).dropna()
signal['AcqTime'] = pd.to_datetime(signal['AcqTime'])

plt.plot(signal['AcqTime'], signal[['TR_PRESS', 'SLURRYRATE', 'PROP_CON']])

pressure_data = []
rate_data = []
step = 30

i = 0
while i < len(signal):
    rate_data.append(signal.SLURRYRATE.loc[i:i + step])
    pressure_data.append(signal['TR_PRESS'].loc[i:i + step])
    i += step + 1

fig, ax = plt.subplots()
ax.boxplot(rate_data)
ax.boxplot(pressure_data)
plt.show()
print(abs(signal.SLURRYRATE.loc[2231:2261].astype(float).mean() - signal.SLURRYRATE.astype(float).max()))