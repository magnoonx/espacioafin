import numpy as np
import matplotlib.pyplot as plt

# Definir la curva r(t) = (t, t^2, t^3)
t = np.linspace(-2, 2, 100)
x = t
y = t**2
z = t**3

# Calcular el vector tangente unitario en t = 2
t_val = 2
r_prime = np.array([1, 2*t_val, 3*t_val**2])
T = r_prime / np.linalg.norm(r_prime)

# Graficar la curva y el vector tangente unitario en el punto t = 2
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, label='Curva r(t)')
ax.quiver(t_val, t_val**2, t_val**3, T[0], T[1], T[2], color='r', label='Vector Tangente Unitario en t=2')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
plt.show()
