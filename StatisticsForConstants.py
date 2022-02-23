import numpy as np
import matplotlib.pyplot as plt
t=np.arange(0, 10, 0.001)
x1 = [10, 30, 70, 150]
y1 = [1.39, 0.80, 0.54, 0.36]

x2 = [10, 30, 70, 150]
y2 = [1.32, 0.60, 0.29, 0.156]

x3 = [ 70, 70, 70, 150]
y3 = [ 2.4,2.4,2.4, 1.2]

plt.scatter(x1, y1, s=30, color='blue')
plt.scatter(x2, y2, s=30, color='red')
plt.scatter(x3, y3, s=30, color='green')

plt.xlabel(r'$Милисекунды$')
plt.ylabel(r'$Ширина\:разброса\:у\:основания$')
plt.legend(['Не Китаев','Китаев с "биномиальным" байесом','Китаев "частым" байесом'], loc='best',)

plt.grid(True)
plt.show()