import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


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


def fracdata_values():

    signal = pd.read_csv(filepath, delimiter='\t', low_memory=False, usecols=['AcqTime', 'TR_PRESS', 'SLURRYRATE'],
                         skiprows=[1, 2]).dropna()
    signal['AcqTime'] = pd.to_datetime(signal['AcqTime'])

    pressure_data = []
    rate_data = []
    pressures = []
    rates = []

    i = 0
    step = 30
    zero_rate_threshold = 0.5
    std_rate_threshold = 1
    percentiles_top = 90
    percentiles_btm = 10

    while i < len(signal):
        rate_data.append(signal.SLURRYRATE.loc[i:i+step])
        pressure_data.append(signal['TR_PRESS'].loc[i:i+step])
        if signal.SLURRYRATE.loc[i:i+step].astype(float).std() > std_rate_threshold:
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

    fig, ax = plt.subplots()
    ax.boxplot(rate_data)
    ax.boxplot(pressure_data)
    #    plt.plot(signal)

    plt.title(f'Last rate before drop: {rates[-3]}. Last rate: {rates[-1]}.\n'
              f'Last pressure before drop: {pressures[-3]}. Last pressure: {pressures[-1]}.\n'
              f'Pad rate: {rates[-5]}. Pad pressure: {pressures[-5]}\n'
              f'WHP: {pressures[0]}. ISIP: {isip()}')
    plt.show()

    return pd.Series(data=[filename, soj, eoj, pressures[0], pressures[-5], rates[-5], pressures[-3], rates[-3], pressures[-1], rates[-1], isip()],
                     index=parameters)

if __name__ == '__main__':

    parameters = ['Job', 'SOJ', 'EOJ', 'Initial WHP', 'Pad pressure', 'Pad rate', 'Last pressure before drop',
                  'Last rate before drop', 'Last pressure', 'Last rate', 'ISIP']
    fracdata_table = pd.DataFrame(index=parameters)
    for filename in os.listdir(input('Enter fracturing job data folder path: ')):
        if filename.endswith('.txt'):
            filepath = os.getcwd() + '\\' + filename
            fracdata_table = pd.concat([fracdata_table, fracdata_values()], axis=1)
            print(f'Interpretation result for {filename} is done')
    fracdata_table.to_csv('fracdata.csv', header=False)

#    with open('fracdata.csv', 'w', newline='') as csvfile:
#        write = csv.writer(csvfile)
#    write.writerow(fields)
#    write.writerows(rows)

    print('Full interpretation has been saved to', os.getcwd())
