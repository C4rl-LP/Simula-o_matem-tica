import numpy as np
from matplotlib import pyplot as plt

N = 1000000
n = 0
for _ in range(N):
    x = np.random.uniform(0,2)
    y = np.random.uniform(0,2)
    if (x-1)**2 + (y-1)**2 < 1:
        n +=1
print(n/N*4) 

x = np.random.multivariate_normal([0,0], [[1,0],
                                        [0,1]], 100)

norms = np.linalg.norm(x, axis=1, keepdims=True)
print(norms)
x = x/norms

plt.scatter(x[:,0], x[:,1])
plt.show()
