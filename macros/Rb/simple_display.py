import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Function to add a vector to the plot
def plot_vector(ax, start_point, end_point, color):
    ax.quiver(start_point[0], start_point[1], start_point[2],
              end_point[0]-start_point[0], end_point[1]-start_point[1], end_point[2]-start_point[2],
              color=color, arrow_length_ratio=0.1)

# Example data (replace with your actual data)
jets = [(0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0)]
bhadrons = [(0.5, 0.5, 0.5, 0.5, 0.5, 0.5)]
gluons = [(0, 0, 0, 0, 0, 1)]

# Create a new figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot each vector
for jet in jets:
    plot_vector(ax, jet[:3], np.add(jet[:3], jet[3:]), 'blue')

for bhadron in bhadrons:
    plot_vector(ax, bhadron[:3], np.add(bhadron[:3], bhadron[3:]), 'red')

for gluon in gluons:
    plot_vector(ax, gluon[:3], np.add(gluon[:3], gluon[3:]), 'green')

# Setting the axes properties
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
ax.set_zlim([0, 1])
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

plt.show()
