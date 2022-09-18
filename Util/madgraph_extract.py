#!/usr/bin/env python3 

import pylhe
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

def η(p):
	return np.arctanh(p.pz/np.sqrt(p.px**2+p.py**2+p.pz**2))

def β(p, m):
	return np.sqrt(p.px**2+p.py**2+p.pz**2) / np.sqrt(p.px**2+p.py**2+p.pz**2 + m**2)
	
def mkσ(dirs):
	# doing this sort of regex is a lot easier in bash than it is in python
	os.system("cat "+dirs+"/crossx.html | grep results | egrep -Eo \" [0-9e.+-]* \" | tr -d ' ' | sed -E '{N; s/([0-9])\s([0-9])/\\1\\t \\2/g ; P ; D}' | tr -s '\\n' | tail -n +2 > "+dirs+"/tmp_res.tsv")
	return np.loadtxt(dirs+"/tmp_res.tsv")
	
def mkm(dirs):
	d = np.empty(50)
	for i in range(50):
		os.system("grep mmm %s/Events/run_%02d/run_%02d_tag_1_banner.txt | grep -o \"[.0-9e+]* #\" | sed \"s/ #//g\" > %s/Events/run_%02d/mass.txt" % (dirs, i+1, i+1, dirs, i+1))
		d[i] = np.loadtxt("%s/Events/run_%02d/mass.txt" % (dirs, i+1))
	return d.astype(int)

def mkn(dirs):
	d = np.empty(50)
	for i in range(50):
		os.system("grep nevents %s/Events/run_%02d/run_%02d_tag_1_banner.txt | grep -o \"[0-9]*\" > %s/Events/run_%02d/nev.txt" % (dirs, i+1, i+1, dirs, i+1))
		d[i] = np.loadtxt("%s/Events/run_%02d/nev.txt" % (dirs, i+1))
	return d.astype(int)

def mkmom(dirs, i):
	print(i)
	os.system("zgrep -Po \"^ [ -]4110000  1    1    2    0    0 \K[0-9.e+ -]{53}\" %s/Events/run_%02d/unweighted_events.lhe.gz > %s/Events/run_%02d/mom.tsv" % (dirs, i+1, dirs, i+1))
	return np.loadtxt("%s/Events/run_%02d/mom.tsv" % (dirs, i+1))



def mkf(dirs):
	try:
		M_ = mkm(dirs)
		MAX_P = mkn(dirs)
		σ = mkσ(dirs)
		d = np.zeros((50, 2 * np.max(MAX_P), 2))
		for i, m in enumerate(M_):
			e = pylhe.read_lhe_with_attributes(dirs+"/Events/run_"+format(i+1, "02d")+"/unweighted_events.lhe.gz")
			for j, ej in enumerate(e):
				for p in ej.particles:
					if (p.id == 4110000):
						d[i, 2*j, 0] = η(p)
						d[i, 2*j, 1] = β(p, m)
					elif (p.id == -4110000):
						d[i, 2*j+1, 0] = η(p)
						d[i, 2*j+1, 1] = β(p, m)
			print(i)
	except FileNotFoundError:
		print("failed", filename)
		return 0
	np.savez_compressed(dirs + "dat.npz", eta = d[:, :, 0], beta = d[:, :, 1], sigma = σ, m = M_, MAX_P = MAX_P )
	return 

def mkf2(dirs):
	M_ = mkm(dirs)
	MAX_P = mkn(dirs)
	σ = mkσ(dirs)
	eta  = np.zeros((50, 2 * np.max(MAX_P)))
	beta = np.zeros((50, 2 * np.max(MAX_P)))
	for i, m in enumerate(M_):
		p = mkmom(dirs, i)
		ps = np.sum(p**2, axis=1)
		psq = np.sqrt(ps)
		if np.shape(ps)[0] != 2_000_000:
			beta[i, :2*MAX_P[i]] = psq / np.sqrt(ps + m**2)
			eta [i, :2*MAX_P[i]] = np.arctanh(p[:,2]/psq)
			beta[i, 2*MAX_P[i]:] = np.NaN
			eta [i, 2*MAX_P[i]:] = np.NaN
			print(MAX_P)
		else:
			beta[i, :] = psq / np.sqrt(ps + m**2)
			eta[i, :] = np.arctanh(p[:,2]/psq)
	np.savez_compressed(dirs + "dat.npz", eta = eta, beta = beta, sigma = σ, m = M_, MAX_P = MAX_P )

def main():
	print("m", "η", "β;n=1.03", "β;n=1.0014", sep=" | ")
	d = np.zeros( (4,50,4) )
	#for dirs in [*glob.glob("/home/henry/.fasthome/fastdata/gg-m3*/Pre*/"), *glob.glob("/home/henry/fasthome/fastdata/aa-m3*/Pre*/")]:
	for dirs in [*glob.glob("/home/henry/.fasthome/fastdata/aa-m3*/Pre*/")]:
		print(dirs)
		mkf2(dirs)

if __name__ == "__main__":
	main()
