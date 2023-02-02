import pandas as pd
import numpy as np
import os


# True value calculation
def fracdata_values():

    pressure_data, rate_data, pressures, rates = [], [], [], []
    step = 30
    sample_gap = 30
    rate_stdev_threshold = 1
    percentiles_top = 90
    percentiles_btm = 10
    zero_rate_threshold = signal['SLURRYRATE'].max() * 0.15
    zero_prop_threshold = signal['PROP_CON'].max() * 0.15

    # Calculate START_OF_JOB
    i = 0
    while i < len(signal) / 2:
        if signal.SLURRYRATE.loc[i] < zero_rate_threshold:
            soj = signal.AcqTime.loc[i]
        i += 1

    # Calculate END_OF_JOB
    i = 0
    while i < len(signal):
        if signal.SLURRYRATE.loc[i] > zero_rate_threshold:
            eoj = signal.AcqTime.loc[i + 1]
        i += 1

    # Calculate PAD_RATE and PAD_PRESSURE
    i = 0
    break_point = 0
    while i < len(signal):
        if signal['PROP_CON'].loc[i].astype(float) > zero_prop_threshold and break_point == 0:
            pad_rate = signal.SLURRYRATE.loc[i-sample_gap:i].median()
            pad_pressure = signal['TR_PRESS'].loc[i-sample_gap:i].median()
            break_point = 1
        i += 1

    # Calculate INITIAL_WHP
    i = 0
    break_point = 0
    while i < len(signal) / 2:
        if signal['SLURRYRATE'].loc[i].astype(float) > zero_rate_threshold and break_point == 0:
            initial_whp = signal['TR_PRESS'].loc[i-sample_gap:i].median()
            break_point = 1
        i += 1
    i = 0

    # Calculate 'Last pressure before drop', 'Last rate before drop', 'Last pressure', and 'Last rate'
    while i < len(signal):
        rate_data.append(signal.SLURRYRATE.loc[i:i+step])
        pressure_data.append(signal['TR_PRESS'].loc[i:i+step])
        if signal.SLURRYRATE.loc[i:i+step].astype(float).std() > rate_stdev_threshold:
            rates.append(round(signal.SLURRYRATE.loc[i:i+step].describe(percentiles=[percentiles_btm/100])[str(percentiles_btm)+'%']))
            rates.append(round(signal.SLURRYRATE.loc[i:i+step].describe(percentiles=[percentiles_top/100])[str(percentiles_top)+'%']))
            pressures.append(round(signal['TR_PRESS'].loc[i:i+step].describe(percentiles=[percentiles_btm/100])[str(percentiles_btm)+'%']))
            pressures.append(round(signal['TR_PRESS'].loc[i:i+step].describe(percentiles=[percentiles_top/100])[str(percentiles_top)+'%']))
        i += step + 1

    # ISIP_STEP_01
    i = 0
    pre_stop_point = 0
    while signal['SLURRYRATE'].iloc[i + round(len(signal['SLURRYRATE']) / 2)] > 0:
        i += 1
        pre_stop_point = i - 100

    # ISIP_STEP_02. Choose ISIP oscillations range
    pressure = np.array(signal['TR_PRESS'].iloc[pre_stop_point:].to_list())
    rate = np.array(signal['SLURRYRATE'].iloc[pre_stop_point:].to_list())

    # ISIP_STEP_03
    i = 0
    eoj_point = 0
    while rate[i] > 0:
        i += 1
        eoj_point = i

    # ISIP_STEP_04
    i = 0
    pressure_threshold_left = 0
    while pressure[i] > pressure[eoj_point]:
        i += 1
        pressure_threshold_left = i

    # ISIP_STEP_05
    i = 0
    step = 3
    pressure_stdev_threshold = 349
    pressure_threshold_right = 0
    while i < len(pressure):
        if pressure[i:i + step].std() > pressure_stdev_threshold:
            pressure_threshold_right = i
        i += 1

    # ISIP_STEP_06. Implement first-degree polinomial (linear regression)
    lr = np.polyfit(np.arange(pressure_threshold_left, pressure_threshold_right),
                    pressure[pressure_threshold_left:pressure_threshold_right], 1)
    mymodel = np.poly1d(lr)
    myline = np.linspace(pressure_threshold_left, pressure_threshold_right,
                         pressure_threshold_right - pressure_threshold_left)  # Draw the line

    # ISIP_STEP_07
    isip_value = round(mymodel(myline)[int(round(len(mymodel(myline)) / 2))], 0)

    return pd.Series(data=[filename, soj, eoj, initial_whp, pad_pressure, pad_rate, pressures[-3], rates[-3], pressures[-1], rates[-1], isip_value],
                     index=parameters)


# X-position of value calculation
def fracdata_x():

    pressure_data, rate_data, pressures, rates = [], [], [], []
    step = 30

    zero_rate_threshold = signal['SLURRYRATE'].max() * 0.15
    zero_prop_threshold = signal['PROP_CON'].max() * 0.15

    # Calculate START_OF_JOB
    i = 0
    while i < len(signal) / 2:
        if signal.SLURRYRATE.loc[i] < zero_rate_threshold:
            soj_x = i
        i += 1

    # Calculate END_OF_JOB
    i = 0
    while i < len(signal):
        if signal.SLURRYRATE.loc[i] > zero_rate_threshold:
            eoj_x = i + 1
        i += 1

    # Calculate PAD_RATE and PAD_PRESSURE
    sample_gap = 30
    break_point = 0
    i = 0
    while i < len(signal):
        if signal['PROP_CON'].loc[i].astype(float) > zero_prop_threshold and break_point == 0:
            pad_rate_x_list = [j for j in range(i - sample_gap, i)]
            pad_rate_x = pad_rate_x_list[int(round(len(pad_rate_x_list) / 2, 0))]
            pad_pressure_x = pad_rate_x
            break_point = 1
        i += 1

    # Calculate INITIAL_WHP
    break_point = 0
    i = 0
    while i < len(signal) / 2:
        if signal['SLURRYRATE'].loc[i].astype(float) > zero_rate_threshold and break_point == 0:
            initial_whp_x_list = [j for j in range(i - sample_gap, i)]
            initial_whp_x = initial_whp_x_list[int(round(len(initial_whp_x_list) / 2, 0))]
            break_point = 1
        i += 1
    i = 0

    # Calculate 'Last pressure before drop', 'Last rate before drop', 'Last pressure', and 'Last rate'
    rate_stdev_threshold = 1
    percentiles_top = 90
    percentiles_btm = 10
    while i < len(signal):
        rate_data.append(signal.SLURRYRATE.loc[i:i+step])
        pressure_data.append(signal['TR_PRESS'].loc[i:i+step])
        if signal.SLURRYRATE.loc[i:i+step].astype(float).std() > rate_stdev_threshold:
            rates.append(round(signal.SLURRYRATE.loc[i:i+step].describe(percentiles=[percentiles_btm/100])[str(percentiles_btm)+'%']))
            rates.append(round(signal.SLURRYRATE.loc[i:i+step].describe(percentiles=[percentiles_top/100])[str(percentiles_top)+'%']))
            pressures.append(round(signal['TR_PRESS'].loc[i:i+step].describe(percentiles=[percentiles_btm/100])[str(percentiles_btm)+'%']))
            pressures.append(round(signal['TR_PRESS'].loc[i:i+step].describe(percentiles=[percentiles_top/100])[str(percentiles_top)+'%']))
        i += step + 1

    # ISIP_STEP_01
    i = 0
    pre_stop_point = 0
    while signal['SLURRYRATE'].iloc[i + round(len(signal['SLURRYRATE']) / 2)] > 0:
        i += 1
        pre_stop_point = i - 100

    # ISIP_STEP_02. Choose ISIP oscillations range
    pressure = np.array(signal['TR_PRESS'].iloc[pre_stop_point:].to_list())
    rate = np.array(signal['SLURRYRATE'].iloc[pre_stop_point:].to_list())

    # ISIP_STEP_03
    i = 0
    eoj_point = 0
    while rate[i] > 0:
        i += 1
        eoj_point = i

    # ISIP_STEP_04
    i = 0
    pressure_threshold_left = 0
    while pressure[i] > pressure[eoj_point]:
        i += 1
        pressure_threshold_left = i

    # ISIP_STEP_05
    i = 0
    step = 3
    pressure_stdev_threshold = 349
    pressure_threshold_right = 0
    while i < len(pressure):
        if pressure[i:i + step].std() > pressure_stdev_threshold:
            pressure_threshold_right = i
        i += 1

    # ISIP_STEP_06. Implement first-degree polinomial (linear regression)
    lr = np.polyfit(np.arange(pressure_threshold_left, pressure_threshold_right),
                    pressure[pressure_threshold_left:pressure_threshold_right], 1)
    mymodel = np.poly1d(lr)
    myline = np.linspace(pressure_threshold_left, pressure_threshold_right,
                         pressure_threshold_right - pressure_threshold_left)  # Draw the line

    # ISIP_STEP_07
    isip_value = round(mymodel(myline)[int(round(len(mymodel(myline)) / 2))], 0)

    return pd.Series(data=[filename, soj_x, eoj_x, initial_whp_x, pad_pressure_x, pad_rate_x, pressures[-3], rates[-3], pressures[-1], rates[-1], isip_value],
                     index=parameters)


if __name__ == '__main__':

    parameters = ['Job', 'SOJ', 'EOJ', 'Initial WHP', 'Pad pressure', 'Pad rate', 'Last pressure before drop',
                  'Last rate before drop', 'Last pressure', 'Last rate', 'ISIP']

    fracdata_table = pd.DataFrame(index=parameters)
    for root, directories, files in os.walk(input('Enter fracturing job data folder path: ')):
        for filename in files:
            if filename.endswith('.txt'):
                filepath = root + '\\' + filename
                signal = pd.read_csv(filepath, delimiter='\t', low_memory=False,
                                     usecols=['AcqTime', 'TR_PRESS', 'SLURRYRATE', 'PROP_CON'],
                                     skiprows=[1, 2]).dropna()
                try:
                    signal['AcqTime'] = pd.to_datetime(signal['AcqTime'], format='%d/%m/%Y %H:%M:%S')
                except ValueError:
                    signal['AcqTime'] = pd.to_datetime(signal['AcqTime'], format='%d:%m:%Y:%H:%M:%S')

                try:
                    fracdata_table = pd.concat([fracdata_table, fracdata_values()], axis=1)
                    print(f'Interpretation result for {filename} is done')
                except TypeError:
                    pass

    fracdata_table.to_csv('fracdata.csv', header=False)
    print('Full interpretation has been saved to', os.getcwd())
