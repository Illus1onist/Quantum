import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random


# Референс
# df = pd.DataFrame({'day_number': [1,2, 3, 4], 'orders': [8,7, 7, 11]})
# df.loc[len(df.index)] = [2, 8]
# df.plot(x='day_number', y='orders', kind="scatter")
# plt.show()

def randbin(p):
    # вероятность нуля
    return np.random.choice([0, 1], size=(1, 1), p=[p, 1 - p]).reshape(1)[0]


Nmax = 3
frequency = 10.0 * 10 ** 3  # 10-50 на 10**3 диапазон считываемых частот, диапазон промежутков времени
# - 10**-4 - 0,2*10**-4
PhaseforB = 0  # Это значение смещения фазы магнитного поля в радианах потом будет меняться рандомно
# (в данном случае, в другом - системно)
Bparasite = 0.0 * 10 ** -12  # паразитное B
koef = 1.4 * 10 ** 15  # магнетон делить на планка
K = 2.0 * 10 ** -12  # наше поле (его амплитуда)
# B0 = 5.6*10**-12  # 5,6*10**-12 - максимум
tizm = 5 * 10 ** -4  # время снятия
U = 100  # количество экспериментов для снятия средней !квадрата! набежавшей фазы при одной частоте поворота
F = 30  # кол-во точек с первого раза
df = pd.DataFrame({'frequency_axis': [], 'giveaway_axis': []})

# Количество кубитов
NumberOfQuants = 100

# Задача поля прямо, или фиговым рандомом.
B = [0] * Nmax
A = [0] * Nmax

A[0] = 1.0 * 10 ** -12
B[0] = 1.0 * 10 ** -12
A[1] = 0 * K
B[1] = 0 * K
A[2] = 0 * K
B[2] = 0 * K


# for i in range(Nmax):
#    B[i] = K * randbin(0.5)  # наше поле (его амплитуда)
#    A[i] = K * randbin(0.5)  # наше поле (его амплитуда)


# цикл i - строительство графика
def function(LowerBorderFr, HigherBorderFr, F):
    for i in range(F):
        print(i / F * 100, '%')
        CurrentFrequency = i / F * (
                HigherBorderFr - LowerBorderFr) + LowerBorderFr  # Перебор частот от нижней границы до верхней
        AverageSqPhase = 0

        for k in range(U):

            PhaseforB = np.pi * 2 * random.random()  # (равные времена)

            SumPhase = 0
            for t in range(2000):
                signal = 0
                for index in range(Nmax):
                    signal = signal \
                             + tizm / 2000 * koef * A[index] * np.sin(
                        t / 2000 * tizm * frequency * (index + 1) * 2 * np.pi + PhaseforB * (index + 1)) \
                             + tizm / 2000 * koef * B[index] * np.cos(
                        t / 2000 * tizm * frequency * (index + 1) * 2 * np.pi + PhaseforB * (index + 1))
                if ((t - 0.25 * int(2000 / (tizm * CurrentFrequency))) // (
                        0.5 * int(2000 / (tizm * CurrentFrequency)))) % 2 == 0:
                    signal = signal * (-1)

                SumPhase = SumPhase + signal

            # Кубитный модуль
            #JU = 0.4
            #SumPhase = SumPhase * JU + np.pi / 4
            #schet = 0
            #for quant in range(NumberOfQuants):
            #    schet = schet + 1 - randbin(np.cos(SumPhase) * np.cos(SumPhase))
            #SumPhase = np.arccos(np.sqrt(schet / NumberOfQuants))
            #SumPhase = (SumPhase - np.pi / 4) / JU
            # Запись с кубитами

            AverageSqPhase = AverageSqPhase + SumPhase ** 2
        df.loc[len(df.index)] = [(LowerBorderFr + (HigherBorderFr - LowerBorderFr) / F * i), AverageSqPhase / U]


picsmassive = []


def findpicks(width):
    dfserv = pd.DataFrame({'frequency_axis': [], 'giveaway_axis': []})
    dfserv.frequency_axis = df.frequency_axis.copy()
    dfserv.giveaway_axis = df.giveaway_axis.copy()
    maximum = max(dfserv["giveaway_axis"])
    flag = 0
    while max(dfserv["giveaway_axis"]) > maximum / 30:
        picsmassive.append(dfserv.idxmax()[1])
        currentmaxlocation = dfserv.loc[picsmassive[flag]][0]
        for s in range(len(dfserv.index)):
            if (currentmaxlocation - width) <= dfserv.frequency_axis[s] <= (currentmaxlocation + width):
                dfserv.giveaway_axis[s] = 0
        flag = flag + 1

    print(picsmassive)


function(2000, 12000, 50)
df.plot(x="frequency_axis", y="giveaway_axis", s=5, kind="scatter")
plt.show()

#findpicks(1000)
function(9000, 11000, 100)
df.plot(x="frequency_axis", y="giveaway_axis", s=5, kind="scatter")
plt.show()

#for i in range(len(picsmassive)):
    #function((df.frequency_axis[picsmassive[i]] - 1000), (df.frequency_axis[picsmassive[i]] + 1000), 30)
    #df.plot(x="frequency_axis", y="giveaway_axis", s=5, kind="scatter")
    #plt.show()

df.plot(x="frequency_axis", y="giveaway_axis", s=5, kind="scatter")
plt.show()
