import numpy as np
import matplotlib.pyplot as plt

def randbin(P):
    # вероятность нуля
    return np.random.choice([0, 1], size=(1, 1), p=[P, 1 - P]).reshape(1)[0]

def C(n, k):
    if 0 <= k <= n:
        nn = 1
        kk = 1
        for s in range(1, min(k, n - k) + 1):
            nn *= n
            kk *= s
            n -= 1
        return nn // kk
    else:
        return 0

frequency=20*10**3
Tperiod=1/frequency
phaseforB=1.5 # Это значение смещения фазы магнитного поля в радианах!!!
Bparasite=1.0*10**-12  # паразитное B
F = 5000 # дискретизация
koef = 1.4*10**15  # магнетон делить на планка
a = 0  # кол-во нулей в одной серии
B = 2.0*10**-12  # наше поле (его амплитуда)
B0 = 5.6*10**-12  # 5,6*10**-12 - максимум
t = 2*10**-4  # время первого снятия
l = [1/F]*int(1000*(5-0.2))  # первое распределение (юниформ)




g = [0]*int(1000*(5-0.2))



Y = 1000 # (Y - частота дискретизации самого поля, один период разделен на 1000 столбцов)
for i in range (int(1000*(5-0.2))):
    Tperevorot=(i/1000+0.2)*Tperiod
    g[i]=0.2+i/1000
    if ((i+200)%500!=0):
        l[i]=(1-1/(np.cos(np.pi*frequency*Tperevorot)))**2*(np.sin(np.pi*frequency*t)/(np.pi*frequency*t)*np.cos(phaseforB*np.pi+np.pi*frequency*t))**2/2
plt.scatter(g, l, s=10, color='blue')



plt.grid(True)
plt.show()