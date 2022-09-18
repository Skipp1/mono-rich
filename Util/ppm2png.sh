#! /usr/bin/env sh 

convert $1.ppm -crop 128x109+0+0 -negate $1.png
