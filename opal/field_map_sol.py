import numpy as np
import matplotlib.pyplot as plt


L = 0.2574        # longitud solenoide (m)
z_start = -0.1    
z_end = L + 0.1  

Nz = 2000
B0 = 1.0

fringe = 0.02     


z = np.linspace(z_start, z_end, Nz + 1)


def solenoid_profile(z, z1, z2, a):
    return 0.5 * (np.tanh((z - z1)/a) - np.tanh((z - z2)/a))

Bz = B0 * solenoid_profile(z, 0.0, L, fringe)


plt.figure()
plt.plot(z, Bz)
plt.xlabel("z (m)")
plt.ylabel("Bz (T)")
plt.title("Perfil de campo solenoide (1D)")
plt.grid()


plt.axvline(0, linestyle='--')
plt.axvline(L, linestyle='--')

plt.show()


z_start_cm = z_start * 100
z_end_cm = z_end * 100

with open("solenoid_1D.map", "w") as f:
    f.write("1DMagnetoStatic 40\n")
    f.write(f"{z_start_cm:.4f} {z_end_cm:.4f} {Nz}\n")
    f.write("0.0 2.0 50\n")

    for b in Bz:
        f.write(f"{b:.8e}\n")

print("✔ solenoid_1D.map generado")