import numpy as np
import matplotlib.pyplot as plt
import math
import random


def randbin(p):
    # вероятность нуля
    return np.random.choice([0, 1], size=(1, 1), p=[p, 1 - p]).reshape(1)[0]


Nmax = 3
frequency = 30.0 * 10 ** 3  # 10-50 на 10**3 диапазон считываемых частот, диапазон промежутков времени
# - 10**-4 - 0,2*10**-4
LowerBorderFr = 5 * 10 ** 3
HigherBorderFr = 35 * 10 ** 3
PhaseforB = 0  # Это значение смещения фазы магнитного поля в радианах потом будет меняться рандомно
# (в данном случае, в другом - системно)
Bparasite = 0.0 * 10 ** -12  # паразитное B
koef = 1.4 * 10 ** 15  # магнетон делить на планка
K = 2.0 * 10 ** -12  # наше поле (его амплитуда)
# B0 = 5.6*10**-12  # 5,6*10**-12 - максимум
tizm = 5 * 10 ** -4  # время снятия
U = 100  # количество экспериментов для снятия средней !квадрата! набежавшей фазы при одной частоте поворота
F = 200  # кол-во точек с первого раза
l = [0] * F
g = [0] * F

B = [0] * Nmax
A = [0] * Nmax

NumberOfQuants = 100

A[0] = 2.0 * 10 ** -12
B[0] = 2.0 * 10 ** -12
A[1] = 0 * K
B[1] = 0 * K
A[2] = 0 * K
B[2] = 0 * K

# for i in range(Nmax):
#    B[i] = K * randbin(0.5)  # наше поле (его амплитуда)
#    A[i] = K * randbin(0.5)  # наше поле (его амплитуда)


# цикл i - строительство графика
for i in range(F):
    print(i / F * 100, '%')
    CurrentFrequency = i / F * (
                HigherBorderFr - LowerBorderFr) + LowerBorderFr  # Перебор частот от нижней границы до верхней
    AverageSqPhase = 0

    for k in range(U):

        PhaseforB = np.pi * 2 * k / U  #random.random()  # (равные времена)

        SumPhase = 0
        for t in range (2000):
            signal = 0
            for index in range (Nmax):
                signal=signal \
                       + tizm / 2000 * koef * A[index] * np.sin(t / 2000 * tizm * frequency * (index+1) * 2 * np.pi + PhaseforB * (index+1)) \
                       + tizm / 2000 * koef * B[index] * np.sin(t / 2000 * tizm * frequency * (index+1) * 2 * np.pi + PhaseforB * (index+1))
            if ((t-0.25*int(2000/(tizm*CurrentFrequency))) // (0.5*int(2000/(tizm*CurrentFrequency)))) % 2 == 0:
                signal = signal*(-1)

            SumPhase = SumPhase+signal

        AverageSqPhase = AverageSqPhase + SumPhase ** 2
    l[i] = AverageSqPhase / U
    g[i] = (LowerBorderFr + (HigherBorderFr - LowerBorderFr) / F * i)  # /frequency

plt.scatter(g, l, s=5, color='blue')
plt.grid(True)
plt.show()