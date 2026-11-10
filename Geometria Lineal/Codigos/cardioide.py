import numpy as np
import matplotlib.pyplot as plt

theta = np.linspace(0, 2*np.pi, 100)
r = 1 + np.cos(theta)

x = r * np.cos(theta)
y = r * np.sin(theta)

plt.plot(x, y)
plt.axis('equal')
plt.title('Cardioide')
plt.show()