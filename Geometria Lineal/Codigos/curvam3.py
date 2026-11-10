import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2*np.pi, 200)  # Parámetro

# Definir la curva paramétrica: x(t) = t, y(t) = t^2
x = t
y = t**2

# Calcular las derivadas de primer, segundo y tercer orden
dx_dt = np.ones_like(t)
dy_dt = 2*t
d2x_dt2 = np.zeros_like(t)
d2y_dt2 = 2*np.ones_like(t)
d3x_dt3 = np.zeros_like(t)
d3y_dt3 = np.zeros_like(t)

# Graficar la curva
plt.figure()
plt.plot(x, y, label='Curva paramétrica')
plt.quiver(x, y, dx_dt, dy_dt, scale=10, color='r', label='Vector tangente')
plt.quiver(x, y, d2x_dt2, d2y_dt2, scale=30, color='g', label='Vector de curvatura')
plt.quiver(x, y, d3x_dt3, d3y_dt3, scale=100, color='b', label='Vector de torsión')
plt.legend()
plt.axis('equal')
plt.show()
