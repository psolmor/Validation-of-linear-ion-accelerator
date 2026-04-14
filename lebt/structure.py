import RF_Track as rft
import numpy as np

def create_lebt(B0):

    drift1 = rft.Drift(0.260)
    drift1.set_aperture(0.05)

    coll1 = rft.Drift(0.0025)
    coll1.set_aperture_x(0.0179)
    coll1.set_aperture_y(0.0144)

    drift2 = rft.Drift(0.3375)
    drift2.set_aperture(0.05)

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
    dip.set_aperture(0.09)
    dip.set_fint(FINT)
    dip.set_aperture_shape("circular")

    drift3 = rft.Drift(0.208)
    drift3.set_aperture(0.05)

    drift_chop = rft.Drift(0.15)
    drift_chop.set_aperture(0.03)

    drift4 = rft.Drift(0.14)
    drift4.set_aperture(0.055)

    drift5 = rft.Drift(0.722)
    drift5.set_aperture(0.05)

    collx = rft.Drift(0.002)
    collx.set_aperture_shape("circular")
    collx.set_aperture_x(0.0118)
    collx.set_aperture_y(0.04)

    drift_col = rft.Drift(0.002)
    drift_col.set_aperture(0.04)

    colly = rft.Drift(0.002)
    colly.set_aperture_shape("circular")
    colly.set_aperture_y(0.02)
    colly.set_aperture_x(0.04)

    drift6 = rft.Drift(0.194)
    drift6.set_aperture(0.05)

    quad1 = rft.Quadrupole(0.14)
    quad1.set_aperture(0.042)
    quad1.set_gradient(-1.19)

    drift7 = rft.Drift(0.092)
    drift7.set_aperture(0.05)

    quad2 = rft.Quadrupole(0.14)
    quad2.set_aperture(0.042)
    quad2.set_gradient(1.76)


    drift8 = rft.Drift(0.092)
    drift8.set_aperture(0.05)


    quad3 = rft.Quadrupole(0.14)
    quad3.set_aperture(0.042)
    quad3.set_gradient(-2.13)


    drift9 = rft.Drift(0.9101)
    drift9.set_aperture(0.05)


    sol = rft.Solenoid(0.2574,0.344,0.042)


    drift10 = rft.Drift(0.139)
    drift10.set_aperture(0.05)


    lebt = rft.Volume()

    z = 0.0
    lebt.add_ref(drift1, 0, 0, z)
    z += 0.260
    lebt.add_ref(coll1, 0, 0, z)
    z += 0.0025
    lebt.add_ref(drift2, 0, 0, z)
    z += 0.3375
    lebt.add_ref(dip, 0, 0, z)
    z += L   


    #lebt.add_ref(drift3, 0, 0, z)
    #z += 0.208
    #lebt.add_ref(drift_chop, 0, 0, z)
    #z += 0.15
#
    #lebt.add_ref(drift4, 0, 0, z)
    #z += 0.14
#
    #lebt.add_ref(drift5, 0, 0, z)
    #z += 0.722
#
    #lebt.add_ref(collx, 0, 0, z)
    #z += 0.002
#
    #lebt.add_ref(drift_col, 0, 0, z)
    #z += 0.002
#
    #lebt.add_ref(colly, 0, 0, z)
    #z += 0.002
#
    #lebt.add_ref(drift6, 0, 0, z)
    #z += 0.194
#
    #lebt.add_ref(quad1, 0, 0, z)
    #z += 0.14
#
    #lebt.add_ref(drift7, 0, 0, z)
    #z += 0.092
#
    #lebt.add_ref(quad2, 0, 0, z)
    #z += 0.14
#
    #lebt.add_ref(drift8, 0, 0, z)
    #z += 0.092
#
    #lebt.add_ref(quad3, 0, 0, z)
    #z += 0.14
#
    #lebt.add_ref(drift9, 0, 0, z)
    #z += 0.9101
#
    #lebt.add_ref(sol, 0, 0, z)
    #z += 0.2574
#
    #lebt.add_ref(drift10, 0, 0, z)
    #z += 0.139

    return lebt