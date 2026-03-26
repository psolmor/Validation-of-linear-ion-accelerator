import RF_Track as rft
import numpy as np

def set_steps(element, length, steps_meter=1000):
    n = max(10, int(length * steps_meter))
    element.set_nsteps(n)
    element.set_tt_nsteps(n)

def create_lebt(B0):

    drift1 = rft.Drift(0.260)
    drift1.set_aperture(0.05)
    set_steps(drift1, 0.260, 800)

    coll1 = rft.Drift(0.0025)
    coll1.set_aperture_x(0.0179)
    coll1.set_aperture_y(0.0144)
    set_steps(coll1, 0.0025)

    drift2 = rft.Drift(0.3375)
    drift2.set_aperture(0.05)
    set_steps(drift2, 0.3375, 800)

    M0 = B0.get_phase_space('%P %Q')
    P0 = np.mean(M0[:,0])
    P_Q = P0 / M0[1,1]

    rho = 0.4
    angle = np.deg2rad(90)
    E1 = np.deg2rad(27)
    E2 = np.deg2rad(27)

    L = rho * angle
    HGAP = 0.020
    FINT = 0.7

    dip = rft.SBend(L, angle, P_Q, E1, E2)
    dip.set_hgap(HGAP)
    dip.set_fint(FINT)
    set_steps(dip, L, 2500)

    print(f"K1_dip: {dip.get_K1()} 1/m^2, Bfield_dip: {dip.get_Bfield()} T") #B field from rftrack
    print(f"B:{P_Q / (299.792458 * rho)} T") # B field from formula

    drift3 = rft.Drift(0.208)
    drift3.set_aperture(0.05)
    set_steps(drift3, 0.208, 800)

    drift_chop = rft.Drift(0.15)
    drift_chop.set_aperture(0.03)
    set_steps(drift_chop, 0.15, 800)

    drift4 = rft.Drift(0.14)
    drift4.set_aperture(0.055)
    set_steps(drift4, 0.14, 800)

    drift5 = rft.Drift(0.722)
    drift5.set_aperture(0.05)
    set_steps(drift5, 0.722, 2000)

    collx = rft.Drift(0.002)
    collx.set_aperture_shape("circular")
    collx.set_aperture_x(0.0118)
    collx.set_aperture_y(0.04)
    set_steps(collx, 0.002)

    drift_col = rft.Drift(0.002)
    drift_col.set_aperture(0.04)
    set_steps(drift_col, 0.002)

    colly = rft.Drift(0.002)
    colly.set_aperture_shape("circular")
    colly.set_aperture_y(0.02)
    colly.set_aperture_x(0.04)
    set_steps(colly, 0.002)

    drift6 = rft.Drift(0.194)
    drift6.set_aperture(0.05)
    set_steps(drift6, 0.194, 800)

    quad1 = rft.Quadrupole(0.14)
    quad1.set_aperture(0.042)
    quad1.set_gradient(-1.19)
    set_steps(quad1, 0.14, 1500)

    drift7 = rft.Drift(0.092)
    drift7.set_aperture(0.05)
    set_steps(drift7, 0.092, 800)

    quad2 = rft.Quadrupole(0.14)
    quad2.set_aperture(0.042)
    quad2.set_gradient(1.76)
    set_steps(quad2, 0.14, 1500)

    drift8 = rft.Drift(0.092)
    drift8.set_aperture(0.05)
    set_steps(drift8, 0.092, 800)

    quad3 = rft.Quadrupole(0.14)
    quad3.set_aperture(0.042)
    quad3.set_gradient(-2.13)
    set_steps(quad3, 0.14, 1500)

    drift9 = rft.Drift(0.9101)
    drift9.set_aperture(0.05)
    set_steps(drift9, 0.9101, 800)

    sol = rft.Solenoid(0.2574,0.344,0.042)
    set_steps(sol, 0.2574, 1800)

    drift10 = rft.Drift(0.139)
    drift10.set_aperture(0.05)
    set_steps(drift10, 0.139, 800)

    lebt = rft.Lattice()

    lebt.append_ref(drift1)
    lebt.append_ref(coll1)
    lebt.append_ref(drift2)
    lebt.append_ref(dip)
    lebt.append_ref(drift3)
    #lebt.append_ref(chopper)
    lebt.append_ref(drift_chop)
    lebt.append_ref(drift4)
    lebt.append_ref(drift5)
    lebt.append_ref(collx)
    lebt.append_ref(drift_col)
    lebt.append_ref(colly)
    #lebt.append_ref(drift6)
    #lebt.append_ref(quad1)
    #lebt.append_ref(drift7)
    #lebt.append_ref(quad2)
    #lebt.append_ref(drift8)
    #lebt.append_ref(quad3)
    #lebt.append_ref(drift9)
    #lebt.append_ref(sol)
    #lebt.append_ref(drift10)

    return lebt