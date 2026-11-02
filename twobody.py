import numpy as np
from scipy.integrate import solve_ivp

from elements import MU_EARTH


def two_body_ode(t, p, mu=MU_EARTH):
    """
    Computes RHS of all six de's, coming from
    p = [x, y, z, vx, vy, vz]
    Returns pdot = [vx, vy, vz, ax, ay, az]
    """
    r_ = p[0:3] # first three values of p are r
    v_ = p[3:6] # last three are v

    # perform calcs per vector section
    r = np.linalg.norm(r_)
    a_ = -mu / r ** 3 * r_ 
    pdot = np.concatenate((v_, a_)) 

    return pdot


def propagate_two_body(r0, v0, t0, tf, t_pts, mu=MU_EARTH):
    """
    Integrate the two-body ODE from t0 to tf given r(t0), v(t0),
    using solve_ivp with method='DOP853' which is equivalent to matlab's ODE113.
    
    Returns a scipy OdeResult object -> t: [t0,t1,t2...] and corresp y: [[x_arr], [y_arr], ..., [vz_arr]] (6 x N)
    in our case, sol.y[:, n] = [x_n, y_n, z_n, vx_n, vy_n, vz_n] (state p) for a timepoint n

    to access the necessary values:
    - sol.y[0:3] -> [x_arr, y_arr, z_arr]
    - sol.y[0:3, -1] -> last value in each x, y, z arrays => r(tf) (target)
    (and do the same for other values as necessary, ie: sol.y[3:6, -1] => v(tf))

    """
    p0 = np.concatenate((np.asarray(r0, dtype=float), np.asarray(v0, dtype=float)))

    sol = solve_ivp(
        two_body_ode, (t0, tf), p0, args=(mu,), #args always has to be a tuple
        method="DOP853", rtol=1e-12, atol=1e-12, t_eval=t_pts, #evaluate over t_points ∊ t_range
    )

    return sol
