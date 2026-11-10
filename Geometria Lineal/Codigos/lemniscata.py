import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2*np.pi, 1000)
a = 3

x = a * np.cos(t) / (1 + np.sin(t)**2)
y = a * np.sin(t) * np.cos(t) / (1 + np.sin(t)**2)

plt.figure(figsize=(6,6))
plt.plot(x, y)
plt.axis('equal')
plt.title('Lemniscata de Bernoulli')
plt.grid(True)
plt.show()