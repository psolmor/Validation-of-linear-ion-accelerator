import numpy as np

gambet = 0.0057

data = np.loadtxt("inputs/beam_preSol_12C6+.txt", skiprows=3)

x  = data[:,0] * 1e-3
xp = data[:,1] * 1e-3
y  = data[:,2] * 1e-3
yp = data[:,3] * 1e-3
z  = data[:,4] * 1e-3

px = gambet * xp
py = gambet * yp
pz = np.full_like(px, gambet)

out = np.column_stack([x, px, y, py, z, pz])

np.savetxt("opal/opal_beam.txt", out, fmt="%.6e", delimiter=" ")