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
        lines = f.readlines()

    N_header, mass, E0, frec_MHz, I0, Q = map(float, lines[1].split())

    N_header = int(N_header)
    Q = int(Q)

    print(
        f"N: {N_header}, Mass: {mass} MeV, Energy: {E0} MeV, "
        f"Frequency: {frec_MHz} MHz, Current: {I0} A, Charge: {Q} e"
    )

    data = np.loadtxt(fichero, skiprows=3)

    x    = data[:, 0]   # mm
    xp   = data[:, 1]   # mrad
    y    = data[:, 2]   # mm
    yp   = data[:, 3]   # mrad
    z    = data[:, 4]   # mm
    zp   = data[:, 5]   # mrad
    ph   = data[:, 6]   # deg
    time = data[:, 7]   # s
    Ekin = data[:, 8]   # MeV
    loss = data[:, 9]

    good = loss == 0

    x = x[good]
    xp = xp[good]
    y = y[good]
    yp = yp[good]
    z = z[good]
    Ekin = Ekin[good]

    N_macro = len(x)

    # Momento total relativista [MeV/c]
    P = np.sqrt(Ekin * (Ekin + 2.0 * mass))

    # RF-Track: xp = Px/Pz en mrad
    xp_rad = xp * 1e-3
    yp_rad = yp * 1e-3

    Pz = P / np.sqrt(1.0 + xp_rad**2 + yp_rad**2)
    Px = xp_rad * Pz
    Py = yp_rad * Pz

    ms = np.full(N_macro, mass)
    Qs = np.full(N_macro, Q)

    # N: número de partículas reales por macropartícula
    if I0 == 0:
        Ns = np.ones(N_macro)
    else:
        e_charge = 1.602176634e-19
        frec_Hz = frec_MHz * 1e6
        total_particles = I0 / (abs(Q) * e_charge * frec_Hz)
        Ns = np.full(N_macro, total_particles / N_macro)

    print(f"N por macropartícula: {Ns[0]}")
    print(f"N total representado: {np.sum(Ns)}")

    # Para Bunch6dT: tiempo de creación en mm/c
    t0 = np.zeros(N_macro)

    # Bunch6dT espera:
    # X, Px, Y, Py, Z, Pz, MASS, Q, N, T0
    F = np.column_stack((x, Px, y, Py, z, Pz, ms, Qs, Ns, t0))

    return rft.Bunch6dT(F)
