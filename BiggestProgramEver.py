import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.optimize import curve_fit

Nmax = 5
df = pd.DataFrame({'frequency_axis': [], 'giveaway_axis': []})
koef = 1.4 * 10 ** 15
T = 0


class Signal:
    def __init__(self):
        self.A = [0] * Nmax
        self.B = [0] * Nmax
        self.frequency = 20 * 10 ** 3
        self.A[0] = 2.0 * 10 ** -12
        #self.B[1] = 2.0 * 10 ** -12
        #self.A[4] = 2.0 * 10 ** -12
        self.PhaseforB = random.random() * 2 * np.pi

    def signal(self, t):
        summ = 0
        for d in range(Nmax):
            summ += self.A[d] * koef * np.sin(self.frequency * (d + 1) * t * 2 * np.pi + self.PhaseforB * (d + 1)) + self.B[d]*koef * np.cos(
                self.frequency * (d + 1) * t * 2 * np.pi  + self.PhaseforB * (d + 1))
        return summ


class Qubit:
    JU = 0.4
    Phase = 0

    def __init__(self):
        self.Phase = np.pi / 2
        self.JU = 0.4

    def make_ready(self):
        self.Phase = np.pi / 2

    @staticmethod
    # Тут плохо сделан о избавление от постоянной составляющей
    def apply_gate_pi(startT, finishT, currentT, F):
        if (currentT - startT + 1 / (4 * F)) // (1 / (2*F)) % 2 == 0:
            return 1
        else:
            return -1

    def accumulate_phase(self, startT, finishT, F, Sig):
        otrezok = finishT-startT
        summ = 0
        for s in range(1000):
            summ += self.apply_gate_pi(startT, finishT, startT + s * (otrezok / 1000), F) \
            * Sig.signal(startT + s * (otrezok / 1000)) \
            * (otrezok / 1000)
        self.Phase = self.Phase+summ*self.JU

    def read(self):
        p=np.cos(self.Phase)**2
        return(1 - np.random.choice([0, 1], size=(1, 1), p=[p, 1 - p]).reshape(1)[0])


picsmassive = []


def findpicks(frame):
    # копирование датафрейма
    dfserv = pd.DataFrame({'frequency_axis': [], 'giveaway_axis': []})
    dfserv.frequency_axis = frame.frequency_axis.copy()
    dfserv.giveaway_axis = frame.giveaway_axis.copy()

    maximum = max(dfserv["giveaway_axis"])
    flag = 0
    normal=2000
    while max(dfserv["giveaway_axis"]) > maximum / 30:
        picsmassive.append(dfserv.idxmax()[1])
        currentmaxlocation = dfserv.loc[picsmassive[flag]][0]
        width=currentmaxlocation*0.1
        for s in range(len(dfserv.index)):
            if (currentmaxlocation - width) <= dfserv.frequency_axis[s] <= (currentmaxlocation + width):
                dfserv.giveaway_axis[s] = 0
        flag = flag + 1
        dfserv.plot(x="frequency_axis", y="giveaway_axis", s=5, kind="scatter")
        plt.show()
    print(picsmassive)


U = 100  # количество экспериментов для снятия средней !квадрата! набежавшей фазы при одной частоте поворота
tizm = 5 * 10 ** -4  # время снятия
Qubits = [Qubit] * 100
sig = Signal()


def function(LowerBorderFr, HigherBorderFr, F):
    global T
    for i in range(F):
        print(i / F * 100, '%')
        CurrentFrequency =  np.exp((F-i)/F*np.log(LowerBorderFr)+i/F*np.log(HigherBorderFr))
                            #i / F * (HigherBorderFr - LowerBorderFr) + LowerBorderFr  # Перебор частот от нижней границы до верхней

        AverageSqPhase = 0

        for k in range(U):

            for s in range(len(Qubits)):
                Qubits[s].make_ready(Qubits[s])
            #for s in range(len(Qubits)):
            #    Qubits[s].accumulate_phase(Qubits[s], T, T+tizm, CurrentFrequency, sig)
            Qubits[0].accumulate_phase(Qubits[0], T, T + tizm, CurrentFrequency, sig)
            for s in range(len(Qubits)-1):
                Qubits[s+1].Phase = Qubits[0].Phase

            # Набегание времени за время набегания фазы...
            T = T + tizm

            # Считывание кубитов с набежавшими фазами
            schet = 0
            for s in range(len(Qubits)):
                schet = schet + Qubits[s].read(Qubits[s])
            SumPhase = (np.arccos(np.sqrt(schet / len(Qubits))) - np.pi / 2) / Qubits[0].JU
            AverageSqPhase = AverageSqPhase + SumPhase ** 2

            # Время отдыха между измерениями
            j = random.random() * 0.003
            T = T + j
            # Время отдыха между измерениями

        df.loc[len(df.index)] = [CurrentFrequency, AverageSqPhase / U]


def mapping1(x, Ampl, coord):
    return (Ampl * koef * tizm)**2*np.sin(coord*np.pi*tizm*coord*2*(1/2/x))**2/(2*(coord*np.pi*tizm*coord*2*(1/2/x))\
                                                                                  **2)*(1-1/np.cos(coord*np.pi*(1/2/x)))**2

    #(Ampl * koef * tizm / 2.1 * (1 / 1)) ** 2 * np.exp(-(x - coord / 1) ** 2 / (2 * (800 / 1) ** 2)) + \
           #(Ampl * koef * tizm / 2.1 * (1 / 3)) ** 2 * np.exp(-(x - coord / 3) ** 2 / (2 * (800 / 3) ** 2)) + \
           #(Ampl * koef * tizm / 2.1 * (1 / 5)) ** 2 * np.exp(-(x - coord / 5) ** 2 / (2 * (800 / 5) ** 2)) + \
           #(Ampl * koef * tizm / 2.1 * (1 / 7)) ** 2 * np.exp(-(x - coord / 7) ** 2 / (2 * (800 / 7) ** 2))

    #(Ampl * koef * tizm)**2*np.sin(coord*np.pi*tizm*fr*2*(1/2/x))**2/(2*(coord*np.pi*tizm*fr*2*(1/2/x))\
                                                                                  #**2)*(1-1/np.cos(coord*np.pi*(1/2/x)))**2

args=[[0]*2 for i in range(10)]
def coefsoffiltrfunctions(frame, N):
    # копирование датафрейма
    dfserv = pd.DataFrame({'frequency_axis': [], 'giveaway_axis': []})
    dfserv.frequency_axis = frame.frequency_axis.copy()
    dfserv.giveaway_axis = frame.giveaway_axis.copy()
    for i in range (N):
        print(i)
        arg, covar = curve_fit(mapping1, dfserv.frequency_axis, dfserv.giveaway_axis, [2*10**-12, 20000])
        #bounds = ([0.5 * 10 ** -12, 100], [5 * 10 ** -12, 100000])
        args[i][0] = arg[0]
        args[i][1] = arg[1]
        for j in range (len(dfserv)):
            dfserv.giveaway_axis[j] = dfserv.giveaway_axis[j] - mapping1(dfserv.frequency_axis[j], arg[0], arg[1])





function(5000, 22000, 50)
print(T)
df.plot(x="frequency_axis", y="giveaway_axis", s=5, kind="scatter")

#findpicks(df)

#for i in range(len(picsmassive)):
#    function((df.frequency_axis[picsmassive[i]] - 1000), (df.frequency_axis[picsmassive[i]] + 1000), 40)
#    df.plot(x="frequency_axis", y="giveaway_axis", s=5, kind="scatter")


coefsoffiltrfunctions(df, 4)

stattime = [0] * 1000
stat1 = [0] * 1000
stat2 = [0] * 1000
stat3 = [0] * 1000
stat4 = [0] * 1000
stat0 = [0] * 1000
for i in range (1000):
    stattime[i] = np.exp((1000-i)/1000*np.log(5000)+i/1000*np.log(22000))
    stat0[i] = mapping1(stattime[i], 2*10**-12, 20000)
    stat1[i] = mapping1(stattime[i], args[0][0], args[0][1])
    stat2[i] = mapping1(stattime[i], args[1][0], args[1][1])
    stat3[i] = mapping1(stattime[i], args[2][0], args[2][1])
    stat4[i] = mapping1(stattime[i], args[3][0], args[3][1])
plt.scatter(stattime, stat0, s=5, color='cyan')
plt.scatter(stattime, stat1, s=5, color='red')
plt.scatter(stattime, stat2, s=5, color='green')
plt.scatter(stattime, stat3, s=5, color='orange')
plt.scatter(stattime, stat4, s=5, color='purple')
df.plot(x="frequency_axis", y="giveaway_axis", s=5, kind="scatter")
plt.show()
print(T)