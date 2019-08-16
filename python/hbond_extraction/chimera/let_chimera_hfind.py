# ----------------------------------------------------------
# this code is for
# 1. build a larger model around #0
# 2. get hbonds
#       via chimera
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import os
from chimera import runCommand as rc

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
path = '/Users/tkimura/Desktop/RNP/'
cif_path = path + 'downloads_PDB/'
pdb_path = path + 'check_contact/PDBfiles/'
hbout_path = path + 'check_contact/chimera_hb_out/'
done_list,pdb_list = [], []

# ----------------------------------------------------------
# make a done-list
# ----------------------------------------------------------
for xprm in ('xray_cif/', 'EM_cif/'):
	for ciffile in os.listdir(hbout_path + xprm):
		done_list.append(ciffile[0:4])

# ----------------------------------------------------------
# make a pdb file list
# ----------------------------------------------------------
for xprm in ('xray/', 'EM/'):
	for pdbfile in os.listdir(pdb_path + xprm):
		pdb_list.append(pdbfile[0:4])

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
os.chdir(path)
for xprm in ('xray_cif/', 'EM_cif/'):
	for ciffile in os.listdir(cif_path + xprm):
		if '.cif' not in ciffile or ciffile[0:4] in done_list:
			continue
		if ciffile[0:4] + '.pdb' in pdb_list:
			rc("open " + pdb_path + xprm + ciffile[0:4] + '.pdb')
			print(ciffile + ' :READING PDB FILE INSTEAD !!!!')
		else:
			print(ciffile + ' :READING CIF FILE !!!!')
			rc("open " + cif_path + xprm + ciffile)
		output_file = hbout_path + xprm + ciffile.replace('cif', 'hb2')
		# ----------------------------------------------------------
		# create copies in 5A around #0, find hbonds, and then
		# (later) choose bonds including #0
		# ----------------------------------------------------------
		rc("cryst #0 5 copies true") # create copies in 5A around model #0
		rc("hbonds showDist true intraMol false intraRes false saveFile " + output_file)
		rc("close all")