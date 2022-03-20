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

maxi=0  # координата пика (нужна для вычисления статистики ошибок)
errordiscret=500
numberoftries=200
miss1=[0]*errordiscret
misscoord=[0]*errordiscret

F = 5000
koef = 1.4*10**15  # магнетон делить на планка
a = 0  # кол-во нулей в одной серии
B = 4.0*10**-12  # наше поле
B0 = 5.6*10**-12  # 5,6*10**-12 - максимум
t = 200*10**-6  # время первого снятия
l = [1/F]*F  # первое распределение (юниформ)
for i in range (errordiscret):
    misscoord[i]=i/errordiscret*B0

g = [0]*F

N = 25

for j in range(F):
    g[j] = j/F*B0


for z in range(errordiscret):
    B = B0/errordiscret*z
    t = 200 * 10 ** -6  # время первого снятия
    print(z)
    for XI in range(numberoftries):
        t = 200 * 10 ** -6  # время первого снятия
        for p in range(F):
            l[p]=1/F
        for i in range(5):
            for j in range(N):
                if (randbin(np.cos(koef*B*t) * np.cos(koef*B*t)) == 0):
                    a=a+1  # первое снятие
            sum=0

            if (i>2):
                for j in range(F):
                    if (a > N / 2):
                        l[j] = l[j] * (np.cos(koef * g[j] * t)) ** 2
                    if (a <= N / 2):
                        l[j] = l[j] * (np.sin(koef * g[j] * t)) ** 2
                    sum = sum + l[j]
            else:
                for j in range(F):
                    l[j] = l[j] * C(N, a) * ((np.cos(koef * g[j] * t)) ** 2) ** (a) * (
                                (np.sin(koef * g[j] * t)) ** 2) ** (N - a)
                    sum = sum + l[j]

            for j in range(F):
                l[j] = l[j]/sum

            max=0
            maxi=0
            y=0
            MaxB=B0
            MinB=0
            for j in range(F):
                if l[j] > max:
                    max = l[j]
                    maxi=j
            schetchikdlydelta=maxi
            while (y == 0):
                if (l[schetchikdlydelta]<0.5*max or schetchikdlydelta==0):
                    MinB=schetchikdlydelta/F*B0
                    break
                schetchikdlydelta = schetchikdlydelta - 1
            schetchikdlydelta = maxi

            while (y == 0):
                if (l[schetchikdlydelta]<0.5*max or schetchikdlydelta == F - 1):
                    MaxB=schetchikdlydelta/F*B0
                    break
                schetchikdlydelta = schetchikdlydelta + 1
            #print(MaxB-MinB)

            t=2*t
            a=0
        if (abs(maxi/F*B0-B)/B0)>(MaxB-MinB)/B0:
            miss1[z]=miss1[z]+1/numberoftries
        #plt.scatter(g, l, s=10, color='blue')

        #plt.grid(True)
        #plt.show()
    print(miss1[z])
plt.scatter(misscoord, miss1, s=10, color='blue')



plt.grid(True)
plt.show()