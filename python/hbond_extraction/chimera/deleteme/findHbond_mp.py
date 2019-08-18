# ----------------------------------------------------------
# First I ran find_hbond.py but was very slow because of
# the time for Chimera to read cif files
# so made this code to expedite it
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
from multiprocessing import Process
import os
from chimera import runCommand as rc

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
path = '/Users/tkimura/Desktop/RNP/'
cif_path = path + 'downloads_PDB/'
pdb_path = path + 'check_contact/PDBfiles/'
hbout_path = path + 'check_contact/chimera_hb_out/'

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------
# ----------------------------------------------------------
# make a done-list
# ----------------------------------------------------------
def done_list():
	done_list = []
	for xprm in ('xray_cif/', 'EM_cif/'):
		for ciffile in os.listdir(hbout_path + xprm):
			done_list.append(ciffile[0:4])
	return done_list


# ----------------------------------------------------------
# make a pdb file list
# ----------------------------------------------------------
def pdb_list():
	pdb_list = []
	for xprm in ('xray/', 'EM/'):
		for pdbfile in os.listdir(pdb_path + xprm):
			pdb_list.append(pdbfile[0:4])
	return pdb_list


# ----------------------------------------------------------
# run chimera
# ----------------------------------------------------------
def hfind(folder_path, done_list, pdb_list, hbout_path):
	# run let_chimera_hfind.py for the folder_path
	# after checking completed files
	for ciffile in os.listdir(folder_path):
		if '.cif' not in ciffile or ciffile[0:4] in done_list:
			continue
		if ciffile[0:4] + '.pdb' in pdb_list:
			rc("open " + pdb_path + ciffile[0:4] + '.pdb')
		else:
			rc("open " + folder_path + ciffile)
		output_file = hbout_path + ciffile.replace('cif', 'hb2')
		# ----------------------------------------------------------
		# create copies in 5A around #0, find hbonds, and then
		# (later) choose bonds including #0
		# ----------------------------------------------------------
		rc("cryst #0 5 copies true") # create copies in 5A around model #0
		rc("hbonds showDist true intraMol false intraRes false saveFile " + output_file)
		rc("close all")
		# print('#######################' + ciffile + ' is DONE!!!')


def func_1(xprm):
	folder_path = cif_path + xprm + '/1/'
	hfind(folder_path, done_list, pdb_list, hbout_path + xprm)

def func_2(xprm):
	folder_path = cif_path + xprm + '/2/'
	hfind(folder_path, done_list, pdb_list, hbout_path + xprm)

def func_3(xprm):
	folder_path = cif_path + xprm + '/3/'
	hfind(folder_path, done_list, pdb_list, hbout_path + xprm)

def func_4(xprm):
	folder_path = cif_path + xprm + '/4/'
	hfind(folder_path, done_list, pdb_list, hbout_path + xprm)

def func_5(xprm):
	folder_path = cif_path + xprm + '/5/'
	hfind(folder_path, done_list, pdb_list, hbout_path + xprm)

def func_6(xprm):
	folder_path = cif_path + xprm + '/6/'
	hfind(folder_path, done_list, pdb_list, hbout_path + xprm)

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
done_list = done_list()
pdb_list = pdb_list()

for xprm in ('xray_cif/', 'EM_cif/'):

	p1 = Process(target=func_1, args=(xprm,))
	p1.start()
	p2 = Process(target=func_2, args=(xprm,))
	p2.start()
	p3 = Process(target=func_3, args=(xprm,))
	p3.start()
	p4 = Process(target=func_4, args=(xprm,))
	p4.start()
	p5 = Process(target=func_5, args=(xprm,))
	p5.start()
	p6 = Process(target=func_6, args=(xprm,))
	p6.start()
