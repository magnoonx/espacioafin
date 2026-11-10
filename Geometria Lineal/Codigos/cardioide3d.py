import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

theta = np.linspace(0, 2*np.pi, 100)
r = 1 + np.cos(theta)

x = r * np.cos(theta)
y = r * np.sin(theta)
z = np.zeros_like(x)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z)

ax.set_title('Cardioide en 3D')
plt.show()