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

from matplotlib.patches import Rectangle

def plot_lattice(ax, s_offset=0.0, show_labels=False, min_width=0.012):
    elements = [
        ("drift3",      "drift",    0.208),
        ("drift_chop", "chopper",  0.150),
        ("drift4",     "drift",    0.140),
        ("drift5",     "drift",    0.722),

        ("collx",      "coll",     0.002),
        ("drift_col",  "drift",    0.002),
        ("colly",      "coll",     0.002),

        ("drift6",     "drift",    0.194),
        ("quad1",      "quad",     0.140),
        ("drift7",     "drift",    0.092),
        ("quad2",      "quad",     0.140),
        ("drift8",     "drift",    0.092),
        ("quad3",      "quad",     0.140),

        ("drift9",     "drift",    0.9101),
        ("sol",        "solenoid", 0.2574),
        ("drift10",    "drift",    0.139),
    ]

    styles = {
        "quad":     dict(color="black", alpha=0.90),
        "solenoid": dict(color="black", alpha=0.45),
        "coll":     dict(color="gray", alpha=0.70),
        "chopper":  dict(color="purple", alpha=0.45),
    }

    y_min, y_max = ax.get_ylim()
    yrange = y_max - y_min

    # Altura visual de los elementos
    height = 0.16 * yrange

    # Centrado en y = 0
    y0 = -height / 2

    z = 0.0

    for label, kind, length in elements:
        s0_real = s_offset + z
        s1_real = s_offset + z + length

        if kind != "drift":
            width = max(length, min_width)

            # Mantiene el centro físico real aunque se ensanche visualmente
            center = 0.5 * (s0_real + s1_real)
            s0_plot = center - width / 2

            rect = Rectangle(
                (s0_plot, y0),
                width,
                height,
                linewidth=0,
                zorder=0,
                **styles[kind]
            )
            ax.add_patch(rect)

            if show_labels:
                ax.text(
                    center,
                    y0 + 0.6 * height,
                    label,
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    rotation=90,
                    zorder=3
                )

        z += length

    # Línea central del haz
    ax.axhline(0.0, color="gray", linewidth=1.0, alpha=0.6, zorder=0)

    # Recupera límites originales
    ax.set_ylim(y_min, y_max)

    return s_offset + z