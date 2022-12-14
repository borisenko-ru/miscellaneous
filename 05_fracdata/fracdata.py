import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
# from numba import jit, cuda
# cuda.select_device(0)
# import sys
# if not sys.warnoptions:
#    import warnings
#    warnings.simplefilter("ignore")


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def isip():

    signal = pd.read_csv(filepath, delimiter='\t', low_memory=False, usecols=['AcqTime', 'TR_PRESS', 'SLURRYRATE'],
                         skiprows=[1, 2]).dropna()
    signal['AcqTime'] = pd.to_datetime(signal['AcqTime'])
    signal['INDEX'] = range(0, len(signal))

    p = np.polyfit(signal['INDEX'].loc[5570:5630], signal['TR_PRESS'].loc[5570:5630], 1)

#    For future visualization
#    plt.scatter(signal['INDEX'].loc[5570:5630], signal['TR_PRESS'].loc[5570:5630], c='gray', marker='o',
#        edgecolors='k', s=10)
#    plt.plot(np.array(plt.xlim()), p[1] + p[0] * np.array(plt.xlim()))
#    plt.plot([5570, 5570], [5000, 8000])

#    plt.plot(signal['INDEX'], signal['TR_PRESS'])
#    plt.show()

    a = np.array([5570, 5000])
    b = np.array([5570, 8000])
    c = np.array([np.array(plt.xlim())[1], p[1] + p[0] * np.array(plt.xlim())[1]])
    d = np.array([np.array(plt.xlim())[0], p[1] + p[0] * np.array(plt.xlim())[0]])

    return round(line_intersection((a, b), (c, d))[1])


# @jit
def fracdata_values():

    signal = pd.read_csv(filepath, delimiter='\t', low_memory=False, usecols=['AcqTime', 'TR_PRESS', 'SLURRYRATE', 'PROP_CON'], skiprows=[1, 2]).dropna()
    signal['AcqTime'] = pd.to_datetime(signal['AcqTime'])

    pressure_data = []
    rate_data = []
    pressures = []
    rates = []

    step = 30
    zero_rate_threshold = signal['SLURRYRATE'].max() * 0.15
    zero_prop_threshold = signal['PROP_CON'].max() * 0.15
    sample_gap = 30
    rate_stdev_threshold = 1
    percentiles_top = 90
    percentiles_btm = 10

    i = 0
    breakpoint = 0
    while i < len(signal):
        if signal['PROP_CON'].loc[i].astype(float) > zero_prop_threshold and breakpoint == 0:
            pad_rate = signal.SLURRYRATE.loc[i-sample_gap:i].median()
            pad_pressure = signal['TR_PRESS'].loc[i-sample_gap:i].median()
            breakpoint = 1
        i += 1

    i = 0
    breakpoint = 0
    while i < len(signal) / 2:
        if signal['SLURRYRATE'].loc[i].astype(float) > zero_rate_threshold and breakpoint == 0:
            initial_whp = signal['TR_PRESS'].loc[i-sample_gap:i].median()
            breakpoint = 1
        i += 1
    i = 0

    while i < len(signal):
        rate_data.append(signal.SLURRYRATE.loc[i:i+step])
        pressure_data.append(signal['TR_PRESS'].loc[i:i+step])
        if signal.SLURRYRATE.loc[i:i+step].astype(float).std() > rate_stdev_threshold:
            rates.append(round(signal.SLURRYRATE.loc[i:i+step].describe(percentiles=[percentiles_btm/100])[str(percentiles_btm)+'%']))
            rates.append(round(signal.SLURRYRATE.loc[i:i+step].describe(percentiles=[percentiles_top/100])[str(percentiles_top)+'%']))
            pressures.append(round(signal['TR_PRESS'].loc[i:i+step].describe(percentiles=[percentiles_btm/100])[str(percentiles_btm)+'%']))
            pressures.append(round(signal['TR_PRESS'].loc[i:i+step].describe(percentiles=[percentiles_top/100])[str(percentiles_top)+'%']))
        i += step + 1

    i = 0
    while i < len(signal) / 2:
        if signal.SLURRYRATE.loc[i] < zero_rate_threshold:
            soj = signal.AcqTime.loc[i]
        i += 1

    i = 0
    while i < len(signal):
        if signal.SLURRYRATE.loc[i] > zero_rate_threshold:
            eoj = signal.AcqTime.loc[i+1]
        i += 1

#    fig, ax = plt.subplots()
#    ax.boxplot(rate_data)
#    ax.boxplot(pressure_data)
#    plt.plot(signal)

#    plt.title(f'Last rate before drop: {rates[-3]}. Last rate: {rates[-1]}.\n'
#              f'Last pressure before drop: {pressures[-3]}. Last pressure: {pressures[-1]}.\n'
#              f'Pad rate: {rates[-5]}. Pad pressure: {pressures[-5]}\n'
#              f'WHP: {pressures[0]}. ISIP: {isip()}')
#    plt.show()

#    return pd.Series(data=[filename, soj, eoj, pressures[0], pressures[-5], rates[-5], pressures[-3], rates[-3], pressures[-1], rates[-1], isip()],
#                     index=parameters)
    return pd.Series(data=[filename, soj, eoj, initial_whp, pad_pressure, pad_rate, pressures[-3], rates[-3], pressures[-1], rates[-1], isip()],
                     index=parameters)

if __name__ == '__main__':

    parameters = ['Job', 'SOJ', 'EOJ', 'Initial WHP', 'Pad pressure', 'Pad rate', 'Last pressure before drop',
                  'Last rate before drop', 'Last pressure', 'Last rate', 'ISIP']

    fracdata_table = pd.DataFrame(index=parameters)
    for root, dir, files in os.walk(input('Enter fracturing job data folder path: ')):
        for filename in files:
            if filename.endswith('.txt'):
                filepath = root + '\\' + filename
                fracdata_table = pd.concat([fracdata_table, fracdata_values()], axis=1)
                print(f'Interpretation result for {filename} is done')
    fracdata_table.to_csv('fracdata.csv', header=False)
    print('Full interpretation has been saved to', os.getcwd())

#    with open('fracdata.csv', 'w', newline='') as csvfile:
#        write = csv.writer(csvfile)
#    write.writerow(fields)
#    write.writerows(rows)
