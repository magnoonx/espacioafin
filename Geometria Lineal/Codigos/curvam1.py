import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2*np.pi, 80)  # Parámetro

# Definir la curva paramétrica: x(t) = cos(t), y(t) = sin(t)
x = np.cos(t)
y = np.sin(t)

# Calcular la derivada de primer orden
dx_dt = -np.sin(t)
dy_dt = np.cos(t)

# Graficar la curva y el vector tangente
plt.plot(x, y, 'b', linewidth=2, label='Curva paramétrica')
plt.quiver(x, y, dx_dt, dy_dt, scale=10, color='r', label='Vector tangente')
plt.legend()
plt.axis('equal')
plt.show()
