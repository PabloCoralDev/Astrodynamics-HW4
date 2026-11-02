import numpy as np
import matplotlib.pyplot as plt

from cases import get_case, MIU
from kepler import propagate_kepler
from twobody import propagate_two_body


def run_case(idx, problem_label, savefig_path):
    """
    Shared process from problems 3 thru 8:

    Part 1)
    - get E
    - get nu
    - get ECI r, v at time t with kepler solver (fixed point iteration)
    - get ECI r, v at time t with ode113-eq. solver (numerical integration)
    - compare both methods.

    Part 2)
    - divide into 100 sub intervals & store
    - find ECI r, v at each value of time from prev. Collect into an array.
    - Display the arrays from prev.
    - 3d plot the positions
    
    Cases given are the same as the ones outlined in 1

    """

    # fetch current case values
    r0, v0, t0, tf = get_case(idx)

    # parts a) thru c) 
    r_kep, v_kep, orbit_vals = propagate_kepler(r0, v0, t0, tf, mu=MIU)
    E, nu = orbit_vals["E"], orbit_vals["nu"]


    ## PART 1 ##
    print(f"{problem_label}")

    # a, b)
    print(f"\t(a) E  = {np.degrees(E) % 360:.6f} deg") # convert to degrees
    print(f"\t(b) nu = {nu:.6f} deg")
    # c)
    print(f"\t(c) r(t) = [{r_kep[0]:.6f}, {r_kep[1]:.6f}, {r_kep[2]:.6f}] km")
    print(f"\t\tv(t) = [{v_kep[0]:.6f}, {v_kep[1]:.6f}, {v_kep[2]:.6f}] km/s")

    # part d) compare numerical integration results to kepler
    sol_tf = propagate_two_body(r0, v0, t0, tf, t_pts=[tf], mu=MIU)
    r_ode, v_ode = sol_tf.y[0:3, -1], sol_tf.y[3:6, -1]

    #find diff vector size
    dr = np.linalg.norm(r_kep - r_ode)
    dv = np.linalg.norm(v_kep - v_ode)

    # report dfferences
    print(f"\t(d) ode113 r(t) = [{r_ode[0]:.6f}, {r_ode[1]:.6f}, {r_ode[2]:.6f}] km")
    print(f"\t\tode113 v(t) = [{v_ode[0]:.6f}, {v_ode[1]:.6f}, {v_ode[2]:.6f}] km/s")
    print(f"\t\tnorm(r_kepler - r_ode113) = {dr:.3e} km")
    print(f"\t\tnorm(v_kepler - v_ode113) = {dv:.3e} km/s")


    ## PART 2 ##

    # e, g): do for both ode113 integrator and kepler:

    # set up time points (101 bc linspace is exclusive of last) and shapes:
    t_series = np.linspace(t0, tf, 101)
    r_kepler_series = np.zeros((101, 3))
    v_kepler_series = np.zeros((101, 3))

    # propagate kepler for each
    for k, t_fk in enumerate(t_series):
        rk, vk, _ = propagate_kepler(r0, v0, t0, t_fk, mu=MIU)
        r_kepler_series[k] = rk
        v_kepler_series[k] = vk

    # propagate two body for entire range
    sol_ode = propagate_two_body(r0, v0, t0, tf, mu=MIU, t_pts=t_series)

    r_ode_series = sol_ode.y[0:3].T
    v_ode_series = sol_ode.y[3:6].T

    # h) display arrays and print
    print("\t(e)-(g) Time series (Kepler solver):")
    print(f"\t{'t [s]':>10} {'x [km]':>11} {'y [km]':>11} {'z [km]':>11} {'vx [km/s]':>10} {'vy [km/s]':>10} {'vz [km/s]':>10}")
    for k in range(0, 101):
        x, y, z = r_kepler_series[k]
        vx, vy, vz = v_kepler_series[k]
        print(f"\t{t_series[k]:10.1f} {x:11.3f} {y:11.3f} {z:11.3f} {vx:10.5f} {vy:10.5f} {vz:10.5f}")

    # (i): plot PCI positions from the Kepler solver alongside ode113
    #create figs
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")

    #plot
    ax.plot(*r_kepler_series.T, color="blue", linewidth=1.5, label="Kepler solver")
    ax.plot(*r_ode_series.T, color="red", linewidth=1.0, linestyle="--", label="ode113 (solve_ivp)")
    ax.scatter(*r0, color="green", s=30, label="r(t0)")
    ax.set(title=problem_label, xlabel="X (km)", ylabel="Y (km)", zlabel="Z (km)")
    ax.legend(fontsize=8)

    #save for report
    plt.tight_layout()
    plt.savefig(savefig_path, dpi=500)
    plt.close(fig)

    return r_kepler_series, v_kepler_series, r_ode_series, v_ode_series


# Organize problems with labels and output paths for ease of formatting/output.
PROBLEMS = {
    3: (1, "Problem 3", "report/figures/problem3_orbit.png"),
    4: (2, "Problem 4", "report/figures/problem4_orbit.png"),
    5: (3, "Problem 5", "report/figures/problem5_orbit.png"),
    6: (4, "Problem 6", "report/figures/problem6_orbit.png"),
    7: (5, "Problem 7", "report/figures/problem7_orbit.png"),
    8: (6, "Problem 8", "report/figures/problem8_orbit.png"),
}


## MAIN ##
selected = list(PROBLEMS)
for p in selected:
    run_case(*PROBLEMS[p])
    if len(selected) > 1:
        print()
