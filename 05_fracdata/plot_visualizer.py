import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates

filepath = r'C:\Users\Borisenko\PycharmProjects\miscellaneous\05_fracdata\dataset\HZEM-141204\HZEM-141204 Stage 10 ASCII.txt'

signal = pd.read_csv(filepath, delimiter='\t', low_memory=False, usecols=['AcqTime', 'TR_PRESS', 'SLURRYRATE', 'PROP_CON'],
                     skiprows=[1, 2]).dropna()
signal['AcqTime'] = pd.to_datetime(signal['AcqTime'])

#plt.plot(signal['AcqTime'], signal[['TR_PRESS', 'SLURRYRATE', 'PROP_CON']])
#plt.show()

###########

fig, ax = plt.subplots()
fig.subplots_adjust(right=0.75)

twin1 = ax.twinx()
twin2 = ax.twinx()

# Offset the right spine of twin2.  The ticks and label have already been
# placed on the right by twinx above.
twin2.spines.right.set_position(('axes', 1.2))

p1, = ax.plot(signal['AcqTime'], signal['TR_PRESS'], 'r-', label='Treating Pressure, psi')
p2, = twin1.plot(signal['AcqTime'], signal['SLURRYRATE'], 'b-', label='Slurry Rate, bpm')
p3, = twin2.plot(signal['AcqTime'], signal['PROP_CON'], 'g-', label='Proppant Concentration, ppac')

#ax.set_xlim(signal['AcqTime'].iloc[-100], signal['AcqTime'].iloc[-1])
#ax.set_ylim(5000, 12000)
twin1.set_ylim(0, 120)
twin2.set_ylim(0, 3)

ax.set_xlabel('Time')
ax.set_ylabel('Treating Pressure, psi')
twin1.set_ylabel('Slurry Rate, bpm')
twin2.set_ylabel('Proppant Concentration, ppac')

ax.yaxis.label.set_color(p1.get_color())
twin1.yaxis.label.set_color(p2.get_color())
twin2.yaxis.label.set_color(p3.get_color())

myFmt = dates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(myFmt)

tkw = dict(size=3, width=1.5)
ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
twin2.tick_params(axis='y', colors=p3.get_color(), **tkw)
#ax.tick_params(axis='x', **tkw)

plt.show()
