# h5 file finite data to csv exractor

import pandas as pd
import h5py
import tables as tb

import warnings
warnings.filterwarnings("ignore")

filename = "file.h5"
f = h5py.File(filename, "r")

with tb.File(filename, 'r') as h5r:     
    for node in h5r.walk_nodes('/',classname='Leaf'):         
        try:
            print ('visiting object:', node._v_pathname, 'export data to CSV')
            csvfname = node._v_pathname[1:].replace('/','_') +'.csv'
            dataset = pd.DataFrame(f[node._v_pathname])
            dataset.to_csv(csvfname)
        except:
            pass
        

