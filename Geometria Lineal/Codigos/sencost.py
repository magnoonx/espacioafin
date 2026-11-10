import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir la curva R(t) = (cos(t), sin(t), t)
t = np.linspace(0, 2*np.pi, 100)
x = np.cos(t)
y = np.sin(t)
z = t

# Calcular el punto en t = pi/4
t_val = 0.01
x_val = np.cos(t_val)
y_val = np.sin(t_val)
z_val = t_val

# Calcular el vector tangente en t = pi/4
r_prime = np.array([-np.sin(t_val), np.cos(t_val), 1])

# Calcular el vector normal al plano en el punto t = pi/4
normal = r_prime / np.linalg.norm(r_prime)

# Crear el plano normal en el punto t = pi/4
xx, yy = np.meshgrid(np.linspace(-1, 1, 10), np.linspace(-1, 1, 10))
zz = normal[0]*(xx - x_val) + normal[1]*(yy - y_val) + normal[2]*(normal[0]*x_val + normal[1]*y_val + normal[2]*z_val)

# Graficar la curva y el plano normal en el punto t = pi/4
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, label='Curva R(t)')
ax.plot_surface(xx, yy, zz, alpha=0.5, label='Plano Normal en t=pi/4')
ax.scatter(x_val, y_val, z_val, color='r', label='Punto en t=pi/4')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
plt.show()
