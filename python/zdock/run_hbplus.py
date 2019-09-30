# ----------------------------------------------------------
# this code is for running hbplus
# to the output files from ZDock server
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import subprocess, os

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
idlist = ["2von_A_C","2y9h_O_P","1qa6_A_C","1hc8_B_D","6nut_A_D","6nme_A_G","5a7a_A_R","2go5_6_9","2om3_A_R","3j46_5_4","6i2n_D_U","5xwy_A_B","5mq0_V_3","3j0l_F_5","5y88_W_x","3iz4_B_A","4uft_B_R","6e9e_A_B","2xea_A_R","3izz_F_D","3j0q_k_9","5fn1_A_B","3izy_P_N","6iv6_A_G","3j0d_G_A","4ue4_C_A","2xkv_C_B","3j06_A_R","3iyq_B_A","4udv_A_R","3iyr_B_A","5z9w_A_R","4d5n_A_X","6h5q_B_R","6h5s_C_E","1mj1_A_D","5a79_A_R"]
path = '/Users/tkimura/Desktop/RNP/zdock/hb2/'
ipath = '/Users/tkimura/Desktop/t3_mnt/zdock/poses/'


# ----------------------------------------------------------
# functions
# ----------------------------------------------------------
def runhbplus(in_folder, out_folder):
	os.chdir(out_folder)
	subprocess.call(['pwd'])
	ifile_list = os.listdir(in_folder)
	ofile_list = os.listdir(out_folder)
	for files in ifile_list:
		# complex.5.cleaned.pdb >> complex.5.cleaned.hb2
		if '.DS' in files or 'hb2' in files:
			continue
		elif 'cleaned.pdb' in files: # zdock output was cleaned for hbplus
			if files.replace('pdb', 'hb2') not in ofile_list:
				subprocess.call(['hbplus', in_folder + files])
		else:
			pass

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
for id in idlist:
	pdbid = id.split('_')[0]
	# pchain = id.split('_')[1]
	# rchain = id.split('_')[2]
	if not os.path.exists(path + pdbid):
		os.mkdir(path + pdbid)
	if len(os.listdir(path + pdbid)) > 3600:
		print('skip ' + pdbid)
		continue
	else:
		print('running ' + pdbid)
		runhbplus(ipath + pdbid + '/', path + pdbid + '/')