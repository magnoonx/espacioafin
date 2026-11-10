import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parámetros del toro
R = 7  # Radio mayor
r = 2  # Radio menor

# Parámetros paramétricos
theta = np.linspace(0, 2*np.pi, 100)
phi = np.linspace(0, 2*np.pi, 100)
Theta, Phi = np.meshgrid(theta, phi)

# Coordenadas paramétricas del toro
X = np.sin(Theta)*(R + 3*np.cos(Theta/3))
Y = np.cos(Theta)*(R + 3*np.cos(Theta/3))
Z = (3*np.sin(Theta/3 - 2*Phi))

# Graficar el toro paramétrico en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, color='w')

# Configuración de la gráfica
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Toro Umbilical Paramétrico')

plt.show()