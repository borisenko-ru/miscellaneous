import numpy as np
import statistics

data = [1,4,6,7,8,5,3,2,2,5,7,8,9,0,65,4]

print(np.percentile(data, [25,75]))
print(statistics.median(data))
