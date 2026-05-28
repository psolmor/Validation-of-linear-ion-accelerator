import numpy as np
from pathlib import Path

input_file = Path("inputs/beam_outDipole_12C6+.txt")
output_file = Path("opal/opal_beam.txt")

output_file.parent.mkdir(exist_ok=True)

data = np.loadtxt(input_file, skiprows=3)

x_mm      = data[:, 0]
xp_mrad   = data[:, 1]
y_mm      = data[:, 2]
yp_mrad   = data[:, 3]
z_mm      = data[:, 4]
Ekin_MeV  = data[:, 8]

m_c12_6 = 11.9967074084982
amu = 931.49410372
mass_MeV = m_c12_6 * amu

x = x_mm * 1e-3
y = y_mm * 1e-3
z = z_mm * 1e-3

xp = xp_mrad * 1e-3
yp = yp_mrad * 1e-3

gamma = 1.0 + Ekin_MeV / mass_MeV
betagamma = np.sqrt(gamma**2 - 1.0)

norm = np.sqrt(1.0 + xp**2 + yp**2)

pz = betagamma / norm
px = xp * pz
py = yp * pz

opal = np.column_stack([x, px, y, py, z, pz])

with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"{len(opal)}\n")
    np.savetxt(f, opal, fmt="%.12e")

print(f"Archivo escrito: {output_file}")
print(f"N partículas = {len(opal)}")
print(f"mean beta*gamma = {np.mean(np.sqrt(px**2 + py**2 + pz**2)):.8e}")
print(f"mean pz = {np.mean(pz):.8e}")
print(f"mean Ekin = {np.mean(Ekin_MeV):.8e} MeV")
xp_check = px / pz
yp_check = py / pz

print("max |xp_check - xp| =", np.max(np.abs(xp_check - xp)))
print("max |yp_check - yp| =", np.max(np.abs(yp_check - yp)))

bg_check = np.sqrt(px**2 + py**2 + pz**2)

print("mean beta*gamma original =", np.mean(betagamma))
print("mean beta*gamma OPAL     =", np.mean(bg_check))
print("std difference           =", np.std(bg_check - betagamma))