import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

theta = np.linspace(0, 4*np.pi, 100)
z = np.linspace(0, 4*np.pi, 100)
r = theta**0.5

x = r * np.cos(theta)
y = r * np.sin(theta)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z)

ax.set_title('Caracol Circular en 3D')
plt.show()