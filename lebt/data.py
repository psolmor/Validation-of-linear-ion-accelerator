import RF_Track as rft
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde



def parser(file="../inputs/inputPK_lebt_12C6+_2.89uA.txt"):    
    #Extraer los datos 
    fichero = file


    with open(fichero, "r") as f:
        header = f.readlines()[1] 

    # N_particles, Mass(MeV), Beam_energy(MeV), Beam_Frequency(MHz), Beam_current(A), Beam_Charge
    D0_vals = list(map(float, header.split()))
    N, mass, E, frec, I0, Q = D0_vals

    Q = int(Q) * 6        
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
