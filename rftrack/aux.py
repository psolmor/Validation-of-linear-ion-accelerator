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

def plot_solenoid_field_lattice(lebt, L_sol=0.2574, L_drift=0.139, x_mm=0.0, y_mm=0.0):

    s = np.linspace(0.0, L_sol + L_drift, 2000)   # m

    x = np.full_like(s, x_mm)     # mm
    y = np.full_like(s, y_mm)     # mm
    z = s * 1e3                   # mm
    t = np.zeros_like(s)          # mm/c

    E, B = lebt.get_field(x, y, z, t)

    B = np.asarray(B)

    if B.shape[0] == 3 and B.shape[1] == len(s):
        B = B.T

    Bx = B[:, 0]
    By = B[:, 1]
    Bz = B[:, 2]
    Babs = np.sqrt(Bx**2 + By**2 + Bz**2)

    Bz_hard = np.where((s >= 0.0) & (s <= L_sol), 0.344, 0.0)

    plt.figure(figsize=(8, 5))
    plt.plot(s, Bz, linewidth=2.2, label=r"RF-Track $B_z$")
    plt.plot(s, Bz_hard, "--", linewidth=2.0, label=r"Hard-edge $B_z$")
    plt.axvline(0.0, color="k", linewidth=1, alpha=0.4)
    plt.axvline(L_sol, color="k", linewidth=1, alpha=0.4)
    plt.xlabel(r"$s$ [m]")
    plt.ylabel(r"$B_z$ [T]")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("rftrack_solenoid_Bz.png", dpi=300)
    plt.show()

    return s, Bx, By, Bz, Babs

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