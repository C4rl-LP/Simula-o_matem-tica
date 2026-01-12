import numpy as np

N = 1000000
n = 0
for _ in range(N):
    x = np.random.uniform(0,2)
    y = np.random.uniform(0,2)
    if (x-1)**2 + (y-1)**2 < 1:
        n +=1
print(n/N*4) 
