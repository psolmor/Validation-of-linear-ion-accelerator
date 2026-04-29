import numpy as np

def rms(arr):
    return np.sqrt(np.mean(arr**2) - np.mean(arr)**2)

def emittance(x, xp):
    return np.sqrt(
        (np.mean(x**2) - np.mean(x)**2) *
        (np.mean(xp**2) - np.mean(xp)**2)
        - (np.mean(x*xp) - np.mean(x)*np.mean(xp))**2
    )

E = 0.182629 # MeV

m_c12_6 = 11.9967074084982 #amu
amu = 931.49410372 #MeV
mass = m_c12_6 * amu

gamma = E / mass + 1
betagamma = np.sqrt(gamma**2 - 1)


data = np.loadtxt("inputs/inputPK_lebt_12C6+_2.89uA.txt", skiprows=3)

x  = data[:,0] * 1e-3 #m
y  = data[:,2] * 1e-3 #m
z  = data[:,4] * 1e-3 #m


xp = data[:,1] * 1e-3 # mrad 
yp = data[:,3] * 1e-3 # mrad
pprime = np.sqrt(xp**2 + yp**2 + 1)
betagammaz = betagamma / pprime
betagammax = xp * betagammaz
betagammay = yp * betagammaz



print(f"gamma: {gamma:.6f}")
print(f"beta*gamma: {betagamma:.6f}")
print(f"pprime: {pprime[0]:.6f}")
print(f"betagammaz: {np.mean(betagammaz):.6f}")
out = np.column_stack([x, betagammax, y, betagammay, z, betagammaz])

with open("opal/opal_beam.txt", "w", encoding="utf-8") as output_file:
	output_file.write(f"{len(x)}\n")
	np.savetxt(output_file, out, fmt="%.6e", delimiter=" ")
     
rms_x = rms(x)
rms_y = rms(y)
rms_z = rms(z)

mean_x = np.mean(x)
mean_y = np.mean(y)
mean_z = np.mean(z)

rms_px = rms(betagammax)
rms_py = rms(betagammay)
rms_pz = rms(betagammaz)

mean_px = np.mean(betagammax)
mean_py = np.mean(betagammay)
mean_pz = np.mean(betagammaz)

print("\n************** BUNCH STATS **************")

print(f"RMS beam size   = ({rms_x:.6e}, {rms_y:.6e}, {rms_z:.6e}) [m]")
print(f"Mean position   = ({mean_x:.6e}, {mean_y:.6e}, {mean_z:.6e}) [m]")

print(f"RMS momenta     = ({rms_px:.6e}, {rms_py:.6e}, {rms_pz:.6e}) [beta*gamma]")
print(f"Mean momenta    = ({mean_px:.6e}, {mean_py:.6e}, {mean_pz:.6e}) [beta*gamma]")