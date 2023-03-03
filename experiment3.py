import numpy as np
import matplotlib.pyplot as plt
import random

K = 1000

l = [0] * K
g = [0] * K
koef = 1.4 * 10 ** 15  # магнетон делить на планка
tizm = 5 * 10 ** -4
fr=10000
for i in range (K):
    f = 2000+i/K*10000
    y = (np.sqrt(2)*10**-12 * koef * tizm)**2*np.sin(fr*np.pi*(tizm*fr*2)*(1/2/f))**2/(2*(fr*np.pi*(tizm*fr*2)*(1/2/f))**2)*(1-1/np.cos(fr*np.pi*(1/2/f)))**2
    #y = ((2 * np.sqrt(2) * 10 ** -12 * koef * tizm / 2.1 * (1 / 1)) ** 2) * np.exp(-(f - 10000/1) ** 2 / (2 * (800 / 1) ** 2)) + \
        #((2 * np.sqrt(2) * 10 ** -12 * koef * tizm / 2.1 * (1 / 3)) ** 2) * np.exp(-(f - 10000/3) ** 2 / (2 * (800 / 3) ** 2)) + \
        #((2 * np.sqrt(2) * 10 ** -12 * koef * tizm / 2.1 * (1 / 5)) ** 2) * np.exp(-(f - 10000/5) ** 2 / (2 * (800 / 5) ** 2))

    l[i] = f
    g[i] = y

plt.scatter(l, g, s=5, color='red')
plt.grid(True)





#def mapping1(x, Ampl, coord):
#    return (Ampl * koef * tizm / 2.1 * (1 / 1)) ** 2 * np.exp(-(x - coord / 1) ** 2 / (2 * (800 / 1) ** 2)) + \
#           (Ampl * koef * tizm / 2.1 * (1 / 3)) ** 2 * np.exp(-(x - coord / 3) ** 2 / (2 * (800 / 3) ** 2)) + \
#           (Ampl * koef * tizm / 2.1 * (1 / 5)) ** 2 * np.exp(-(x - coord / 5) ** 2 / (2 * (800 / 5) ** 2)) + \
#           (Ampl * koef * tizm / 2.1 * (1 / 7)) ** 2 * np.exp(-(x - coord / 7) ** 2 / (2 * (800 / 3) ** 2))


#stattime=[0]*1000
#stat2=[0]*1000
#for i in range ( 1000):
#    stattime[i] = np.exp((1000-i)/1000*np.log(10)+i/1000*np.log(50000))
#    #stat2[i] = mapping1(stattime[i],2*10**-2,20)
#    stat2[i] = mapping1(stattime[i], 2*np.sqrt(2)*10**-12, 10*10**3)
#plt.scatter(stattime, stat2, s=5, color='blue')

plt.show()