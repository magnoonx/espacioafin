import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir la recta
point_on_line = np.array([1, 2, 3])  # Punto en la recta
direction_vector = np.array([1, 1, 1])  # Vector de dirección de la recta

# Crear una malla de puntos para los planos
xx, yy = np.meshgrid(range(-5, 6), range(-5, 6))
z = np.zeros(xx.shape)

# Crear la figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Graficar los planos que pasan por la recta
for i in range(-5, 6):
    normal_vector = np.cross(direction_vector, np.array([i, i, i]))  # Generar un vector normal usando el producto cruz
    d = -point_on_line.dot(normal_vector)  # Calcular la distancia desde el origen al plano
    ax.plot_surface(xx, yy, (-normal_vector[0]*xx - normal_vector[1]*yy - d)*1./normal_vector[2], color='b', alpha=0.3)

# Graficar la recta
line_points = point_on_line + np.array([t*direction_vector for t in range(-5, 6)])
ax.plot3D(line_points[:,0], line_points[:,1], line_points[:,2], 'red')

# Configurar los ejes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Mostrar la gráfica
plt.show()
