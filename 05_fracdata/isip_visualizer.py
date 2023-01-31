import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates

#def line_intersection(line1, line2):
#    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
#    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

#    def det(a, b):
#        return a[0] * b[1] - a[1] * b[0]

#    div = det(xdiff, ydiff)
#    if div == 0:
#        raise Exception('lines do not intersect')

#    d = (det(*line1), det(*line2))
#    x = det(d, xdiff) / div
#    y = det(d, ydiff) / div
#    return x, y


# def isip():

#    signal = pd.read_csv(filepath, delimiter='\t', low_memory=False, usecols=['AcqTime', 'TR_PRESS', 'SLURRYRATE'],
#                         skiprows=[1, 2]).dropna()
#    signal['AcqTime'] = pd.to_datetime(signal['AcqTime'])
#    signal['INDEX'] = range(0, len(signal))

#    p = np.polyfit(signal['INDEX'].loc[5570:5630], signal['TR_PRESS'].loc[5570:5630], 1)

#    For future visualization
#    plt.scatter(signal['INDEX'].loc[5570:5630], signal['TR_PRESS'].loc[5570:5630], c='gray', marker='o',
#        edgecolors='k', s=10)
#    plt.plot(np.array(plt.xlim()), p[1] + p[0] * np.array(plt.xlim()))
#    plt.plot([5570, 5570], [5000, 8000])

#    plt.plot(signal['INDEX'], signal['TR_PRESS'])
#    plt.show()

#    a = np.array([5570, 5000])
#    b = np.array([5570, 8000])
#    c = np.array([np.array(plt.xlim())[1], p[1] + p[0] * np.array(plt.xlim())[1]])
#    d = np.array([np.array(plt.xlim())[0], p[1] + p[0] * np.array(plt.xlim())[0]])

#    return round(line_intersection((a, b), (c, d))[1])

filepath = r'C:\Users\Borisenko\PycharmProjects\miscellaneous\05_fracdata\dataset\HZEM-141204\HZEM-141204 Stage 12 ASCII.txt'

signal = pd.read_csv(filepath, delimiter='\t', low_memory=False, usecols=['AcqTime', 'TR_PRESS', 'SLURRYRATE', 'PROP_CON'],
                     skiprows=[1, 2]).dropna()
signal['AcqTime'] = pd.to_datetime(signal['AcqTime'])

fig, ax = plt.subplots()
#fig.subplots_adjust(right=0.75)

twin1 = ax.twinx()
# twin2 = ax.twinx()

# Offset the right spine of twin2.  The ticks and label have already been
# placed on the right by twinx above.
#twin2.spines.right.set_position(('axes', 1.2))


h = 0
pre_stop_point = 0
while signal['SLURRYRATE'].iloc[h+round(len(signal['SLURRYRATE'])/2)] > 0:
    h += 1
    pre_stop_point = h - 100

# Choose ISIP oscillations range
isip_range = len(signal['SLURRYRATE']) - pre_stop_point
pressure = np.array(signal['TR_PRESS'].iloc[pre_stop_point:].to_list())
rate = np.array(signal['SLURRYRATE'].iloc[pre_stop_point:].to_list())

i = 0
eoj_point = 0
while rate[i] > 0:
    i += 1
    eoj_point = i

j = 0
pressure_threshold_left = 0
while pressure[j] > pressure[eoj_point]:
    j += 1
    pressure_threshold_left = j

k = 0
step = 3
pressure_stdev_threshold = 349
pressure_threshold_right = 0
while k < len(pressure):
    if pressure[k:k+step].std() > pressure_stdev_threshold:
        pressure_threshold_right = k
    k += 1

# Implement first-degree polinomial (linear regression)
lr = np.polyfit(np.arange(pressure_threshold_left, pressure_threshold_right), pressure[pressure_threshold_left:pressure_threshold_right], 1)
mymodel = np.poly1d(lr)
myline = np.linspace(pressure_threshold_left, pressure_threshold_right, pressure_threshold_right-pressure_threshold_left) # Draw the line

# Calculate ISIP value
isip_value = mymodel(myline)[int(round(len(mymodel(myline))/2))]
print(isip_value)

# Show plot with ISIP lines
plt.plot(myline, mymodel(myline))

p1, = ax.plot(np.arange(isip_range), pressure, 'r-', label='Treating Pressure, psi')
p2, = twin1.plot(np.arange(isip_range), rate, 'b-', label='Slurry Rate, bpm')
# p3, = twin2.plot(signal['AcqTime'], signal['PROP_CON'], 'g-', label='Proppant Concentration, ppac')
p4, = ax.plot(np.arange(pressure_threshold_left, pressure_threshold_right), mymodel(myline))
p5, = ax.plot([eoj_point, eoj_point], [0, pressure.max()])

ax.set_xlim(0, isip_range)
#ax.set_ylim(5000, 12000)
twin1.set_ylim(0, 120)
#twin2.set_ylim(0, 3)

#ax.set_xlabel('Time')
ax.set_ylabel('Treating Pressure, psi')
twin1.set_ylabel('Slurry Rate, bpm')
#twin2.set_ylabel('Proppant Concentration, ppac')

ax.yaxis.label.set_color(p1.get_color())
twin1.yaxis.label.set_color(p2.get_color())
#twin2.yaxis.label.set_color(p3.get_color())

myFmt = dates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(myFmt)

tkw = dict(size=2, width=1.5)
ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
#twin2.tick_params(axis='y', colors=p3.get_color(), **tkw)
#ax.tick_params(axis='x', **tkw)

plt.show()
