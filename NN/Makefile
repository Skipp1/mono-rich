LATEX=latexmk -pdf -pdflatex='pdflatex -shell-esc' -auxdir=build -makeindexfudge -emulate-aux-dir -quiet

FORTRAN=gfortran 
CXX=g++
STRIP=strip

PYTHON=python3
PYCACHE=.cpython-310.opt-2.pyc

OUTDIR=build

FLAGS=-flto -Ofast -DNDEBUG -march=native -mtune=native -Wall -Wextra -Wpedantic -fPIC -shared -fopenmp
FLAGS+=-finline-limit=500  -fopt-info-all=$@.opt
# FLAGS=-flto -Wall -Wextra -Wpedantic -fpic -shared -g 
CXXFLAGS=${FLAGS} 
FFLAGS=${FLAGS} -Wno-tabs -Winteger-division -fbacktrace
PYFLAGS=-OO

LDLIBS=-lgfortran -lfftw3 -lfftw3f -lfortran_stdlib $(shell root-config --glibs --libs)

FINC=-I/usr/include -I/usr/include/fortran_stdlib
CXXINC=-I/usr/include/root -pthread 

OBJ=writeimg.f90.o nn_fake_gendata.f90.o conv.f90.o loadroot.cpp.o
PYOBJ=nn.pyc

.PRECIOUS: ${OUTDIR}/%.f90 ${OUTDIR}/%.cpp ${OUTDIR}/%.mod ${OUTDIR}/%.py

main: nn_fake_gendata.so ${PYOBJ} CLEANTMP
# main: ${PYOBJ} CLEANTMP

nn_fake_gendata.so: $(OBJ:%.o=${OUTDIR}/%.o)
# 	${STRIP} --strip-all $?
	${CXX} ${LDLIBS} ${CXXFLAGS} $^ -o $@

${OUTDIR}/%.f90.o: ${OUTDIR}/%.f90
	${FORTRAN} -c $? -J${OUTDIR} ${FINC} ${FFLAGS} -o $@ 
	
${OUTDIR}/%.cpp.o: ${OUTDIR}/%.cpp
	${CXX} -c $? ${CXXINC} ${CXXFLAGS} -o $@ 

${OUTDIR}/%.cpp: %.tex
	${LATEX} $?
	
${OUTDIR}/%.f90: %.tex
	${LATEX} $?

${OUTDIR}/%.py: %.tex
	${LATEX} $?

${OUTDIR}/__pycache__/%${PYCACHE}: ${OUTDIR}/%.py
	${PYTHON} ${PYFLAGS} -m py_compile $?
	
%.pyc: ${OUTDIR}/__pycache__/%${PYCACHE}
	cp $< $@
	
CLEANTMP:
	-rm *.fls
	-rm -rf _minted-*
	-grep -v "function body not available" nn_fake_gendata.so.opt > ${OUTDIR}/nn_fake_gendata.so.opt
	-rm nn_fake_gendata.so.opt
	
.PHONY: clean
clean:
	-latexmk -c
	-rm -rf build/* 
	-rm a.out
	-rm nn_fake_gendata.so
	-rm *.pyc
