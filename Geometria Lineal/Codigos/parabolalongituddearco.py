import numpy as np
import matplotlib.pyplot as plt

# Definir la función de la parábola
def parabola(x):
    return x**2

# Definir el intervalo
a = -2
b = 2

# Crear un arreglo de valores de x
x_values = np.linspace(a, b, 100)
y_values = parabola(x_values)

# Calcular la longitud de arco
dx = x_values[1] - x_values[0]
dy = parabola(x_values[1:]) - parabola(x_values[:-1])
arc_length = np.sum(np.sqrt(dx**2 + dy**2))
print(f"La longitud de arco de la parábola en el intervalo [{a}, {b}] es: {arc_length:.4f}")

# Graficar la parábola
plt.plot(x_values, y_values, label='$y = x^2$')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Gráfica de la parábola $y = x^2$')
plt.grid(True)
plt.legend()
plt.show()



