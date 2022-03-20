import numpy as np
import math
import matplotlib.pyplot as plt
import random


frequency = 15*10**3  # 10-50 на 10**3 диапазон считываемых частот, диапазон промежутков времени - 10**-4 - 0,2*10**-4
LowerBorderFr = 10*10**3
HigherBorderFr = 50*10**3

phaseforB = 0  # Это значение смещения фазы магнитного поля в радианах потом будет меняться!!!
Bparasite = 0.0*10**-12  # паразитное B
koef = 1.4*10**15  # магнетон делить на планка
F = 200  # кол-во точек с первого раза
B = 3.0*10**-12  # наше поле (его амплитуда)
B0 = 5.6*10**-12  # 5,6*10**-12 - максимум
t = 2*10**-4  # время снятия
l = [0]*F
g = [0]*F
# random.uniform(A, B)
N = 10  # количество переворотов - четное число!
Y = 100  # (Y - частота дискретизации самого поля, один период разделен на 100 столбцов)
U = 100  # количество экспериментов для снятия средней набежавшей фазы при одной частоте

for j in range(F):
    print(j)
    Tau = 0.5/(LowerBorderFr+float(HigherBorderFr-LowerBorderFr)/F*j)  # Перебор тау для частот от Нижней границы до
    #Tau = 0.5 / frequency
    # Верхней на 10**3
    AveragePhase = 0
    for k in range(U):
        SumPhase = 0
        phaseforB = random.random()*2
        #phaseforB = float(k)/U*2
        #phaseforB = -0.5
        stat = [0]*math.ceil(frequency*N*Tau*Y)
        stat2 = [0]*math.ceil(frequency*N*Tau*Y)
        for i in range(math.ceil(frequency*N*Tau*Y)):  # (Y - частота дискретизации самого поля, один период разделен
            # на 100 столбцов) Tau/Tperiod=Itau/Y
            if (i - int(Tau*frequency*Y / 2)) % (2*Tau*frequency*Y) < Tau*frequency*Y:
                SumPhase = SumPhase - koef * Bparasite / (Y*frequency) - koef * B * np.sin(
                        i / Y * 2 * np.pi +
                        phaseforB * np.pi) / (Y*frequency)

            if (i - int(Tau*frequency*Y/2)) % (2* Tau*frequency*Y) >= Tau*frequency*Y:
                SumPhase = SumPhase + koef * Bparasite / (Y * frequency) + koef * B * np.sin(
                    i / Y * 2 * np.pi +
                    phaseforB * np.pi) / (Y * frequency)

            '''
            stat2[i]=i
            stat[i]=SumPhase
        plt.scatter(stat2, stat, s=5, color='blue')
        plt.grid(True)
        plt.show()
        '''
        AveragePhase = AveragePhase+SumPhase**2
    AveragePhase = AveragePhase/U
    l[j] = AveragePhase
    g[j] = (LowerBorderFr+float(HigherBorderFr-LowerBorderFr)/F*j)/frequency

plt.scatter(g, l, s=5, color='blue')
plt.grid(True)
plt.show()
