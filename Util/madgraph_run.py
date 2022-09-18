#! /usr/bin/env python3

import numpy as np
import os

def gg(ss, bs, ms, fn, k):
	out = "modscr/"+fn+"/"
	os.system("mkdir " + out)
	print(os.getpid())
	
	for s in ss:
		for b in bs:
			fp1 = open(out+"/spin"+s+b+"script.txt", "w")
			fp1.write("set auto_convert_model T\n")
			fp1.write("import model mono_spin"+s+b+"\n")
			fp1.write("generate a a > mm+ mm-\n")
			fp1.write("output "+out+"/Pre"+s+b)
			fp1.close()
			
			os.system("./bin/mg5_aMC "+out+"spin"+s+b+"script.txt")
			os.system("sed -i s!maxparticles\.inc!/home/henry/Nextcloud/Imperial/MSc/ns~madgrpah/"+out+"/Pre"+s+b+"/Source/maxparticles.inc!g "+out+"/Pre"+s+b+"/Source/genps.inc")
			
			for m in ms:
				fp2 = open(out+"/spin"+s+b+str(int(m))+"script2.txt", "w")
				fp2.write("launch "+out+"/Pre"+s+b+"\n")
				fp2.write("analysis=madanalysis5\n")
				fp2.write("set run_card ebeam1 4000\n")
				fp2.write("set ebeam2 4000\n")
				fp2.write("set lpp1 2\n")
				fp2.write("set lpp2 2\n")
				fp2.write("set pdlabel lhapdf\n")
				fp2.write("set lhaid 82000\n")
				fp2.write("set nevents 1000000\n")
				fp2.write("set dynamical_scale_choice -1\n")
				fp2.write("set fixed_couplings False\n")
				fp2.write("set param_card mass 25 125\n")
				fp2.write("set mass 4110000 "+str(int(m))+"\n")
				fp2.write("set decay 4110000 0.000000e+0\n")
				if (k != None):
					fp2.write("set kappamon "+str(k)+"\n")
				fp2.write("set gch 1 1.0\n")
				fp2.close()
				os.system("./bin/mg5_aMC "+out+"spin"+s+b+str(int(m))+"script2.txt")

def aa(ss, bs, ms, fn, k):
	out = "modscr/"+fn+"/"
	os.system("mkdir " + out)
	print(os.getpid())
	
	for s in ss:
		for b in bs:
			fp1 = open(out+"/spin"+s+b+"script.txt", "w")
			fp1.write("set auto_convert_model T\n")
			fp1.write("import model mono_spin"+s+b+"\n")
			fp1.write("generate p p > a > mm+ mm-\n")
			fp1.write("output "+out+"/Pre"+s+b)
			fp1.close()
			
			os.system("./bin/mg5_aMC "+out+"spin"+s+b+"script.txt")
			os.system("sed -i s!maxparticles\.inc!/home/henry/Nextcloud/Imperial/MSc/ns~madgrpah/"+out+"/Pre"+s+b+"/Source/maxparticles.inc!g "+out+"/Pre"+s+b+"/Source/genps.inc")
			
			for m in ms:
				fp2 = open(out+"/spin"+s+b+str(int(m))+"script2.txt", "w")
				fp2.write("launch "+out+"/Pre"+s+b+"\n")
				fp2.write("analysis=madanalysis5\n")
				fp2.write("set run_card ebeam1 4000\n")
				fp2.write("set ebeam2 4000\n")
				fp2.write("set lpp1 1\n")
				fp2.write("set lpp2 1\n")
				fp2.write("set pdlabel nn23lo1\n")
				fp2.write("set lhaid 230000\n")
				fp2.write("set nevents 1000000\n")
				fp2.write("set dynamical_scale_choice -1\n")
				fp2.write("set fixed_couplings False\n")
				fp2.write("set param_card mass 25 125\n")
				fp2.write("set mass 4110000 "+str(int(m))+"\n")
				fp2.write("set decay 4110000 0.000000e+0\n")
				if (k != None):
					fp2.write("set kappamon "+str(k)+"\n")
				fp2.write("set gch 1 1.0\n")
				fp2.close()
				os.system("./bin/mg5_aMC "+out+"spin"+s+b+str(int(m))+"script2.txt")

def ggaa(ss, bs, ms, fn, k):
	gg(ss, bs, ms, "gg"+fn, k)
	aa(ss, bs, ms, "aa"+fn, k)

if __name__ == "__main__":
	try:
		#m = np.linspace(1, 3999, 50)
		m = np.linspace(1, 350, 50)
		ggaa(["zero"], ["", "_beta"], m, "-m3-kd-4", None)
		ggaa(["one"],  ["", "_beta"], m, "-m3-k1-4", 1)
		ggaa(["one"],  ["", "_beta"], m, "-m3-k0-4", 0)
		ggaa(["half"], ["", "_beta"], m, "-m3-k0-4", 0)
	except KeyboardInterrupt:
		exit
