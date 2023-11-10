import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors


# Function to read and parse the data from the file
def read_data(file_path):
    data = []
    with open(file_path, "r") as file:
        for line in file:
            if not line.startswith("#"):
                values = line.split()
                if len(values) == 3:
                    # Convert string to float and append to the data list
                    data.append([float(v) for v in values])
    return np.array(data)


# Read the data from the file
#data = read_data("/home/michele/Downloads/EPOSLHC_14TeV_310.txt")
data = read_data("/home/michele/Downloads/Pythia8_14TeV_-5.txt")

# Separate the columns for plotting
log10_theta = data[:, 0]
log10_p_GeV = data[:, 1]
cross_section = data[:, 2]
eta = - np.log(np.tan(np.power(10,log10_theta)/2.))

# To handle zero cross-section values in a log scale, we replace 0 with a small number
cross_section[cross_section == 0] = np.min(cross_section[cross_section > 0]) / 10

# Plotting the 2D histogram
plt.figure(figsize=(10, 8))
plt.hist2d(
    eta, log10_p_GeV, weights=cross_section, bins=50, norm=colors.LogNorm()
)
plt.colorbar(label="Cross-section [pb/bin] (log scale)")
plt.xlabel("eta")
plt.ylabel("log10(p/GeV)")
plt.title("2D Histogram of Particle Cross-Sections")
plt.show()
