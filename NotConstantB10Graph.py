import numpy as np
import matplotlib.pyplot as plt
import random
from scipy import integrate


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
        def f(t):

            # Заготовка под кручение
            x = t  # + 1/frequency/(Numb+1)/4
            count = 0
            while x >= 1 / (CurrentFrequency * 2):
                x = x - 1 / (CurrentFrequency * 2)
                count += 1

            # Значение сигнала в точке
            signal = 0
            for j in range(Nmax):
                signal = signal \
                         + koef * A[j] * np.sin(frequency * (j + 1) * t * 2 * np.pi + PhaseforB * (j + 1))\
                         + koef * B[j] * np.cos(frequency * (j + 1) * t * 2 * np.pi + PhaseforB * (j + 1))
            signal = signal + koef * Bparasite
            # Значение сигнала в точке

            # Кручение
            if count % 2 == 0:
                return signal * -1
            if count % 2 == 1:
                return signal * 1
        SumPhase, err = integrate.quad(f, 0, tizm)
        AverageSqPhase = AverageSqPhase + SumPhase ** 2
    l[i] = AverageSqPhase / U
    g[i] = (LowerBorderFr + (HigherBorderFr - LowerBorderFr) / F * i)  # /frequency

plt.scatter(g, l, s=5, color='blue')
plt.grid(True)
plt.show()