# ----------------------------------------------------------
# this code is for extracting rows including model#0 from raw hb output
# /Users/tkimura/Desktop/RNP/check_contact/chimera_hb_out/xray_cif/4gkj.hb2
# を、model #0 を含む行のみ取り出し、新ファイルとして、
# /Users/tkimura/Desktop/RNP/check_contact/hb_out_cleaned/xray/   に作成。
# ----------------------------------------------------------


def clean_hbonds(from_path, to_path):

	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------
	import os

	for file in os.listdir(from_path):
		if '.DS' in file:
			continue
		with open(to_path + file, 'w') as fo:
			with open(from_path + file) as f:
				for line in f.readlines():
					print(line)
					if 'HOH' not in line:
						#0 7MG 1.D N1 #0 G 1.D N7
						#0 7MG 1.D N2 #0 G 1.D N7
						#0 G 1.P N2 #0 C 1.P O2
						if line.split()[2] != line.split()[6]:
							fo.writelines(line)

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import subprocess, os

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
idlist = ["2von_A_C","2y9h_O_P","1qa6_A_C","1hc8_B_D","6nut_A_D","6nme_A_G","5a7a_A_R","2go5_6_9","2om3_A_R","3j46_5_4","6i2n_D_U","5xwy_A_B","5mq0_V_3","3j0l_F_5","5y88_W_x","3iz4_B_A","4uft_B_R","6e9e_A_B","2xea_A_R","3izz_F_D","3j0q_k_9","5fn1_A_B","3izy_P_N","6iv6_A_G","3j0d_G_A","4ue4_C_A","2xkv_C_B","3j06_A_R","3iyq_B_A","4udv_A_R","3iyr_B_A","5z9w_A_R","4d5n_A_X","6h5q_B_R","6h5s_C_E","1mj1_A_D","5a79_A_R"]
ipath = '/Users/tkimura/Desktop/RNP/zdock/chimera_format/'
opath = '/Users/tkimura/Desktop/RNP/zdock/cleaned_hbonds/'

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
for id in idlist:
	pdbid = id.split('_')[0]
	# pchain = id.split('_')[1]
	# rchain = id.split('_')[2]
	if not os.path.exists(opath + pdbid):
		os.mkdir(opath + pdbid)
	print('here')
	if len(os.listdir(opath + pdbid)) > 3599:
		print('skip ' + pdbid)
		continue
	else:
		print('cleaning ' + pdbid)
		clean_hbonds(ipath + pdbid + '/', opath + pdbid + '/')