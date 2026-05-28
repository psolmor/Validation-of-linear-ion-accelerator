import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

L = 0.2574
z_start = -0.1
z_end = L + 0.1

Nz = 2000
B0 = 0.344
fringe = 0.0

z = np.linspace(z_start, z_end, Nz + 1)

def solenoid_profile(z, z1, z2, a):
    return 0.5 * (np.tanh((z - z1) / a) - np.tanh((z - z2) / a))

Bz = B0 * solenoid_profile(z, 0.0, L, fringe)

results_dir = Path.cwd().resolve().parent / "beam_plots"
results_dir.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(8, 4.5))

ax.plot(z, Bz, linewidth=2)
ax.axvline(0, linestyle="--", linewidth=1.5, label="Entrada solenoide")
ax.axvline(L, linestyle="--", linewidth=1.5, label="Salida solenoide")

ax.set_xlabel("z [m]")
ax.set_ylabel(r"$B_z$ [T]")
ax.grid(True, alpha=0.3)
ax.legend()

fig.tight_layout()

plot_path = results_dir / "solenoid_hard_profile.png"
fig.savefig(plot_path, dpi=300, bbox_inches="tight")

plt.show()

z_start_cm = z_start * 100
z_end_cm = z_end * 100

with open("solenoid_1D.map", "w") as f:
    f.write("1DMagnetoStatic 40\n")
    f.write(f"{z_start_cm:.4f} {z_end_cm:.4f} {Nz}\n")
    f.write("0.0 2.0 50\n")

    for b in Bz:
        f.write(f"{b:.8e}\n")

print("solenoid_1D.map generated")
print(f"Plot saved in: {plot_path}")