import numpy as np

MIU = 398600.0  # km^3/s^2

#pack each case into a dict struct
#create func to fetch case:

CASES = [
    dict(t0_min=1329.16, tf_min=3885.73,
         r0=[68524.298, -17345.863, -51486.409], v0=[-0.578936, 0.957665, 0.357759]),
         
    dict(t0_min=3.93, tf_min=1771.58,
         r0=[2721.965, 3522.863, 5267.244], v0=[9.572396, -0.474701, -2.725664]),
    dict(t0_min=242.82, tf_min=612.69,
         r0=[6997.56, -34108.00, 20765.49], v0=[0.15599, 0.25517, 1.80763]),
    dict(t0_min=616.79, tf_min=1880.41,
         r0=[1882.725, 9864.690, 4086.088], v0=[-5.565367, 5.451548, 2.258105]),
    dict(t0_min=21.02, tf_min=1913.38,
         r0=[-664.699, 8112.75, 4479.81], v0=[-0.87036, -0.068046, -8.290459]),
    dict(t0_min=27.0, tf_min=57.0,
         r0=[-10515.45, -5235.37, 49.17], v0=[-2.10305, -4.18146, 5.56329]),
]


def get_case(idx):
    """gets case #, returns unpacked vars r0, v0, t0, tf"""
    c = CASES[idx - 1]
    r0 = np.array(c["r0"], dtype=float)
    v0 = np.array(c["v0"], dtype=float)
    t0 = c["t0_min"] * 60.0
    tf = c["tf_min"] * 60.0
    return r0, v0, t0, tf
