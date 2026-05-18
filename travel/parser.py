from pathlib import Path
import numpy as np

def rms(arr):
    return np.sqrt(np.mean(arr**2) - np.mean(arr)**2)

def emittance(x, xp):
    return np.sqrt(
        (np.mean(x**2) - np.mean(x)**2) *
        (np.mean(xp**2) - np.mean(xp)**2)
        - (np.mean(x*xp) - np.mean(x)*np.mean(xp))**2
    )

E = 0.182629  # MeV

m_c12_6 = 11.9967074084982  # amu
amu = 931.49410372          # MeV/c^2
mass_MeV = m_c12_6 * amu
mass_GeV = mass_MeV * 1e-3

charge = 6
freq = 749.48e6  # Hz
phis = 0.0       # rad

gamma = E / mass_MeV + 1
betagamma = np.sqrt(gamma**2 - 1)

P0_MeV_c = betagamma * mass_MeV
P0_GeV_c = P0_MeV_c * 1e-3

data = np.loadtxt("inputs/inputPK_lebt_12C6+_2.89uA.txt", skiprows=3)

x = data[:, 0] * 1e-3   # mm -> m
xp = data[:, 1] * 1e-3  # mrad -> rad
y = data[:, 2] * 1e-3   # mm -> m
yp = data[:, 3] * 1e-3  # mrad -> rad
phase = np.zeros_like(x)
dp_p_percent = np.zeros_like(x)  # (P - P0) / P0 in %
lost_flag = np.zeros_like(x)
charge_arr = np.full_like(x, charge)
mass_arr = np.full_like(x, mass_GeV)

out = np.column_stack([
    x,
    xp,
    y,
    yp,
    phase,
    dp_p_percent,
    lost_flag,
    charge_arr,
    mass_arr,
])

output_path = Path("travel/BEAM.DAT")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    f.write("C12 6+ input beam for TRAVEL\n")
    f.write(f"{P0_GeV_c:.12e} {phis:.12e} {freq:.12e} {mass_GeV:.12e} {charge:d}\n")
    f.write(f"{len(x)}\n")
    np.savetxt(f, out, fmt="%.12e")

print(f"Wrote {output_path}")
print(f"gamma:      {gamma:.12e}")
print(f"beta*gamma: {betagamma:.12e}")
print(f"P0:         {P0_GeV_c:.12e} GeV/c")
print(f"mass:       {mass_GeV:.12e} GeV/c2")

rms_x = rms(x)
rms_y = rms(y)
rms_xp = rms(xp)
rms_yp = rms(yp)

emit_x = emittance(x, xp)
emit_y = emittance(y, yp)

print("\n************** TRAVEL INPUT STATS **************")
print(f"RMS x        = {rms_x:.6e} m  = {rms_x*1e3:.6e} mm")
print(f"RMS y        = {rms_y:.6e} m  = {rms_y*1e3:.6e} mm")
print(f"RMS xp       = {rms_xp:.6e} rad = {rms_xp*1e3:.6e} mrad")
print(f"RMS yp       = {rms_yp:.6e} rad = {rms_yp*1e3:.6e} mrad")
print(f"emit_x geom  = {emit_x:.6e} m rad = {emit_x*1e6:.6e} mm mrad")
print(f"emit_y geom  = {emit_y:.6e} m rad = {emit_y*1e6:.6e} mm mrad")
print(f"emit_x norm  = {emit_x*betagamma:.6e} m rad = {emit_x*betagamma*1e6:.6e} mm mrad")
print(f"emit_y norm  = {emit_y*betagamma:.6e} m rad = {emit_y*betagamma*1e6:.6e} mm mrad")