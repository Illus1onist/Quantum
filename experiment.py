
import numpy as np
import matplotlib.pyplot as plt
import random
import openpyxl

def randbin(P):
    # вероятность нуля
    return np.random.choice([0, 1], size=(1, 1), p=[P, 1 - P]).reshape(1)[0]
Nmax=35
Notgad=10
Nzad=10

phaseforB=0 # Это значение смещения фазы магнитного поля в радианах!!!



Y = 1000 # (Y - частота дискретизации самого поля, один МАКСИМАЛЬНЫЙ период разделен на 1000 столбцов)
AverageSquarePhase=0
AverageSquarePhaseB=0
P=20000
K=100

SumPhase=[0]*P
SumPhaset=[0]*K

for v in range(P):
    phaseforB = random.random()*2
    SumPhase[v] = np.cos(phaseforB*np.pi)+np.sin(phaseforB*np.pi*2)+2*np.cos(phaseforB*np.pi*2)

maxSum=max(SumPhase)
minSum=min(SumPhase)
schetchik=[0]*K
for v in range(K):
    SumPhaset[v]=minSum+(maxSum-minSum)*((v)/(K))
for v in range(P):
    for j in range(K):
        if (SumPhase[v]>=SumPhaset[j] and SumPhase[v]<=SumPhaset[j]+(maxSum-minSum)/K):
            schetchik[j]=schetchik[j]+1

plt.scatter(SumPhaset, schetchik, s=5, color='blue')

plt.grid(True)
plt.show()
