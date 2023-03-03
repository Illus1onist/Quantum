import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.optimize import curve_fit


def randbin(P):
    # вероятность нуля
    return np.random.choice([0, 1], size=(1, 1), p=[P, 1 - P]).reshape(1)[0]


Nmax = 35  # Просто для программы, должно быть больше Notgad и Nzad
Notgad = 4  # Число частот считывания
Nzad = 4  # Число задающих частот

frequency = 10 * 10 ** 3  # Наименьшая частота сигнала
Bparasite = 0 * 10 ** -12  # Паразитное B

koef = 1.4 * 10 ** 15  # Магнетон делить на планка

# Создание больших массивов
B = [0] * Nmax
A = [0] * Nmax

# Задача поля
for i in range(Nzad):
    B[i] = randbin(0.5) * 10 ** -12  # наше поле (его амплитуда)
    A[i] = randbin(0.5) * 10 ** -12  # наше поле (его амплитуда)
NumberOfQuants = 100

# Дополнительная задача первых гармоник
#A[0] = 1 * 10 ** -12
#B[0] = 0 * 10 ** -12
#A[1] = 1 * 10 ** -12
#B[1] = 1 * 10 ** -12
#A[2] = 1 * 10 ** -12
#B[2] = 1 * 10 ** -12

JU = 3.5  # Множитель для более хорошей амплитуда сигнала

Y = 1000  # Количество точек для отображения

GraphiksDataBase = [0] * Nzad
for i in range(Nzad):
    GraphiksDataBase[i] = [0] * Y

# DatabaseOfSumPhaseCorrectedFromMistakesInExperiment
GraphiksDataBaseCorrected = [0] * Nzad
for i in range(Nzad):
    GraphiksDataBaseCorrected[i] = [0] * Y

GraphiksDataBaseIdeal = [0] * Nzad
for i in range(Nzad):
    GraphiksDataBaseIdeal[i] = [0] * Y

stattime = [0] * Y
for i in range(Y):
    stattime[i] = i/Y*2*np.pi


#  Перебор всех частот от наименьшей к наибольшей, моделирование сигнала.
print("Modelling in progress 0%")
for Numb in range(Notgad - 1, -1, -1):
    #  Перебор фаз начала
    stat0 = [0] * Y
    for v in range(Y):
        PhaseForB = (v / Y) * 2 * np.pi  # 2pi - наибольший период


        # Моделирование сигнала
        # Функция сигнала от времени
        def f(t):

            # Заготовка под кручение
            x=t#+1/frequency/(Numb+1)/4
            count=0
            while x>=1/frequency/(Numb+1)/2:
                x = x-1/frequency/(Numb+1)/2
                count += 1

            # Значение сигнала в точке
            signal = 0
            for j in range(Nzad):
                signal = signal + koef * A[j] * np.sin(frequency * (j + 1) * t * 2 * np.pi + PhaseForB * (j + 1)) + \
                         koef * B[j] * np.cos(frequency * (j + 1) * t * 2 * np.pi + PhaseForB * (j + 1))
            signal = signal + koef * Bparasite
            # Значение сигнала в точке

            # Кручение
            if count % 2 == 0:
                return signal * -1
            if count % 2 == 1:
                return signal * 1
        SumPhase, err = integrate.quad(f, 0, 1 / frequency)

        # Запись без кубитного модуля
        GraphiksDataBaseIdeal[Numb][v] = float(SumPhase)*JU

        # Кубитный модуль
        SumPhase=SumPhase*JU+np.pi/4
        schet = 0
        for i in range(NumberOfQuants):
            schet = schet+1-randbin(np.cos(SumPhase) * np.cos(SumPhase))
        SumPhase = np.arccos(np.sqrt(schet/NumberOfQuants))
        # Запись с кубитами
        GraphiksDataBase[Numb][v] = (SumPhase - np.pi / 4)

    print(int(100 * (Notgad - Numb) / Notgad), '%')
print("Done")



# Корректировка данных для последующей обработки (преобразование к чистым синусам, вычитание одних сигналов из других)
print("Correcting graphiks of integrals in progress 0%")
for Numb in range(Notgad - 1, -1, -1):
    for Numb2 in range(Notgad - 1, Numb, -1):
        if (Numb2 + 1) % (Numb + 1) == 0 and ((Numb2 + 1) // (Numb + 1)) % 2 == 1:
            print(Numb2 + 1, Numb + 1)
            for v in range(Y):
                GraphiksDataBase[Numb][v] = GraphiksDataBase[Numb][v] - GraphiksDataBase[Numb2][v] / (
                            (Numb2 + 1) / (Numb + 1))
                GraphiksDataBaseIdeal[Numb][v] = GraphiksDataBaseIdeal[Numb][v] - GraphiksDataBaseIdeal[Numb2][v] / (
                            (Numb2 + 1) / (Numb + 1))
print("Done")


# Корректировка от случайных ошибок, сглаживание
print("Correcting of accident mistakes in progress 0%")
for v in range(Notgad):
    for i in range(Y):
        sum = 0
        k = max(int(20 / (v + 1)), 2)
        for d in range(-k, k):
            sum = sum + GraphiksDataBase[v][(i + d) % Y]
        GraphiksDataBaseCorrected[v][i] = sum / 2 / k
print("Done")



print("Finding the Phases of Waves in progress 0%")
FinalPhases = [0] * Nzad
for v in range(Nzad):
    MaxOfGraph = max(GraphiksDataBaseCorrected[v])
    for i in range(Y):
        if GraphiksDataBaseCorrected[v][i] == MaxOfGraph:
            FinalPhases[v] = i  # /Y*2*np.pi     #((i*(v+1))%Y)/Y*2*np.pi  # тут фаза для волны уже не зависящей от частоты, в ее координатах!
            break
print("Done")
print(FinalPhases)

# Модуль нахождения амплитуд
AverageSquarePhase = [0] * Notgad
for v in range(Notgad):
    for i in range(Y):
        AverageSquarePhase[v] = AverageSquarePhase[v] + GraphiksDataBaseCorrected[v][i] * GraphiksDataBaseCorrected[v][i] / Y
Amplitudes = [0] * Notgad
for v in range(Notgad):
    Amplitudes[v] = np.sqrt(AverageSquarePhase[v] / (2 / np.pi / np.pi) / koef ** 2 / (1 / frequency * JU) ** 2)
print(Amplitudes)



for v in range(Notgad):
    def mapping1(X, phi):
        return 2 / np.pi * Amplitudes[v] * koef / frequency * JU * np.sin((v+1)*X + phi)
    arg, covar = curve_fit(mapping1, stattime, GraphiksDataBaseIdeal[v])
    FinalPhases[v] = (arg)
    print(arg/(2*np.pi))

#print("Finding better Phases of Waves in progress 0%")
#Value = 90
#
#statF = [0] * Y
#stat = [0] * Value
#stat0 = [0] * Value
#for v in range(Notgad):
#    minmetrica = 10000
#    newI = FinalPhases[v]
#    for d in range(Value):
#        metrica = 0
#        for i in range(Y):
#            metrica = metrica + abs(
#                GraphiksDataBaseCorrected[v][i] - 2 / np.pi * Amplitudes[v] * koef / frequency * JU * np.sin(
#                    i / (Y / (v + 1)) * 2 * np.pi
#                    - ((((v + 1) * FinalPhases[v] - int(Value / 2) + d + Y) % Y) / Y
#                       * 2 * np.pi)))
#            # stat[d]=metrica
#            # stat0[d]=FinalPhases[v]-int(Value/2)+d
#
#            statF[i] = 2 / np.pi * Amplitudes[v] * koef / frequency * JU * np.sin(i / (Y / (v + 1)) * 2 * np.pi
#                                                                                  - ((((v + 1) * FinalPhases[v] - int(
#                Value / 2) + d + Y) % Y) / Y
#                                                                                     * 2 * np.pi))
#
#        if metrica < minmetrica:
#            newI = FinalPhases[v] - int(Value / 2) + d
#            minmetrica = metrica
#
#    FinalPhases[v] = newI
#
#print(FinalPhases)
#print("Done")

#for v in range(Notgad):
#    FinalPhases[v] = ((FinalPhases[v] * (v + 1)) % Y) / Y * 2 * np.pi


#plt.scatter(stattime, GraphiksDataBase[0], s=2, color='blue')
#plt.scatter(stattime, GraphiksDataBaseCorrected[0], s=2, color='green')
#plt.scatter(stattime, GraphiksDataBaseIdeal[0], s=2, color='red')
#plt.grid(True)
#plt.show()
#plt.scatter(stattime, GraphiksDataBase[1], s=2, color='blue')
#plt.scatter(stattime, GraphiksDataBaseCorrected[1], s=2, color='green')
#plt.scatter(stattime, GraphiksDataBaseIdeal[1], s=2, color='red')
#plt.grid(True)
#plt.show()
#plt.scatter(stattime, GraphiksDataBase[2], s=2, color='blue')
#plt.scatter(stattime, GraphiksDataBaseCorrected[2], s=2, color='green')
#plt.scatter(stattime, GraphiksDataBaseIdeal[2], s=2, color='red')
#plt.grid(True)
#plt.show()
# plt.scatter(stattime, GraphiksDataBase[3], s=2, color='blue')
# plt.scatter(stattime, GraphiksDataBaseCorrected[3], s=2, color='green')
# plt.scatter(stattime, GraphiksDataBaseIdeal[3], s=2, color='red')
# plt.grid(True)
# plt.show()

stat1 = [0] * Y
stat2 = [0] * Y

# Реальный Сигнал
for i in range(Y):
    signal = 0
    for j in range(Nzad):
        signal = signal + A[j] * np.sin(i / (Y / (j + 1)) * 2 * np.pi) + \
                 B[j] * np.cos(i / (Y / (j + 1)) * 2 * np.pi)
    signal = signal + Bparasite
    stat1[i] = signal
# Реальный сигнал

# Найденный сигнал
for i in range(Y):
    signal = 0
    for j in range(Notgad):
        signal = signal + Amplitudes[j] * np.sin(i / Y * (j + 1) * 2 * np.pi + FinalPhases[j]+0.5*np.pi)
    signal = signal + Bparasite
    stat2[i] = signal
# Найденный сигнал


plt.scatter(stattime, stat1, s=5, color='blue')
plt.scatter(stattime, stat2, s=5, color='red')

plt.grid(True)
plt.show()
