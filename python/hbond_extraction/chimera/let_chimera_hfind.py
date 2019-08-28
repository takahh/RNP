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
pdb_list_dic, file_list_dic, done_list_dic = {}, {}, {}
skip_list = ['4uyj', '6bbo','6b0b','1xpu']

# ----------------------------------------------------------
# make a done-list
# ----------------------------------------------------------
for xprm in ('xray_cif/', 'EM_cif/'):
	done_list = []
	for ciffile in os.listdir(hbout_path + xprm):
		done_list.append(ciffile[0:4])
	done_list_dic[xprm[:-5]] = done_list

# ----------------------------------------------------------
# make a pdb file list
# ----------------------------------------------------------
for xprm in ('xray/', 'EM/'):
	pdb_list = []
	for pdbfile in os.listdir(pdb_path + xprm):
		pdb_list.append(pdbfile[0:4])
	pdb_list_dic[xprm[:-1]] = pdb_list

# ----------------------------------------------------------
# make a cif file list sorted by the file size
# ----------------------------------------------------------
def sorted_cif_list():
	for exp in ('xray', 'EM'):
		all_files = (os.path.join(basedir, filename) for basedir,\
					dirs, files in os.walk(cif_path + exp + '_cif/')\
					 for filename in files)
		sorted_files = sorted(all_files, key=os.path.getsize)
		file_list_dic[exp] = sorted_files
	return file_list_dic

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
os.chdir(path)
for xprm in (['EM_cif/']):
# for xprm in (['xray_cif/']):
	cif_list_dic = sorted_cif_list()
	xprm_s = xprm.replace('_cif/', '')
	for ciffile in cif_list_dic[xprm_s]:
		cif_filename = ciffile.split('/')[-1]
		# print("open " + pdb_path + xprm_s + '/' + cif_filename[0:4] + '.pdb')
		if cif_filename[0:4] in skip_list: # skip erroneous entry
			continue
		if '.cif' not in ciffile or cif_filename[0:4] in done_list_dic[xprm_s]:
			continue
		if cif_filename[0:4] in pdb_list_dic[xprm[:-5]]:
			rc("open " + pdb_path + xprm_s + '/' + cif_filename[0:4] + '.pdb')
			print(cif_filename + ' :READING PDB FILE INSTEAD !!!!')
		else:
			print(cif_filename + ' :READING CIF FILE !!!!')
			rc("open " + ciffile)
		output_file = hbout_path + xprm + cif_filename.replace('cif', 'hb2')
		# ----------------------------------------------------------
		# create copies in 5A around #0, find hbonds, and then
		# (later) choose bonds including #0
		# ----------------------------------------------------------
		try:
			if 'xray' in xprm:
				rc("cryst #0 5 copies true") # create copies in 5A around model #0
			rc("hbonds namingStyle simples showDist true intraMol false intraRes false saveFile " + output_file)
			rc("close all")
		except ValueError as e:
			print('VALUEERROR!!!!!!!!!!!')
			print(e)
		except TypeError:
			print('TypeError!!!!')
			rc("close all")
			print(cif_filename + ' :READING CIF FILE !!!!')
			rc("open " + ciffile)
			if 'xray' in xprm:
				rc("cryst #0 5 copies true") # create copies in 5A around model #0
			rc("hbonds namingStyle simples showDist true intraMol false intraRes false batch true saveFile " + output_file)
			rc("close all")