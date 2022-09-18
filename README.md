# mono-rich
Code used for searching for MM using RICH1

To build this you need OpenMP, Fortran-stdlib and texlive >= 2022 (specifically expl3)  
To read the root files you need ROOT6

For the Hough transform you need FFTW3 installed  
For the NN you need tensorflow, tensorflow-probaility, and tensorflow-datasets

Other dependencies include numpy/scipy/matplotlib/imageio and pylhe 

Finally there are a random collection of texlive dependencies (tikz, babel, etc)

## Hough
Contains all the files needed for the Hough transform 

## NN
Contains all the files needed for the neural network

## Stats 
Contains all the files to add two different pdfs via sampling 

## Util 
Contains scripts to extract data from madgraph and convert ppm to png