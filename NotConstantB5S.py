import numpy as np

import matplotlib.pyplot as plt
import random
N=35
koeffitsienti=[0]*N

frequency=10*10**3
phaseforB=0 # Это значение смещения фазы магнитного поля в радианах!!!
Bparasite=0*10**-12  # паразитное B
koef = 1.4*10**15  # магнетон делить на планка

B0 = 5.6*10**-12  # 5,6*10**-12 - максимум
t = 4*10**-4  # время первого снятия

Y = 1000 # (Y - частота дискретизации самого поля, один МАКСИМАЛЬНЫЙ период разделен на 1000 столбцов)

P=300
for g in range (N):
    for o in range (N): # перебор частот составляющих сигнал , от frequency до 6xfrequency

        for v in range(P):
            phaseforB = v/P*2
            SumPhaseA = 0
            for i in range(int(t * frequency) * Y):  # (Y - частота дискретизации самого поля, один Максимальный период разделен на 1000 столбцов)
                if (i%int(Y/(g+1))<=int(Y/(g+1))/2):
                    SumPhaseA = SumPhaseA + 1/frequency / Y * (
                    np.sin(i / (Y / (o+1)) * 2 * np.pi + phaseforB * (o+1) * np.pi))
                if (i%int(Y/(g+1))>int(Y/(g+1))/2):
                    SumPhaseA = SumPhaseA - 1/frequency / Y * (
                    np.sin(i / (Y / (o+1)) * 2 * np.pi + phaseforB * (o+1) * np.pi))

            koeffitsienti[o] = koeffitsienti[o]+SumPhaseA*SumPhaseA/P

    for u in range(N):
        koeffitsienti[u]=koeffitsienti[u]/(t)**2  #тут находится коэффициент типа 2/pi**2.
    print(koeffitsienti)
    for u in range(N):
        koeffitsienti[u] = 0