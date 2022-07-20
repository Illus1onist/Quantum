#7 серия отличается от шестой тем, что количество коэффициентов увеличено до 35x35, сами коэффициенты помещены в эксель,
# появилась возможность изменения количества частот задачи сигнала и частот его отгадки. При этом стоит заметить, что
# коэффициенты в экселе считаются не программой а теоретическим способом, так как програмный показал себя ненадежным.
# Программа signal дает параболический сигнал, а F - обычный сгнал на гармониках

import numpy as np
import matplotlib.pyplot as plt
import random
import openpyxl

def randbin(P):
    # вероятность нуля
    return np.random.choice([0, 1], size=(1, 1), p=[P, 1 - P]).reshape(1)[0]
Nmax=35
Notgad=3
Nzad=3
frequency=10*10**3
Tperiod=1/frequency
phaseforB=0 # Это значение смещения фазы магнитного поля в радианах!!!
Bparasite=0*10**-12  # паразитное B
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
Numb=0 #(+1 - номер частоты показания)
Bpoleconst=0*10**-12
B[0]=1*10**-12
A[0]=1*10**-12
B[1]=0*10**-12
A[1]=0*10**-12
B[2]=1*10**-12
A[2]=1*10**-12


#перебор фаз начала
for v in range (P):
    SumPhase=0
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

    stattime[v] = v/P*2*np.pi #/(Numb+1)
    stat1[v]=SumPhase-Bpoleconst/frequency

plt.scatter(stattime, stat1, s=5, color='blue')
plt.grid(True)

plt.show()