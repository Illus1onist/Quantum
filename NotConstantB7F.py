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
Notgad=20
Nzad=30

frequency=10*10**3
Tperiod=1/frequency
phaseforB=0 # Это значение смещения фазы магнитного поля в радианах!!!
Bparasite=0*10**-12  # паразитное B
F = 5000 # дискретизация
koef = 1.4*10**15  # магнетон делить на планка
B=[0]*Nmax
for i in range (Nzad):
    B[i] = randbin(0.5)*10**-12  # наше поле (его амплитуда)
B0 = 5.6*10**-12  # 5,6*10**-12 - максимум
t = 1*10**-4  # время первого снятия

Y = 1000 # (Y - частота дискретизации самого поля, один МАКСИМАЛЬНЫЙ период разделен на 1000 столбцов)
AverageSquarePhase=[0]*Notgad
P=100
NumberOfQuants=100
for o in range (Notgad): # перебор частот поворотов
    for v in range(P):
        phaseforB = random.random()*2
        SumPhase = 0
        for i in range(int(t * frequency) * Y):  # (Y - частота дискретизации самого поля, один Максимальный период разделен на 1000 столбцов)
            signal = 0
            for j in range(Notgad):
                signal = signal + B[j] * np.sin(i / (Y / (j + 1)) * 2 * np.pi + phaseforB * (j + 1) * np.pi)
            if (i%int(Y/(o+1))<=int(Y/(o+1))/2):
                SumPhase = SumPhase - koef * Bparasite * Tperiod / Y + koef / frequency / Y * (
                signal)
            if (i%int(Y/(o+1))>int(Y/(o+1))/2):
                SumPhase = SumPhase + koef * Bparasite * Tperiod / Y - koef / frequency / Y * (
                signal)
        schet=0

        #for i in range(NumberOfQuants):
        #    schet=schet+1-randbin(np.cos(SumPhase) * np.cos(SumPhase))
        #SumPhase=np.arccos(np.sqrt(schet/NumberOfQuants))

        AverageSquarePhase[o]=AverageSquarePhase[o]+SumPhase*SumPhase/P
    print(0)

matritsakoeffitsientow=[[0]*Notgad for i in range (Notgad)]


wb = openpyxl.load_workbook("KOEFS.xlsx")
sheet = wb.active

for i in range (Notgad):
    for j in range(Notgad):
        matritsakoeffitsientow[i][j]=sheet.cell(row = 41+i+1, column = j+1).value


solution = np.linalg.inv(matritsakoeffitsientow)@AverageSquarePhase
for i in range (Notgad):
    solution[i]=np.sqrt(abs(solution[i])/koef**2/t**2)

stat1=[0]*int(t * frequency) * Y
stat2=[0]*int(t * frequency) * Y
stattime=[0]*int(t * frequency) * Y
for i in range (int(t * frequency) * Y):
    stattime[i]=i
    signal = 0
    for j in range(Nzad):
        signal = signal + B[j] * np.sin(i / (Y / (j + 1)) * 2 * np.pi)
    stat1[i]=signal
    signal=0
    for j in range(Notgad):
        signal = signal + solution[j] * np.sin(i / (Y / (j + 1)) * 2 * np.pi)
    stat2[i]=signal#-stat1[i]

plt.scatter(stattime, stat1, s=5, color='blue')
plt.scatter(stattime, stat2, s=5, color='red')


plt.grid(True)

plt.show()