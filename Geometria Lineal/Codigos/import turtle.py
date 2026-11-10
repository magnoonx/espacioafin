import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir el punto de origen y el vector normal para los planos
origin = np.array([0, 0, 0])
normal_vector = np.array([1, 1, 1])  # Vector normal para el primer plano

# Crear una malla de puntos para los planos
xx, yy = np.meshgrid(range(-5, 6), range(-5, 6))
z = np.zeros(xx.shape)

# Crear la figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Graficar los planos
for i in range(-5, 6):
    point = origin + normal_vector * i
    ax.plot_surface(xx + point[0], yy + point[1], z + point[2], color='b', alpha=0.3)

# Configurar los ejes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Mostrar la gráfica
plt.show()
