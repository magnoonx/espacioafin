import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir parámetro t
t = np.linspace(0, 2*np.pi, 100)

# Definir la curva paramétrica en 3D
x = np.sin(t)
y = np.cos(t)
z = t

# Graficar la curva en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, label='Curva paramétrica')
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')
ax.set_zlabel('Eje Z')
ax.legend()

# Calcular la longitud de arco
delta_t = t[1] - t[0]
arc_length = np.sum(np.sqrt((x[1:] - x[:-1])**2 + (y[1:] - y[:-1])**2 + (z[1:] - z[:-1])**2)) * delta_t

print("La longitud de arco de la curva es:", arc_length)

plt.show()
