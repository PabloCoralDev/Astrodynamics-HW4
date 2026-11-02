PY ?= python3

all: main.pdf

main.pdf: main.tex sections/*.tex figures/*.png outputs/*.txt ../*.py
	pdflatex -interaction=nonstopmode -halt-on-error main.tex
	pdflatex -interaction=nonstopmode -halt-on-error main.tex

# re-run the scripts (from the repo root) to refresh program output and figures
outputs:
	cd .. && MPLBACKEND=Agg $(PY) problem1.py > report/outputs/problem1.txt
	cd .. && $(PY) problem2.py > report/outputs/problem2.txt
	# problem3to8.py runs all six; split its output at each "Problem N" header into problemN.txt
	cd .. && MPLBACKEND=Agg $(PY) problem3to8.py | awk '/^Problem [3-8]$$/ {f = "report/outputs/problem" $$2 ".txt"} f {print > f}'

clean:
	rm -f main.aux main.log main.out main.pdf

.PHONY: all outputs clean
