import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

u = np.linspace(0, 2*np.pi, 100)
v = np.linspace(0, np.pi, 50)
x = 10*np.outer(np.cos(u), np.sin(v))
y = 10*np.outer(np.sin(u), np.sin(v))
z = 5*np.outer(np.ones(np.size(u)), np.cos(v))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, color='y')

plt.show()