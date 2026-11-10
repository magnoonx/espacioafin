import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

theta = np.linspace(0, 2*np.pi, 200)
phi = np.linspace(0, np.pi, 100)
theta, phi = np.meshgrid(theta, phi)
a = 0.9
b = 0.9
c = 0.9
x = a * np.sin(phi) * np.cos(theta)
y = b * np.sin(phi) * np.sin(theta)
z = c * np.cos(phi) * (np.sqrt(np.sin(phi)**2 + np.cos(phi)**2))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, color='red')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
