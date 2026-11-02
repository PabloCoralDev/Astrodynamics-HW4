import numpy as np

from elements import MU_EARTH, rv_to_elements, elements_to_rv


# necessary eqns and functions 
def true_to_eccentric(nu_deg, e):
    """Eq. 3.23 in notes"""
    nu = np.radians(nu_deg)
    E = 2 * np.arctan2(np.sqrt(1 - e) * np.sin(nu / 2), np.sqrt(1 + e) * np.cos(nu / 2))
    if E < 0:
        E += 2 * np.pi

    return E


def eccentric_to_true(E, e):
    """Eq. 3.21 in notes"""
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    if nu < 0:
        nu += 2 * np.pi

    return np.degrees(nu)


def solve_kepler(E0, e, a, t0, t, mu=MU_EARTH):
    """
    Solve Kepler's equation E - e*sin(E) = C for E at time t, given E0 at t0,
    using fpi, starting with the mean anomaly guess M0, and running for N iters.
    """
    n = np.sqrt(mu / a ** 3)
    k = int(np.floor((n * (t - t0) + (E0 - e * np.sin(E0))) / (2 * np.pi)))  # calculate int # of crossings; solve 3.48 for k.

    C = n * (t - t0) - 2 * np.pi * k + (E0 - e * np.sin(E0))  # Eq. (3.52)

    M0 = E0 - e * np.sin(E0) # mean anomaly at t0
    E = M0  # set initial guess to M0 (3.57)

    N = int(10 * np.ceil(1 / (1 - e)))  # proper num of iters
    for _ in range(N):
        E = e * np.sin(E) + C  # Eq. (3.56): E(k+1) = e*sin(E(k)) + C

    return E


def propagate_kepler(r0, v0, t0, t, mu=MU_EARTH):
    """
    Solves kepler eqn given r0, v0 and t range
    Method (from section 3.5):

      1. r(t0), v(t0) -> orbital elements (a, e, O, i, w, nu0)
      2. nu0 -> E0                                   
      3. E0 -> E(t) via fixed-point Kepler solve      
      4. E(t) -> nu(t)                               
      5. (a, e, O, i, w, nu(t)) -> r(t), v(t)

    Returns r(t), v(t) and intermediary calc values (extra)
    """
    a, e, O, i, w, nu0 = rv_to_elements(r0, v0, mu=mu)

    E0 = true_to_eccentric(nu0, e)
    E = solve_kepler(E0, e, a, t0, t, mu=mu)
    nu = eccentric_to_true(E, e)

    r, v = elements_to_rv([a, e, O, i, w, nu], mu=mu)

    return r, v, {"a": a, "e": e, "O": O, "i": i, "w": w, "nu0": nu0, "E0": E0, "E": E, "nu": nu}
