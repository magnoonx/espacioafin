import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir la curva R(t) = (t, t^2, t^3)
t = np.linspace(-1, 2, 100)
x = t
y = t**2
z = t**3

# Calcular el punto en t = 2
t_val = 2
x_val = t_val
y_val = t_val**2
z_val = t_val**3

# Calcular el vector tangente en t = 2
r_prime = np.array([1, 2*t_val, 3*t_val**2])
T = r_prime / np.linalg.norm(r_prime)

# Calcular el vector normal al plano en el punto t = 2
normal = r_prime / np.linalg.norm(r_prime)

# Crear el plano normal en el punto t = 2
xx, yy = np.meshgrid(np.linspace(-2, 2, 10), np.linspace(-2, 4, 10))
zz = z_val - (r_prime[0]*(xx - x_val) + r_prime[1]*(yy - y_val) / r_prime[2]) 

# Graficar la curva y el plano normal en el punto t = 2
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, label='Curva R(t)')
ax.quiver(t_val, t_val**2, t_val**3, T[0], T[1], T[2], color='r', label='Vector Tangente Unitario en t=2')
ax.plot_surface(xx, yy, zz, alpha=0.5, label='Plano Normal en t=2')
ax.scatter(x_val, y_val, z_val, color='r', label='Punto en t=2')
ax.set_title('Plano con vector normal ({}, {}, {})'.format(r_prime[0], r_prime[1], r_prime[2]))
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
plt.show()

