import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Get a list of colors from the 'jet' colormap
colors = plt.cm.jet(range(256))

# Display the colors and their hexadecimal values
for i, color in enumerate(colors):
    print(f"Color {i}: {mcolors.to_hex(color)}")

