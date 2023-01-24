#8 серия пытается достать больше информации из полученных результатов (еще и фазу волны некоторой частоты)
#эта программа экспериментальная, для проверки некоторых концептов, вторая - более автоматизированная и по-другому продуманная

import numpy as np
import matplotlib.pyplot as plt
import random
import openpyxl

def randbin(P):
    # вероятность нуля
    return np.random.choice([0, 1], size=(1, 1), p=[P, 1 - P]).reshape(1)[0]
Nmax=35
#число задающих частот
Notgad=3
Nzad=3
#
frequency=10*10**3
Tperiod=1/frequency
phaseforB=0 # Это значение смещения фазы магнитного поля в радианах!!!
F = 5000 # дискретизация
koef = 1.4*10**15  # магнетон делить на планка
B=[0]*Nmax
A=[0]*Nmax
for i in range (Nzad):
    B[i] = randbin(0.5)*10**-12  # наше поле (его амплитуда)
Y = 1000 # (Y - частота дискретизации самого поля, один МАКСИМАЛЬНЫЙ период разделен на 1000 столбцов)
P=1000
NumberOfQuants=100
stattime=P*[0]
stat1=P*[0]
stat2=P*[0]
stat1nov=P*[0]
#
Numb=2 #(+1 - номер частоты показания)

Bpoleconst=2*10**-12

B[0]=1*10**-12
A[0]=1*10**-12
B[1]=0*10**-12
A[1]=0*10**-12
B[2]=1*10**-12
A[2]=1*10**-12

JU=4 #описано ниже
#перебор фаз начала
for v in range (P):
    SumPhase=  0
    PhaseForB=v/P*2*np.pi/(Numb+1)           #2pi - наибольший период
    for i in range (Y):  # (Y - частота дискретизации самого поля, один Максимальный период разделен на 1000 столбцов)
        #моделирование сигнала в точке
        signal = 0
        for j in range(Notgad):
            signal = signal + A[j] * np.sin(i / (Y / (j + 1)) * 2 * np.pi + PhaseForB*(j+1)) +\
                     B[j] * np.cos(i / (Y / (j + 1)) * 2 * np.pi + PhaseForB*(j+1))
        signal = signal + Bpoleconst

        if (i % int(Y / (Numb + 1)) <= int(Y / (Numb + 1)) / 2):
            SumPhase = SumPhase + koef / frequency / Y * (
                signal)
        if (i % int(Y / (Numb + 1)) > int(Y / (Numb + 1)) / 2):
            SumPhase = SumPhase - koef / frequency / Y * (
                signal)

    SumPhase = np.pi/4+SumPhase*JU   # ВАЖНО Одного пробега по самому большому периоду мало, надо собирать статистику в течении
    # бОльшего времени, чтобы кубит был к ней более чувствителен
    stat2[v] = SumPhase - np.pi / 4
    schet = 0
    for i in range(NumberOfQuants):
        schet = schet + 1 - randbin(np.cos(SumPhase) * np.cos(SumPhase))
    SumPhase = np.arccos(np.sqrt(schet / NumberOfQuants))

    stattime[v] = v/P*2*np.pi #/(Numb+1)
    stat1[v]=SumPhase-np.pi/4

for i in range(Y):
     sum=0
     for d in range (-20,20):
         sum=sum+stat1[(i+d)%Y]
     stat1nov[i]=sum/40

plt.scatter(stattime, stat1nov, s=5, color='green')
plt.scatter(stattime, stat2, s=5, color='red')
#plt.scatter(stattime, stat1, s=5, color='blue')
plt.grid(True)

plt.show()