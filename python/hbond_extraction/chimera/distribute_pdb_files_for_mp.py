# ----------------------------------------------------------
# this code is for distributing pdb files to
# several folders for multiprocessing
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import os, sys, shutil

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
path = '/Users/tkimura/Desktop/RNP/downloads_PDB/'
# exps = ['xray_cif', 'EM_cif']
exps = ['EM_cif']
file_list_dic = {}

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------
# make a list for files sorted by file size
for exp in exps:
	all_files = (os.path.join(basedir, filename) for basedir, dirs, files in os.walk(path + exp) for filename in files)
	sorted_files = sorted(all_files, key=os.path.getsize)
	file_list_dic[exp] = sorted_files

# move files one by one to folders
for exp in exps:
	i = 0
	for file in file_list_dic[exp]:
		if '.cif' not in file:
			continue
		else:
			shutil.copy2(file, path + exp + '/' + str(i+1))
		i = (i+1)%6

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
