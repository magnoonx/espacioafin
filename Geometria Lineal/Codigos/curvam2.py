import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2*np.pi, 40)  # Parámetro

# Definir la curva paramétrica: x(t) = cos(t), y(t) = sin(t)
x = np.cos(t)
y = np.sin(t)

# Calcular las derivadas de primer y segundo orden
dx_dt = -np.sin(t)
dy_dt = np.cos(t)
d2x_dt2 = -np.cos(t)
d2y_dt2 = -np.sin(t)

# Graficar la curva
plt.figure()
plt.plot(x, y, label='Curva paramétrica')
plt.quiver(x, y, dx_dt, dy_dt, scale=10, color='r', label='Vector tangente')
plt.quiver(x, y, d2x_dt2, d2y_dt2, scale=30, color='g', label='Vector de curvatura')
plt.legend()
plt.axis('equal')
plt.show()