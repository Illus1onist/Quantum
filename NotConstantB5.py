import numpy as np
import matplotlib.pyplot as plt
import random
N=10
koeffitsienti=[[0]*N for i in range (N)]

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
        for l in range(o,N): # перебор частот, составляющих сигнал, от frequency до 6xfrequency
            print(l)
            for v in range(P):
                phaseforB = v/P*2
                SumPhaseA = 0
                SumPhaseB = 0
                for i in range(int(t * frequency) * Y):  # (Y - частота дискретизации самого поля, один Максимальный период разделен на 1000 столбцов)
                    if (i%int(Y/(g+1))<=int(Y/(g+1))/2):
                        SumPhaseA = SumPhaseA + 1/frequency / Y * (
                        np.sin(i / (Y / (o+1)) * 2 * np.pi + phaseforB * (o+1) * np.pi))
                    if (i%int(Y/(g+1))>int(Y/(g+1))/2):
                        SumPhaseA = SumPhaseA - 1/frequency / Y * (
                        np.sin(i / (Y / (o+1)) * 2 * np.pi + phaseforB * (o+1) * np.pi))

                for i in range(int(t * frequency) * Y):  # (Y - частота дискретизации самого поля, один Максимальный период разделен на 1000 столбцов)
                    if (i % int(Y / (g + 1)) <= int(Y / (g + 1)) / 2):
                        SumPhaseB = SumPhaseB - Bparasite / frequency / Y + 1/frequency / Y * (
                        np.sin(i / (Y / (l+1)) * 2 * np.pi + phaseforB * (l+1) * np.pi))
                    if (i % int(Y / (g + 1)) > int(Y / (g + 1)) / 2):
                        SumPhaseB = SumPhaseB + Bparasite / frequency / Y - 1/frequency / Y * (
                        np.sin(i / (Y / (l+1)) * 2 * np.pi + phaseforB * (l+1) * np.pi))
                koeffitsienti[o][l] = koeffitsienti[o][l]+SumPhaseB*SumPhaseA/P
            koeffitsienti[l][o] = koeffitsienti[o][l]

    for u in range(N):
        for v in range(N):
            koeffitsienti[u][v]=koeffitsienti[u][v]/(t)**2  #тут находится коэффициент типа 2/pi**2.

    for u in range(N):
        print(koeffitsienti[u])

    for u in range(N):
        for j in range(N):
            koeffitsienti[u][j] = 0
    print(0)
    print(0)

                #stat[i]=SumPhase

            #print(SumPhase)
        #print(AverageSquarePhase)