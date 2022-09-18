LATEX=latexmk -pdflua -lualatex='lualatex -shell-esc' -auxdir=build -makeindexfudge -emulate-aux-dir -silent

FORTRAN=gfortran 
STRIP=strip

PYTHON=python3
PYCACHE=.cpython-310.opt-2.pyc

OUTDIR=build

FLAGS=-flto -Ofast -DNDEBUG -march=native -mtune=native -Wall -Wextra -Wpedantic -fPIC -shared
FLAGS+=-fopenmp -Wno-tabs -Winteger-division -fbacktrace
PYFLAGS=-OO

LDLIBS=-lgfortran -lfortran_stdlib 
FINC=-I/usr/include -I/usr/include/fortran_stdlib

OBJ=fastlib.f90.o
PYOBJ=ie.pyc

.PRECIOUS: ${OUTDIR}/%.f90 ${OUTDIR}/%.mod ${OUTDIR}/%.py

main: ${PYOBJ} fastlib.so cleantmp

fastlib.so: $(OBJ:%.o=${OUTDIR}/%.o)
	${FORTRAN} ${FLAGS} ${LDLIBS} $^ -o $@

${OUTDIR}/%.f90.o: ${OUTDIR}/%.f90
	${FORTRAN} -c $< -J${OUTDIR} ${FINC} ${FLAGS} -o $@ 
	
${OUTDIR}/__pycache__/%${PYCACHE}: ${OUTDIR}/%.py
	${PYTHON} ${PYFLAGS} -m py_compile $?
	
%.pyc: ${OUTDIR}/__pycache__/%${PYCACHE}
	cp $< $@

${OUTDIR}/%.py: %.tex
	${LATEX} $?
	
${OUTDIR}/%.f90: ${PYOBJ}
	
cleantmp:
	-rm *.fls
	-rm -rf _minted-*
	
.PHONY: clean
clean:
	-latexmk -c
	-rm -rf build/* 
	-rm fastlib.so
	-rm ie.pyc
