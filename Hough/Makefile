LATEX=latexmk -pdf -pdflatex='pdflatex -shell-esc' -auxdir=build -makeindexfudge -emulate-aux-dir -quiet
FORTRAN=gfortran 
CXX=g++

OUTDIR=build

FLAGS=-flto -Ofast -march=native -mtune=native -Wall -Wextra
# FLAGS=-flto -g -Wall -Wextra
CXXFLAGS=${FLAGS} 
FFLAGS=${FLAGS} -fno-stack-arrays -Wno-tabs -fbacktrace

LDLIBS=-lgfortran -lfftw3 -lfftw3f -lfortran_stdlib $(shell root-config --glibs --libs)

FINC=-I/usr/include -I/usr/include/fortran_stdlib
CXXINC=-I/usr/include/root -pthread 

A_OBJ=writeimg.f90.o conv.f90.o rootconv.cpp.o

.PRECIOUS: ${OUTDIR}/%.f90 ${OUTDIR}/%.cpp ${OUTDIR}/%.mod

main: hough cleantmp

hough: $(A_OBJ:%.o=${OUTDIR}/%.o)
	${CXX} ${LDLIBS} ${CXXFLAGS} $^ -o $@

${OUTDIR}/%.f90.o: ${OUTDIR}/%.f90
	${FORTRAN} -c $< -J${OUTDIR} ${FINC} ${FFLAGS} -o $@ 
	
${OUTDIR}/%.cpp.o: ${OUTDIR}/%.cpp
	${CXX} -c $< ${CXXINC} ${CXXFLAGS} -o $@ 

${OUTDIR}/%.cpp: %.tex
	${LATEX} $<
	
${OUTDIR}/%.f90: %.tex
	${LATEX} $<

cleantmp:
	-rm *.fls
	-rm -rf _minted-*
	
.PHONY: clean
clean:
	-latexmk -c
	-rm -rf ${OUTDIR}/* 
	-rm a.out
