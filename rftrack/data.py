import RF_Track as rft
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde



def parser(file="../inputs/beam_outDipole_12C6+.txt"):    
    #Extraer los datos 
    fichero = file


    with open(fichero, "r") as f:
        header = f.readlines()[1] 

    # N_particles, Mass(MeV), Beam_energy(MeV), Beam_Frequency(MHz), Beam_current(A), Beam_Charge
    D0_vals = list(map(float, header.split()))
    N, mass, E, frec, I0, Q = D0_vals

    Q = int(Q)        
    N = int(N)        
    print(f"N: {N}, Mass: {mass} MeV, Energy: {E} MeV, Frequency: {frec} MHz, Current: {I0} A, Charge: {Q} e")

    #  x(mm), x'(mrad), y(mm), y'(mrad), z(mm), z'(mrad), Phase(deg), Time(s), Energy(MeV), Loss
    data_vals = np.loadtxt(fichero, skiprows=3, usecols=(0,1,2,3,4,5,6,7,8,9))

    x   = data_vals[:,0]  # mm
    xp  = data_vals[:,1]  # mrad 
    y   = data_vals[:,2]  # mm
    yp  = data_vals[:,3]  # mrad
    z   = data_vals[:,4]  # mm
    zp  = data_vals[:,5]  # mrad 
    ph  = np.deg2rad(data_vals[:,6])  # rad
    #t   = data_vals[:,7] * 1e3        # s → mm/c aprox (c ≈ 3e8 m/s = 3e11 mm/s)
    t = np.zeros_like(x)

    E_part = data_vals[:,8]        

    p = np.sqrt(E_part * (E_part + 2*mass))  # MeV/c


    frec = frec   
    total_particles = I0 / (Q * 1.602e-19 * frec)
    Ns = np.full(N, total_particles / N)
    Qs = np.full(N, Q)
    ms = np.full(N, mass)


    #x, x', y, y', t, p, mass, charge, N
    F = np.column_stack((x, xp, y, yp, t, p, ms, Qs, Ns))


    return rft.Bunch6d(F)

def parser_volume(file="../inputs/beam_outDipole_12C6+.txt"):
    fichero = file

    with open(fichero, "r") as f:
        header = f.readlines()[1] 

    # N_particles, Mass(MeV), Beam_energy(MeV), Beam_Frequency(MHz), Beam_current(A), Beam_Charge
    N_header, mass, E, frec_MHz, I0, Q = map(float, header.split())

    Q = int(Q)
    N_header = int(N_header)

    print(
        f"N: {N_header}, Mass: {mass} MeV, Energy: {E} MeV, "
        f"Frequency: {frec_MHz} MHz, Current: {I0} A, Charge: {Q} e"
    )

    data_vals = np.loadtxt(
        fichero,
        skiprows=3,
        usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    )

    x   = data_vals[:, 0]  # mm
    xp  = data_vals[:, 1]  # mrad 
    y   = data_vals[:, 2]  # mm
    yp  = data_vals[:, 3]  # mrad
    z   = data_vals[:, 4]  # mm
    zp  = data_vals[:, 5]  # mrad 
    ph  = np.deg2rad(data_vals[:, 6])
    E_part = data_vals[:, 8]  # MeV
    loss = data_vals[:, 9]

    good = loss == 0

    x = x[good]
    xp = xp[good]
    y = y[good]
    yp = yp[good]
    E_part = E_part[good]

    N_macro = len(x)

    t = np.zeros(N_macro)

    p = np.sqrt(E_part * (E_part + 2.0 * mass))  # MeV/c

    e_charge = 1.602176634e-19
    frec_Hz = frec_MHz * 1e6

    total_particles = I0 / (abs(Q) * e_charge * frec_Hz)
    Ns = np.full(N_macro, total_particles / N_macro)

    Qs = np.full(N_macro, Q)
    ms = np.full(N_macro, mass)

    e_charge = 1.602176634e-19
    frec_Hz = frec_MHz * 1e6          # MHz -> Hz

    if np.isclose(I0, 0.0):
        Ns = np.ones(N_macro)
        print("I0 = 0 A: 1 macroparticle.")

    else:
        bunch_charge = I0 / frec_Hz
        macro_charge = bunch_charge / N_macro
        particle_charge = abs(Q) * e_charge

        particles_per_macro = macro_charge / particle_charge

        Ns = np.full(N_macro, particles_per_macro)

        print(f"Bunch charge = {bunch_charge:.6e} C")
        print(f"Charge per macroparticle = {macro_charge:.6e} C")
        print(f"Particles per macroparticle = {particles_per_macro:.6e}")
        print(f"Total current represented = {abs(Q) * e_charge * frec_Hz * np.sum(Ns):.6e} A")

    Qs = np.full(N_macro, Q)
    ms = np.full(N_macro, mass)

    # Bunch6d: x, x', y, y', t, p, mass, charge, N
    F = np.column_stack((x, xp, y, yp, t, p, ms, Qs, Ns))

    return rft.Bunch6d(F)
