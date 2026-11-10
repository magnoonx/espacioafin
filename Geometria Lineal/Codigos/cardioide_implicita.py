import numpy as np
import matplotlib.pyplot as plt

# Definir la función implícita de la cardioide
def cardioid_implicit(x, y, a):
    return (x**2 + y**2 - a*x)**2 - a**2 * (x**2 + y**2)

# Crear un grid de valores para evaluar la función implícita
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)

# Parámetro de la cardioide
a = 1

# Evaluar la función implícita en el grid
Z = cardioid_implicit(X, Y, a)

# Graficar la cardioide implícita
plt.contour(X, Y, Z, [0], colors='b')
plt.axis('equal')
plt.title('Representación Implícita de una Cardioide')
plt.show()