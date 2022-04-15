import numpy as np
import matplotlib.pyplot as plt
import random


frequency=10*10**3
Tperiod=1/frequency
phaseforB=0 # Это значение смещения фазы магнитного поля в радианах!!!
Bparasite=0*10**-12  # паразитное B
F = 5000 # дискретизация
koef = 1.4*10**15  # магнетон делить на планка
B=[0]*6
B[0] = 1.0*10**-12  # наше поле (его амплитуда)
B[1] = 0.0*10**-12  # наше поле (его амплитуда)
B[2] = 1.0*10**-12  # наше поле (его амплитуда)
B[3] = 0.0*10**-12  # наше поле (его амплитуда)
B[4] = 0.0*10**-12  # наше поле (его амплитуда)
B[5] = 0.0*10**-12  # наше поле (его амплитуда)
B0 = 5.6*10**-12  # 5,6*10**-12 - максимум
t = 4*10**-4  # время первого снятия

Y = 1000 # (Y - частота дискретизации самого поля, один МАКСИМАЛЬНЫЙ период разделен на 1000 столбцов)
stat=[0]*int(t * frequency) * Y
stat2=[0]*int(t * frequency) * Y

AverageSquarePhase=[0]*6
P=300
for o in range (6): # перебор частот поворотов, от frequency lj 5xfrequency
    for v in range(P):
        phaseforB = v/P*2
        SumPhase = 0
        for i in range(int(t * frequency) * Y):  # (Y - частота дискретизации самого поля, один Максимальный период разделен на 1000 столбцов)
            if (i%int(Y/(o+1))<=int(Y/(o+1))/2):
                SumPhase = SumPhase - koef * Bparasite * Tperiod / Y + koef / frequency / Y * (
                B[0] * np.sin(i / Y * 2 * np.pi + phaseforB*np.pi) + B[1] * np.sin(i / (Y / 2) * 2 * np.pi + phaseforB*2*np.pi) +
                B[2] * np.sin(i / (Y / 3) * 2 * np.pi + phaseforB*3*np.pi) + B[3] * np.sin(i / (Y / 4) * 2 * np.pi + phaseforB*4*np.pi) +
                B[4] * np.sin(i / (Y / 5) * 2 * np.pi + phaseforB*5*np.pi))
            if (i%int(Y/(o+1))>int(Y/(o+1))/2):
                SumPhase = SumPhase + koef * Bparasite * Tperiod / Y - koef / frequency / Y * (
                B[0] * np.sin(i / Y * 2 * np.pi + phaseforB*np.pi) + B[1] * np.sin(i / (Y / 2) * 2 * np.pi + phaseforB*2*np.pi) +
                B[2] * np.sin(i / (Y / 3) * 2 * np.pi + phaseforB*3*np.pi) + B[3] * np.sin(i / (Y / 4) * 2 * np.pi + phaseforB*4*np.pi) +
                B[4] * np.sin(i / (Y / 5) * 2 * np.pi + phaseforB*5*np.pi))

            #stat2[i] = i
            #stat[i] = SumPhase
        #if v==0:
            #plt.scatter(stat2, stat, s=5, color='blue')
            #plt.grid(True)
            #plt.show()
        #print(SumPhase)


        AverageSquarePhase[o]=AverageSquarePhase[o]+SumPhase*SumPhase/P
            #stat[i]=SumPhase

        #print(SumPhase)
    #print(AverageSquarePhase)

for i in range (6):
    print(AverageSquarePhase)
    print(np.sqrt(AverageSquarePhase[i]/koef/koef/t/t/2*np.pi*np.pi))

