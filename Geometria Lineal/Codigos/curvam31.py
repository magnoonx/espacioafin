import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

t = np.linspace(0, 2*np.pi, 30)  # Parámetro

# Definir la curva paramétrica en el espacio R^3
x = np.cos(t)
y = np.sin(t)
z = t

# Calcular las derivadas de primer, segundo y tercer orden
dx_dt = -np.sin(t)
dy_dt = np.cos(t)
dz_dt = np.ones_like(t)

d2x_dt2 = -np.cos(t)
d2y_dt2 = -np.sin(t)
d2z_dt2 = np.zeros_like(t)

d3x_dt3 = np.sin(t)
d3y_dt3 = -np.cos(t)
d3z_dt3 = np.zeros_like(t)

# Graficar la curva y los vectores tangente, normal y binormal
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, 'b', linewidth=2, label='Curva paramétrica')
ax.quiver(x, y, z, dx_dt, dy_dt, dz_dt, length=0.1, normalize=True, color='r', label='Vector tangente')
ax.quiver(x, y, z, d2x_dt2, d2y_dt2, d2z_dt2, length=0.1, normalize=True, color='g', label='Vector normal')
ax.quiver(x, y, z, d3x_dt3, d3y_dt3, d3z_dt3, length=0.1, normalize=True, color='m', label='Vector Ortonormal')
ax.legend()
plt.show()
