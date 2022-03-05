import numpy as np
import matplotlib.pyplot as plt

def randbin(P):
    # вероятность нуля
    return np.random.choice([0, 1], size=(1, 1), p=[P, 1 - P]).reshape(1)[0]

def C(n, k):
    if 0 <= k <= n:
        nn = 1
        kk = 1
        for t in range(1, min(k, n - k) + 1):
            nn *= n
            kk *= t
            n -= 1
        return nn // kk
    else:
        return 0


N=1000

F = 5000
koef = 1.4*10**15  # магнетон делить на планка
a = 0  # кол-во нулей в одной серии
B=3*10**-12 # 5,6*10**-12
t=200*10**-6
for i in range (N):
    if (randbin(np.cos(koef*B*t) * np.cos(koef*B*t)) == 0):
        a=a+1
l=[0]*F
g=[0]*F
k = C(N, a)
p=1  # границы
o=0
y=0  # счетчик для границ
max=0
for j in range (F):

    l[j] = k*pow(j/F, a)*pow(1-j/F, N-a)
    if l[j]>max:
        max=l[j]
    g[j]=j/F
for j in range(F):
    if (l[j]>0.05*max and y==0):
        p=j/F
        y=y+1
    if (y==1 and l[j]<0.05*max):
        o=j/F
        y=y+1

Bmin=(np.arccos(np.sqrt(o))/koef)/t
Bmax=(np.arccos(np.sqrt(p))/koef)/t
print(-Bmin+Bmax)
#for j in range (F):

plt.scatter(g, l, s=10, color='red')

plt.grid(True)
plt.show()