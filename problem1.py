import numpy as np
import matplotlib.pyplot as plt

#cases repeat thru the hw, make separate file/func.
from cases import CASES, get_case, MIU
from twobody import propagate_two_body

fig = plt.figure(figsize=(14, 9)) #fig size in inches, tweaked to fit report nicely.

for idx in range(1, 7):
    r0, v0, t0, tf = get_case(idx) 

    #prep even time grid
    t_pts = np.linspace(t0, tf, 200)
    sol = propagate_two_body(r0, v0, t0, tf, mu=MIU, t_pts=t_pts)

    # sol -> 
    rf, vf = sol.y[0:3, -1], sol.y[3:6, -1]


    # organize each case output:
    print(f"Case {idx}:")
    print(f"  tf = {tf / 60:.2f} min ({tf:.1f} s)")
    print(f"  r(tf) = [{rf[0]:.6f}, {rf[1]:.6f}, {rf[2]:.6f}] km")
    print(f"  v(tf) = [{vf[0]:.6f}, {vf[1]:.6f}, {vf[2]:.6f}] km/s")

    # plot for the report:
    ax = fig.add_subplot(2, 3, idx, projection="3d")
    ax.plot(sol.y[0], sol.y[1], sol.y[2], color="blue", linewidth=1.25)
    ax.scatter(*r0, color="green", s=30, label="r(t0)")
    ax.scatter(*rf, color="red", s=30, label="r(tf)")
    ax.set(title=f"Case {idx}", xlabel="X (km)", ylabel="Y (km)", zlabel="Z (km)")
    ax.legend(fontsize=7)

plt.tight_layout()
plt.show()
plt.savefig("report/figures/problem1_orbits.png")
