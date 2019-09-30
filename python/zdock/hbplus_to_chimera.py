# ----------------------------------------------------------
# this code is for converting hbplus output to chimera output
# input: a folder of hbplus output
# output: a folder of chimera style output
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import os


def hbout_to_chimeraout(i_path, o_path):

	# ----------------------------------------------------------
	# constants
	# ----------------------------------------------------------
	input_list = []
	go = 0

	# ----------------------------------------------------------
	# functions
	# ----------------------------------------------------------

	# ----------------------------------------------------------
	# main
	# ----------------------------------------------------------
	for file in os.listdir(i_path):
		if '.DS' not in file:
			input_list.append(i_path + file)

	for file in input_list:
		go = 0
		with open(file) as f:
			for lines in f.readlines():
				if go == 0:
					if "n    s   type" in lines:
						go = 1
				elif go == 1:
					go = 2 # when at least one data row exists
		if go != 2:
			continue # exit if no data in the file
		with open(o_path + file.split('/')[-1], 'w') as fo:
			with open(file) as f:
				go = 0
				for lines in f.readlines():
					if go == 0:
						if "n    s   type" in lines:
							go = 1
					elif go == 1:
						resi1 = lines[6:9].replace(' ', '')
						atom1 = lines[10:14].replace(' ', '')
						chain1 = lines[0].replace(' ', '')
						resi2 = lines[20:23].replace(' ', '')
						atom2 = lines[24:28].replace(' ', '')
						chain2 = lines[14].replace(' ', '')
						fo.writelines(f'#0 {resi1} 1.{chain1} {atom1} #0 {resi2} 1.{chain2} {atom2}\n')


# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
idlist = ["2von_A_C","2y9h_O_P","1qa6_A_C","1hc8_B_D","6nut_A_D","6nme_A_G","5a7a_A_R","2go5_6_9","2om3_A_R","3j46_5_4","6i2n_D_U","5xwy_A_B","5mq0_V_3","3j0l_F_5","5y88_W_x","3iz4_B_A","4uft_B_R","6e9e_A_B","2xea_A_R","3izz_F_D","3j0q_k_9","5fn1_A_B","3izy_P_N","6iv6_A_G","3j0d_G_A","4ue4_C_A","2xkv_C_B","3j06_A_R","3iyq_B_A","4udv_A_R","3iyr_B_A","5z9w_A_R","4d5n_A_X","6h5q_B_R","6h5s_C_E","1mj1_A_D","5a79_A_R"]
ipath = '/Users/tkimura/Desktop/RNP/zdock/hb2/'
opath = '/Users/tkimura/Desktop/RNP/zdock/chimera_format/'

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
for id in idlist:
	pdbid = id.split('_')[0]
	# pchain = id.split('_')[1]
	# rchain = id.split('_')[2]
	if not os.path.exists(opath + pdbid):
		os.mkdir(opath + pdbid)
	if len(os.listdir(opath + pdbid)) > 3599:
		continue
	hbout_to_chimeraout(ipath + pdbid + '/', opath + pdbid + '/')

