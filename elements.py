import numpy as np
from scipy.spatial.transform import Rotation as R

MU_EARTH = 398600.0  # km^3/s^2 


def rv_to_elements(r_, v_, mu=MU_EARTH):
    """
    Position & inertial velocity [r, v] -> orbital elements [a, e, O, i, w, nu] (angles in degrees).
    Assumes the planet-centered inertial frame has basis Ix = [1,0,0], Iy = [0,1,0], Iz = [0,0,1].
    """
    norm = lambda vec: np.linalg.norm(vec)

    Ix_ = np.array([1, 0, 0])
    Iy_ = np.array([0, 1, 0])
    Iz_ = np.array([0, 0, 1])

    r_ = np.asarray(r_, dtype=float)
    v_ = np.asarray(v_, dtype=float)

    h_ = np.cross(r_, v_)

    p = (norm(h_) ** 2) / mu
    e_ = (np.cross(v_, h_) / mu) - (r_ / norm(r_))
    e = norm(e_)
    a = p / (1 - e ** 2)
    n_ = np.cross(Iz_, h_)

    angle_inputs = {
        "O": {"A": np.dot(n_, Iy_), "B": np.dot(n_, Ix_), "correction": True},
        "i": {"A": np.dot(h_, np.cross(n_, Iz_)), "B": norm(n_) * np.dot(h_, Iz_), "correction": False},
        "w": {"A": np.dot(e_, np.cross(h_, n_)), "B": norm(h_) * np.dot(e_, n_), "correction": True},
        "nu": {"A": np.dot(r_, np.cross(h_, e_)), "B": norm(h_) * np.dot(r_, e_), "correction": True},
    }

    angles = {}
    for name, inputs in angle_inputs.items():
        angle = np.arctan2(inputs["A"], inputs["B"])
        if inputs["correction"] and angle < 0:
            angle += 2 * np.pi
        angles[name] = angle

    O, i, w, nu = (np.degrees(angles[k]) for k in ("O", "i", "w", "nu"))

    return [a, e, O, i, w, nu]


def elements_to_rv(orbital_parameters, mu=MU_EARTH):
    """
    Orbital elements [a, e, O, i, w, nu] (angles in degrees) -> position & inertial velocity [r, v].
    Perifocal state rotated into the inertial frame with a 3-1-3 (Z-X-Z) rotation (O, i, w).
    """
    a, e, O, i, w, nu = orbital_parameters

    rot1 = R.from_euler('z', O, degrees=True)
    rot2 = R.from_euler('x', i, degrees=True)
    rot3 = R.from_euler('z', w, degrees=True)
    rotation_matrix = rot1 * rot2 * rot3

    nu_rad = np.radians(nu)
    p = a * (1 - e ** 2)
    r = p / (1 + e * np.cos(nu_rad))
    r_perifocal = np.array([r * np.cos(nu_rad), r * np.sin(nu_rad), 0.0])
    v_perifocal = np.sqrt(mu / p) * np.array([-np.sin(nu_rad), e + np.cos(nu_rad), 0.0])

    r_inertial = rotation_matrix.apply(r_perifocal)
    v_inertial = rotation_matrix.apply(v_perifocal)

    return [r_inertial, v_inertial]
