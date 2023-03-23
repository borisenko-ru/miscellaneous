import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
from mpl_toolkits.axisartist.axislines import AxesZero

# Fixing random state for reproducibility
np.random.seed(19680801)

# some random data
x = np.random.randn(1000)
y = np.random.randn(1000)

im = image.imread('img/wbs0.png')

def scatter_hist(x, y, ax, ax_wbs):
    # no labels
    ax_wbs.tick_params(labelbottom=False, labelleft=False)
    # hides borders
    for direction in ["left", "right", "bottom", "top"]:
        ax_wbs.axis[direction].set_visible(False)

    ax.scatter(x, y)
    ax_wbs.imshow(im)

fig = plt.figure(figsize=(6, 6))
# Add a gridspec with one row and two columns and a ratio of 1 to 4 between
# the size of the marginal axes and the main axes in both directions.
# Also adjust the subplot parameters for a square plot.
gs = fig.add_gridspec(1, 2, width_ratios=(1, 1), left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.05)
# Create the Axes.
ax = fig.add_subplot(gs[1])
ax_wbs = fig.add_subplot(gs[0], axes_class=AxesZero)

# Draw the scatter plot and marginals.
scatter_hist(x, y, ax, ax_wbs)

plt.show()
