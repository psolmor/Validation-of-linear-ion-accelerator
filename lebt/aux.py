import RF_Track as rft
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

def plot_phase_space(x, y, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(6,5))
    
    xy = np.vstack([x, y])
    kde = gaussian_kde(xy, bw_method=0.5)
    z = kde(xy)
    
    idx = z.argsort()
    x, y, z = x[idx], y[idx], z[idx]
    
    sc = ax.scatter(x, y, c=z, s=5, cmap='viridis', alpha=0.8)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    
    cbar = fig.colorbar(sc, ax=ax, orientation='vertical', label='Densidad de partículas')
    
    plt.tight_layout()
    plt.show()