# ----------------------------------------------------------
# this code is for removing anisou lines in poses
#
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import pandas as pd
import os, shutil

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
anisoulist = '/Users/tkimura/Desktop/RNP/check_contact/anisou_list_xray.csv'
pdb_dir = '/Users/tkimura/Desktop/RNP/check_contact/PDBfiles/xray/'
# cif_dir = '/Users/tkimura/Desktop/RNP/downloads_PDB/xray_cif/'
base_pdb_nega = '/Users/tkimura/Desktop/RNP/zdock/pdb/' # AAAA_A_A/AAAA_p.pdb

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
df = pd.read_csv(anisoulist, header=None)
ani_list = df[0].tolist()
print(ani_list)

for dir in os.listdir(base_pdb_nega):
	if dir[:4] in ani_list:
		for files in os.listdir(base_pdb_nega + dir):
			original = base_pdb_nega + dir + '/' + files
			temp = base_pdb_nega + dir + '/' + files + '.tmp'
			shutil.copy2(original, temp)
			with open(original, 'w') as fo:
				with open(temp) as f:
					for lines in f.readlines():
						if 'ANISOU' not in lines:
							fo.writelines(lines)
			os.remove(temp)
