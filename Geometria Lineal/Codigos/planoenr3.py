import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Pedir al usuario las coordenadas del vector normal
print("Introduce las coordenadas del vector normal al plano en la forma (a, b, c): ")
a, b, c = map(float, input().split())

# Crear un meshgrid para el plano
xx, yy = np.meshgrid(np.linspace(-10, 10, 10), np.linspace(-10, 10, 10))
z = (-a * xx - b * yy) / c

# Graficar el plano en R^3
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xx, yy, z, alpha=0.8)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Plano con vector normal ({}, {}, {})'.format(a, b, c))
plt.show()
