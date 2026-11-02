from cases import get_case, MIU
from kepler import propagate_kepler


# Demonstration of the Kepler-equation solver with case 1:

# fetch the case
r0, v0, t0, tf = get_case(1)

# solve eqn with given inputs, return r & v vecs at time t (single timepoint)
r, v, _ = propagate_kepler(r0, v0, t0, tf, mu=MIU)

# outputs (only r(t) and v(t))
print("Outputs: r(t), v(t)")
print(f"  r(t) = [{r[0]:.6f}, {r[1]:.6f}, {r[2]:.6f}] km")
print(f"  v(t) = [{v[0]:.6f}, {v[1]:.6f}, {v[2]:.6f}] km/s")