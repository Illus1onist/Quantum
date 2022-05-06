import numpy as np
import matplotlib.pyplot as plt
import random

def randbin(P):
    # вероятность нуля
    return np.random.choice([0, 1], size=(1, 1), p=[P, 1 - P]).reshape(1)[0]

N=10
frequency=10*10**3
Tperiod=1/frequency
phaseforB=0 # Это значение смещения фазы магнитного поля в радианах!!!
Bparasite=0*10**-12  # паразитное B
F = 5000 # дискретизация
koef = 1.4*10**15  # магнетон делить на планка
B=[0]*N
B[0] = 1.0*10**-12  # наше поле (его амплитуда)
B[1] = 0.0*10**-12  # наше поле (его амплитуда)
B[2] = 1.0*10**-12  # наше поле (его амплитуда)
B[3] = 0.0*10**-12  # наше поле (его амплитуда)
B[4] = 1.0*10**-12  # наше поле (его амплитуда)
B[5] = 0.0*10**-12  # наше поле (его амплитуда)
B[6] = 1.0*10**-12  # наше поле (его амплитуда)
B[7] = 1.0*10**-12  # наше поле (его амплитуда)
B[8] = 0.0*10**-12  # наше поле (его амплитуда)
B[9] = 0.0*10**-12  # наше поле (его амплитуда)
B0 = 5.6*10**-12  # 5,6*10**-12 - максимум
t = 1*10**-4  # время первого снятия

Y = 1000 # (Y - частота дискретизации самого поля, один МАКСИМАЛЬНЫЙ период разделен на 1000 столбцов)

AverageSquarePhase=[0]*N
P=100
NumberOfQuants=100
for o in range (N): # перебор частот поворотов, от frequency до 10xfrequency
    for v in range(P):
        phaseforB = random.random()*2
        SumPhase = 0
        for i in range(int(t * frequency) * Y):  # (Y - частота дискретизации самого поля, один Максимальный период разделен на 1000 столбцов)
            signal = 0
            #for j in range(N):
                #signal = signal + B[j] * np.sin(i / (Y / (j + 1)) * 2 * np.pi + phaseforB * (j + 1) * np.pi)
            y = 16
            signal = -(-1 + 2 * (((i-(int(t * frequency) * Y*phaseforB)) // int((int(t * frequency) * Y / y * 2))) % 2)) * B[0] * (
                        1 - (y * (((i-(int(t * frequency) * Y*phaseforB)) % ((int(t * frequency) * Y) / (y / 2)) - 1 / y * (int(t * frequency) * Y)) / (
                        int(t * frequency) * Y))) ** 2)
            if (i%int(Y/(o+1))<=int(Y/(o+1))/2):
                SumPhase = SumPhase - koef * Bparasite * Tperiod / Y + koef / frequency / Y * (
                signal)
            if (i%int(Y/(o+1))>int(Y/(o+1))/2):
                SumPhase = SumPhase + koef * Bparasite * Tperiod / Y - koef / frequency / Y * (
                signal)
        schet=0
        #for i in range(NumberOfQuants):
        #    schet=schet+1-randbin(np.cos(SumPhase) * np.cos(SumPhase))
        #SumPhase=np.arccos(np.sqrt(schet/NumberOfQuants))
        AverageSquarePhase[o]=AverageSquarePhase[o]+SumPhase*SumPhase/P
    print(AverageSquarePhase[o])

matritsakoeffitsientow=[[0]*10 for i in range (10)]

matritsakoeffitsientow[0]=[0.20264103395265898, 1.9999999999999995e-06, 0.02251448526569643, 2.0000000000000033e-06, 0.008104361390953645, 1.9999999999999957e-06, 0.004134225247166818, 2.0000000000002197e-06, 0.002500424394070387, 2.0000000000000033e-06]
matritsakoeffitsientow[1]=[2.7149467218981034e-32, 0.2026370339723984, 3.418457832014207e-32, 7.999999999999995e-06, 6.59009381167487e-33, 0.022510485443359887, 6.419841833087326e-33, 8.000000000000042e-06, 1.47367377494754e-32, 0.008100361884515057]
matritsakoeffitsientow[2]=[6.62604776738826e-07, 1.985115299958709e-06, 0.20254505274243378, 2.027489017105197e-06, 6.860080374719085e-07, 7.985482266461899e-06, 6.369853757419257e-07, 1.9361152203587923e-06, 0.02241865423319009, 2.062775031792105e-06]
matritsakoeffitsientow[3]=[4.532305448045641e-33, 2.1946469490836946e-32, 3.8095717474096454e-32, 0.20262103428823447, 3.9585689848138024e-32, 7.375622881940737e-33, 5.0707522864384635e-33, 3.200000000000005e-05, 7.657208190026788e-33, 6.409130269149584e-33]
matritsakoeffitsientow[4]=[4.9577475842598764e-33, 4.249750948278483e-33, 1.600549471916734e-32, 3.409825337958267e-32, 0.20260903477384357, 5.819350485318818e-32, 1.1820203452761893e-32, 1.1037886543208696e-32, 1.3397635278877058e-32, 4.9999999999999935e-05]
matritsakoeffitsientow[5]=[8.361865566691387e-06, 1.0374208453598385e-05, 1.5481115894875063e-05, 3.066097771090504e-05, 0.00011151265071199187, 0.19648186863339542, 0.00012247081988763452, 3.209472085439718e-05, 1.6073065643218786e-05, 1.0993597459081489e-05]
matritsakoeffitsientow[6]=[1.837050957280775e-05, 2.1376555230044792e-05, 2.8080287713814123e-05, 4.341905738332553e-05, 8.73037134344698e-05, 0.000313709218085569, 0.1843809914617719, 0.00035792205995654444, 8.834257545291098e-05, 4.14191600059331e-05]
matritsakoeffitsientow[7]=[1.4331091782838609e-33, 2.583412965165243e-33, 1.5864144743086246e-33, 2.9800975059722024e-33, 4.7539883736401045e-33, 1.8860082739260162e-32, 8.759116110576872e-32, 0.20265303428823458, 3.7207927851810183e-31, 3.738106668745816e-32]
matritsakoeffitsientow[8]=[5.063344174541235e-07, 5.562372725868805e-07, 6.551134027807813e-07, 8.376366462757637e-07, 1.1901900107320288e-06, 1.967411918142152e-06, 4.20104286411072e-06, 1.6195567402157058e-05, 0.20178448570575058, 1.6919902616056704e-05]
matritsakoeffitsientow[9]=[5.3209853665031076e-34, 9.476641683721688e-33, 1.0996422373424231e-33, 2.1406205109909887e-33, 2.5013641621846793e-33, 1.2902281813424753e-32, 2.8500909835813964e-32, 3.6278804190556504e-32, 3.6957836796785783e-31, 0.2025090471128799]

solution = np.linalg.inv(matritsakoeffitsientow)@AverageSquarePhase
for i in range (N):
    solution[i]=np.sqrt(abs(solution[i])/koef**2/t**2)
    print(solution[i])


stat1=[0]*int(t * frequency) * Y
stat2=[0]*int(t * frequency) * Y
stattime=[0]*int(t * frequency) * Y
for i in range (int(t * frequency) * Y):
    stattime[i]=i
    signal = 0
    #for j in range(N):
    #    signal = signal + B[j] * np.sin(i / (Y / (j + 1)) * 2 * np.pi)

    phaseforB=0.0
    signal = -(-1 + 2 * (((i - (int(t * frequency) * Y * phaseforB)) // int((int(t * frequency) * Y / y * 2))) % 2)) * \
             B[0] * (
                     1 - (y * (((i - (int(t * frequency) * Y * phaseforB)) % (
                         (int(t * frequency) * Y) / (y / 2)) - 1 / y * (int(t * frequency) * Y)) / (
                                       int(t * frequency) * Y))) ** 2)


    stat1[i]=signal
    signal=0
    for j in range(N):
        signal = signal +  solution[j] * np.sin(i / (Y / (j + 1)) * 2 * np.pi)
    stat2[i]=signal#-stat1[i]

plt.scatter(stattime, stat1, s=5, color='blue')
plt.scatter(stattime, stat2, s=5, color='red')


plt.grid(True)
plt.show()