import matplotlib.pyplot as plt
import sys

VecStart_x = 0
VecStart_y = 2
VecStart_z = 0
VecEnd_x = 1
VecEnd_y = 3
VecEnd_z  = 1

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot([VecStart_x, VecEnd_x], [VecStart_y,VecEnd_y],zs=[VecStart_z,VecEnd_z], marker='o')
plt.show()
plt.close()
input("Press Enter to continue...")