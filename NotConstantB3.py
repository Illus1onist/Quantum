import numpy as np
import math
import matplotlib.pyplot as plt
import random


frequency = 25.0*10**3  # 10-50 на 10**3 диапазон считываемых частот, диапазон промежутков времени - 10**-4 - 0,2*10**-4
LowerBorderFr = 70*10**3
HigherBorderFr = 80*10**3
phaseforB = 0  # Это значение смещения фазы магнитного поля в радианах потом будет меняться!!!
Bparasite = 0.5*10**-12  # паразитное B
koef = 1.4*10**15  # магнетон делить на планка
F = 400  # кол-во точек с первого раза
B = 3.0*10**-12  # наше поле (его амплитуда)
B0 = 5.6*10**-12  # 5,6*10**-12 - максимум
t = 5*10**-4  # время снятия
l = [0]*F
g = [0]*F
# rando m.uniform(A, B)
Y = 200  # (Y - частота дискретизации самого поля, один период разделен на 100 столбцов)
U = 100  # количество экспериментов для снятия средней !квадрата! набежавшей фазы при одной частоте поворота



#цикл j - строительство графика
for j in range(F):
    print(j)
    Tau = 0.5/(LowerBorderFr+(HigherBorderFr-LowerBorderFr)/F*j)  # Перебор тау (пол периода) для частот от Нижней границы до верхней
    AverageSqPhase = 0
    for k in range(U):
        SumPhase = 0
        phaseforB = random.random()*2 #(равные времена)
        for i in range(int(Y*t*frequency)):
            if i%int(2*Tau*frequency*Y)<=int(Tau*frequency*Y):
                SumPhase = SumPhase - koef * Bparasite / (Y*frequency) \
                - 1 * koef * B * np.sin(1 * i / Y * 2 * np.pi + 1 * phaseforB * np.pi) / (Y * frequency)\
                - 2 * koef * B * np.sin(2 * i / Y * 2 * np.pi + 2 * phaseforB * np.pi) / (Y * frequency)\
                - 3 * koef * B * np.sin(3 * i / Y * 2 * np.pi + 3 * phaseforB * np.pi) / (Y * frequency)
            if i%int(2*Tau*frequency*Y)>int(Tau*frequency*Y):
                SumPhase = SumPhase + koef * Bparasite / (Y * frequency) \
                + 1 * koef * B * np.sin(1 * i / Y * 2 * np.pi + 1 * phaseforB * np.pi) / (Y * frequency)\
                + 2 * koef * B * np.sin(2 * i / Y * 2 * np.pi + 2 * phaseforB * np.pi) / (Y * frequency)\
                + 3 * koef * B * np.sin(3 * i / Y * 2 * np.pi + 3 * phaseforB * np.pi) / (Y * frequency)

        AverageSqPhase = AverageSqPhase+SumPhase**2
    l[j] = AverageSqPhase/U
    g[j] = (LowerBorderFr+float(HigherBorderFr-LowerBorderFr)/F*j) #/frequency

    '''
    max=0
    maxi=0
    y=0
    NewLowerBorderFr=LowerBorderFr
    NewHigherBorderFr=HigherBorderFr
    for j in range(F):
        if l[j] > max:
            max = l[j]
            maxi=j
    schetchikdlyfr = maxi
    while (y == 0):
        if (l[schetchikdlyfr]<0.1*max or schetchikdlyfr==0):
            NewLowerBorderFr = LowerBorderFr+(HigherBorderFr-LowerBorderFr)/F*schetchikdlyfr
            break
        schetchikdlyfr = schetchikdlyfr - 1

    schetchikdlyfr = maxi

    while (y == 0):
        if (l[schetchikdlyfr]<0.1*max or schetchikdlyfr == F - 1):
            NewHigherBorderFr = LowerBorderFr+(HigherBorderFr-LowerBorderFr)/F*schetchikdlyfr
            break
        schetchikdlyfr = schetchikdlyfr + 1
    print(NewLowerBorderFr,' ',NewHigherBorderFr)
    HigherBorderFr=NewHigherBorderFr
    LowerBorderFr=NewLowerBorderFr
    '''

plt.scatter(g, l, s=5, color='blue')
plt.grid(True)
plt.show()