import numpy as np
import matplotlib.pyplot as plt

def randbin(P):
    # вероятность нуля
    return np.random.choice([0, 1], size=(1, 1), p=[P, 1 - P]).reshape(1)[0]

def C(n, k):
    if 0 <= k <= n:
        nn = 1
        kk = 1
        for s in range(1, min(k, n - k) + 1):
            nn *= n
            kk *= s
            n -= 1
        return nn // kk
    else:
        return 0

frequency=10*10**3
Tperiod=1/frequency
phaseforB=1.5 # Это значение смещения фазы магнитного поля в радианах!!!
Bparasite=1.0*10**-12  # паразитное B
F = 5000 # дискретизация
koef = 1.4*10**15  # магнетон делить на планка
a = 0  # кол-во нулей в одной серии
B = 2.0*10**-12  # наше поле (его амплитуда)
B0 = 5.6*10**-12  # 5,6*10**-12 - максимум
t = 2*10**-4  # время первого снятия
l = [1/F]*F  # первое распределение (юниформ)
u = [1/F]*F
q = [1/F]*F
p = [1/F]*F



g = [0]*F

N = 50

for j in range (F):
    g[j] = j/F*B0


Y = 1000 # (Y - частота дискретизации самого поля, один период разделен на 1000 столбцов)
#h=int(t*frequency * Y)
#stat=[0]*h
#timeforstat=[0]*h
#for i in range (h):
    #timeforstat[i]=i


for k in range(5):
    SumPhase = 0
    for i in range(int(t / Tperiod) * Y):  # (Y - частота дискретизации самого поля, один период разделен на 1000 столбцов)
        if (np.sin(i / Y * 2 * np.pi + phaseforB*np.pi)<0):
            SumPhase = SumPhase - koef * Bparasite * Tperiod / Y - koef * B * np.sin(
                i / Y * Tperiod * 2 * np.pi / Tperiod +
                phaseforB * np.pi) * Tperiod / Y
        if (np.sin(i / Y * 2 * np.pi + phaseforB*np.pi)>0):
            SumPhase = SumPhase + koef * Bparasite * Tperiod / Y + koef * B * np.sin(
                i / Y * Tperiod * 2 * np.pi / Tperiod +
                phaseforB * np.pi) * Tperiod / Y


        #stat[i]=SumPhase
    #print(SumPhase)
    for j in range (N):
        if (randbin(np.cos(SumPhase*np.pi/2) * np.cos(SumPhase*np.pi/2)) == 0):
            a=a+1  # первое снятие
    sum=0

    for j in range(F):
        l[j] = l[j]*C(N,a)*((np.cos(koef*g[j]*t))**2)**(a)*((np.sin(koef*g[j]*t))**2)**(N-a)
        sum = sum+l[j]


    for j in range(F):
        l[j] = l[j]/sum

    for j in range(F):
        u[j]=l[j]

    max=0
    y=0
    for j in range(F):
        if l[j] > max:
            max = l[j]
    for j in range(F):
        if (l[j] > 0.01 * max and y == 0):
            MinB = j / F*B0
            y = y + 1
        if (y == 1 and l[j] < 0.01 * max):
            MaxB = j / F*B0
            y = y + 1
    print(MaxB-MinB)

    t=2*t
    a=0

plt.scatter(g, l, s=10, color='blue')



plt.grid(True)
plt.show()
