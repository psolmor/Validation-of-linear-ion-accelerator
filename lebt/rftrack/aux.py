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

import matplotlib.pyplot as plt

def plot_lattice(ax):
    elements = [
        ("drift", 0.260),
        ("coll", 0.0025),
        ("drift", 0.3375),
        ("dipole", 0.628318),
        ("drift", 0.208),
        ("chopper", 0.150),
        ("drift", 0.140),
        ("drift", 0.722),
        ("collx", 0.002),
        ("drift", 0.002),
        ("colly", 0.002),
        ("drift", 0.194),
        ("quad", 0.140),
        ("drift", 0.092),
        ("quad", 0.140),
        ("drift", 0.092),
        ("quad", 0.140),
        ("drift", 0.9101),
        ("solenoid", 0.2574),
        ("drift", 0.1393),
    ]

    y_min, y_max = ax.get_ylim()

    height = 0.15 * (y_max - y_min)
    y0 = -height / 2  

    s_pos = 0

    for name, length in elements:
        s0 = s_pos
        s1 = s_pos + length

        if name == "dipole":
            color = "black"
            alpha = 0.25

        elif name == "quad":
            color = "black"
            alpha = 0.9

        elif name == "solenoid":
            color = "black"
            alpha = 0.5

        elif name.startswith("coll"):
            color = "gray"
            alpha = 0.6

        elif name == "chopper":
            color = "purple"
            alpha = 0.5

        else:
            s_pos = s1
            continue

        rect = plt.Rectangle(
            (s0, y0),
            s1 - s0,
            height,
            color=color,
            alpha=alpha
        )

        ax.add_patch(rect)

        s_pos = s1