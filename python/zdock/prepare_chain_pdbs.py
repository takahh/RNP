# ----------------------------------------------------------
# this code is for preparing two pdbb files
# INPUT : (pdbid + chainid) list, PDB file
# OUTPUT : pdb file1, pdb file2
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import os, sys
import pandas as pd

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
idlist = ["2von_A_C","2y9h_O_P","1qa6_A_C","1hc8_B_D","6nut_A_D","6nme_A_G","5a7a_A_R","2go5_6_9","2om3_A_R","3j46_5_4","6i2n_D_U","5xwy_A_B","5mq0_V_3","3j0l_F_5","5y88_W_x","3iz4_B_A","4uft_B_R","6e9e_A_B","2xea_A_R","3izz_F_D","3j0q_k_9","5fn1_A_B","3izy_P_N","6iv6_A_G","3j0d_G_A","4ue4_C_A","2xkv_C_B","3j06_A_R","3iyq_B_A","4udv_A_R","3iyr_B_A","5z9w_A_R","4d5n_A_X","6h5q_B_R","6h5s_C_E","1mj1_A_D","5a79_A_R"]
# idlist = ["3iz4_B_A"]
bpath = '/Users/tkimura/Desktop/RNP/check_contact/'
pdb_path_EM = '/Users/tkimura/Desktop/RNP/check_contact/PDBfiles/EM/'
pdb_path_xray = '/Users/tkimura/Desktop/RNP/check_contact/PDBfiles/xray/'
outpath = '/Users/tkimura/Desktop/RNP/zdock/pdb/' # 1ABC/1ABC_r, 1ABC/1ABC_p
path = ''
vec_file = bpath + 'non_redun_positives.txt'

# ----------------------------------------------------------
# preprocess
# ----------------------------------------------------------
df = pd.read_csv(vec_file)
idlist = df['vec_id'].to_list()
print(idlist)

# ----------------------------------------------------------
# main
# ----------------------------------------------------------

# prepare pdb file list
EM_pdb_list = os.listdir(pdb_path_EM)
xray_pdb_list = os.listdir(pdb_path_xray)

keepgoing = 0

for id in idlist:

	pdbid = id.split('_')[0]

	if pdbid == '2ht1':
		keepgoing = 1

	if keepgoing == 1:
		pass
	else:
		continue

	pchain = id.split('_')[1]
	rchain = id.split('_')[2]
	if f'{pdbid}.pdb' in EM_pdb_list:
		path = pdb_path_EM
	elif  f'{pdbid}.pdb' in xray_pdb_list:
		path = pdb_path_xray
	outdir = f'{outpath}/{id}'
	try:
		os.mkdir(outdir)
	except FileExistsError:
		pass

	# make p chain pdb file
	#0123456789012345678901
	#ATOM   3434  CA  GLY A  15
	write = 0
	try:
		with open(f'{outdir}/{pdbid}_p.pdb', 'w') as fo:
			with open(f'{path}/{pdbid}.pdb') as f:
				for lines in f.readlines():
					if write == 0:
						if lines[0:4] == 'ATOM' and len(lines[17:20].strip()) == 3 and lines[20:22].strip() == pchain:
							write = 1
							fo.writelines(lines)
						else:
							continue
					elif write == 1:
						if lines[0:3] == 'TER':
							fo.writelines(lines)
							break
						else:
							fo.writelines(lines)


		# make r chain pdb file
		write = 0
		with open(f'{outdir}/{pdbid}_r.pdb', 'w') as fo:
			with open(f'{path}/{pdbid}.pdb') as f:
				for lines in f.readlines():
					if write == 0:
						if lines[0:4] == 'ATOM' and len(lines[17:20].strip()) == 1 and lines[20:22].strip() == rchain:
							write = 1
							fo.writelines(lines)
						else:
							continue
					elif write == 1:
						if lines[0:3] == 'TER':
							fo.writelines(lines)
							break
						else:
							fo.writelines(lines)
	except FileNotFoundError:
		print(f'{id} not done')
		continue
	print(f'{id} is done')
