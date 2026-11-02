# HW4 - how to run this

For TA: Quick guide on how to run the code:

## Setup (if on a MAC / if not it's slightly different)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run (from this folder)

```bash
python problem1.py        # Problem 3-1: twoBodyOde + ode113-equivalent integration, 6 cases
python problem2.py        # Problem 3-2: general Kepler-equation solver, demo on Case 1
python problem3to8.py     # Problems 3-3 to 3-8: Cases 1-6, E, nu, r(t)/v(t), ode113 comparison, time series
python problem3to8.py 5   # just one problem (here 3-5); any of 3-8, or several, e.g. 3 7
```

`cases.py` holds the six (t0, tf, r0, v0) cases shared by Problems 3-1 and 3-3 to 3-8.
`twobody.py`, `elements.py`, and `kepler.py` hold the functions used by the scripts above.
`problem3to8.py` holds the shared Problem-3-3-to-3-8 routine `run_case` (parts a-i) and runs it once
per problem with the corresponding case index.
