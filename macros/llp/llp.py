import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Enable LaTeX formatting for all text in the plot
plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=14)

# Define the exponential distribution function
def exp_dist(z, x):
    return (1/x) * np.exp(-z/x)

# Function to plot the acceptance for given r1, r2, color, and label
def plot_acceptance(r1, r2, color, label):
    # Calculate the acceptance for each decay length
    acceptances = []
    for x in decay_lengths:
        # Integrate the exponential distribution between r1 and r2
        acceptance, _ = quad(exp_dist, r1, r2, args=(x,))
        acceptances.append(acceptance)
    
    # Plot the results
    plt.loglog(decay_lengths, acceptances, color=color, label=label)

# Define the range of decay lengths in log scale
decay_lengths = np.logspace(-1, 4, num=100)  # More points for a smoother line

# Plot settings
plt.figure(figsize=(10, 6))

# Example usage of the function
#plot_acceptance(3, 6, 'blue', 'HGCAL')
plot_acceptance(10.4, 10.9, 'blue', 'HF-Nose')
plot_acceptance(96, 110, 'orange', 'FMS')
plot_acceptance(500, 501.5, 'red', 'FASER')
plot_acceptance(500, 505, 'green', 'FASER 2')

# Set the y-axis limits
plt.ylim(1e-8, 1e0)

# Labeling the axes, title, and legend
plt.xlabel('Decay Length (m)', fontsize=16)
plt.ylabel('Acceptance', fontsize=16)
#plt.title('Acceptance as a Function of Decay Length', fontsize=18)
plt.legend(fontsize=14)

# Grid and show plot
plt.grid(True, which="both", ls="--")
plt.show()
