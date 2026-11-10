import numpy as np
import matplotlib.pyplot as plt

# Definir la función implícita de la Elipse
def circle_implicit(x, y):
    return (0.5)*x**2 + y**2 - 1  # La ecuación de una elipse centrada en el origen

# Crear un grid de valores para evaluar la función implícita
x = np.linspace(-1.5, 1.5, 100)
y = np.linspace(-1.5, 1.5, 100)
X, Y = np.meshgrid(x, y)

# Evaluar la función implícita en el grid
Z = circle_implicit(X, Y)

# Graficar la curva implícita
plt.contour(X, Y, Z, [0], colors='b')
plt.axis('equal')
plt.title('Representación Implícita de una Elipse')
plt.show()