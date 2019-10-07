# ----------------------------------------------------------
# this code is for running zdock
# on T3
# input : pchain_pdb file, rchain_pdb file
# output : *.out
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import subprocess
import pandas as pd

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
path = '/gs/hs0/tga-science/kimura/zdock/'
# idlist = ["2von_A_C","2y9h_O_P","1qa6_A_C","1hc8_B_D","6nut_A_D","6nme_A_G","5a7a_A_R","2go5_6_9","2om3_A_R","3j46_5_4","6i2n_D_U","5xwy_A_B","5mq0_V_3","3j0l_F_5","5y88_W_x","3iz4_B_A","4uft_B_R","6e9e_A_B","2xea_A_R","3izz_F_D","3j0q_k_9","5fn1_A_B","3izy_P_N","6iv6_A_G","3j0d_G_A","4ue4_C_A","2xkv_C_B","3j06_A_R","3iyq_B_A","4udv_A_R","3iyr_B_A","5z9w_A_R","4d5n_A_X","6h5q_B_R","6h5s_C_E","1mj1_A_D","5a79_A_R"]
bpath = '/Users/tkimura/Desktop/RNP/check_contact/'
idfile = bpath + 'pdbid_hfrac_ltoeq_0.5.csv'

# ----------------------------------------------------------
# preprocess
# ----------------------------------------------------------
with open(idfile) as f:
	for lines in f.readlines():
		idlist = lines.replace('\ufeff','').split(',')
		break

print(idlist)

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
# zdock
# -R path + 'pdb/1hc8/1hc8_p.pdb'
# -L path + 'pdb/1hc8/1hc8_r.pdb'
# -O path + 'outs/1hc8.out'
# -N 10000

for id in idlist:
	pdbid = id.split('_')[0]
	pchain = id.split('_')[1]
	rchain = id.split('_')[2]

	# preprocess
	command = 'mark_sur ' + path + 'pdb/' + id + '/' + pdbid + '_p.pdb ' + path + 'pdb/' + id + '/' + id + '_p_m.pdb'
	subprocess.call([command], shell=True)
	command = 'mark_sur ' + path + 'pdb/' + id + '/' + pdbid + '_r.pdb ' + path + 'pdb/' + id + '/' + id + '_r_m.pdb'
	subprocess.call([command], shell=True)
	command = 'zdock -o ' + path + 'outs/' + id + '.out -N 10000 -R ' + path + 'pdb/' + id + '/' + id + '_p_m.pdb -L ' + path + 'pdb/' + id + '/' + id + '_r_m.pdb'
	subprocess.call([command], shell=True)
	print(f'{pdbid} is done')


# This is the README file for release 3.0 of ZDOCK program. ZDOCK is an
# initial stage protein-protein docking program, developed initially by
# Rong Chen and Zhiping Weng in 2002. It optimizes pairwise shape
# complementarity, an interface contact potential called IFACE, and
# electrostatic energies using the Fast Fourier Transform algorithm. Please
# cite "Mintseris J, Pierce B, Wiehe K, Anderson R, Chen R, and Weng Z.
# Integrating Statistical Pair Potentials into Protein Complex Prediction.
# Proteins (in press)".
#
# This distribution includes an executable file (zdock) of the ZDOCK program,
# PDB processing file (mark_sur, uniCHARMM, block.pl), and auxiliary files
# (create.pl, create_lig) to create predicted complex structures from a ZDOCK
# output. All executables have been compiled on a 32-bit Linux system. This
# version of ZDOCK 3.0 uses the FFTW3 library to perform its FFTs.
#
# Example:
# mark_sur PDB new_PDB
# zdock -R receptor.pdb -L ligand.pdb -o zdock.out
# create.pl zdock.out
#
# Attention: receptor.pdb, ligand.pdb and create_lig must be in your current
# directory when you try to create all predicted structures using create.pl.
#
# Standard PDB format files must be processed by mark_sur before used as the
# input of ZDOCK. Formatted PDB files of docking benchmark can be downloaded at
# http://zlab.bu.edu/zdock/benchmark.shtml. If you know that some atoms
# are not in the binding site, you can block them by changing their ACE type
# (column 55-56) to 19. This blocking procedure can improve docking
# performance significantly. A blocking script block.pl is included, type
# "block.pl" for usage information.