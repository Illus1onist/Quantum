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


F = 5000
koef = 1.4*10**15  # магнетон делить на планка
a = 0  # кол-во нулей в одной серии
B = 5*10**-12  # наше поле
B0 = 5.6*10**-12  # 5,6*10**-12 - максимум
t = 200*10**-6  # время первого снятия
l = [1/F]*F  # первое распределение (юниформ)
u = [1/F]*F
q = [1/F]*F
p = [1/F]*F


g = [0]*F
N = 50
for j in range (F):
    g[j] = j/F*B0

for i in range (5):
    for j in range (N):
        if (randbin(np.cos(koef*B*t) * np.cos(koef*B*t)) == 0):
            a=a+1  # первое снятие
    sum=0
    for j in range(F):
        if (a>N/2):
            l[j] = l[j]*(np.cos(koef*g[j]*t))**2
        if (a<=N/2):
            l[j] = l[j]*(np.sin(koef*g[j]*t))**2
        sum = sum+l[j]
    for j in range(F):
        l[j] = l[j]/sum
    max=0
    y=0
    MaxB=B0
    MinB=0
    for j in range(F):
        if l[j] > max:
            max = l[j]
    for j in range(F):
        if (l[j] > 0.05 * max and y == 0):
            MinB = j / F*B0
            y = y + 1
        if (y == 1 and l[j] < 0.05 * max):
            MaxB = j / F*B0
            y = y + 1
    print(MaxB-MinB)
    a=0
    t=t*2



plt.scatter(g, l, s=3, color='blue')


plt.grid(True)
plt.show()