import numpy as np
import matplotlib.pyplot as plt
import random

K = 3000

l = [0] * K
g = [0] * K

for i in range (K):
    f = 10+i/K*3500
    av = 0
    for j in range(100):
        p = j/100*2*np.pi #random.random()*2*np.pi
        y = np.sin(np.pi*f*12*(1/2/500))/(np.pi*f*12*(1/2/500))*(1-1/np.cos(np.pi*f*(1/2/500)))*np.cos(np.pi*f*12*(1/2/500)+p)
        #y = np.sin(np.pi * 500 *12 * (1 / 2 / f)) / (np.pi * 500  *12* (1 / 2 / f)) * np.tan(np.pi * 500 * (1 / 2 / f)) * np.sin(np.pi * 500 *12* (1 / 2 / f) + p)
        av = av+y**2/100
    l[i] = f
    g[i] = av

plt.scatter(l, g, s=5, color='red')
plt.grid(True)
plt.show()


