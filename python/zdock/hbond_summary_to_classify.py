# ----------------------------------------------------------
# this code is for classifying hbonds
#              0  1   2     3     4  5 6   7
# in   hb      #0 ASN 212.A ND2   #0 U 5.P O4        no hydrogen  2.858  N/A
#      contact {'chain': '6ifr#0.Bp', '#0.Ap': 6, '#0.Ep': 11, '#0.Nr': 17, '#0.Jr': 5}
# out
# {'pdb': '1ABC', 	PDBID
#  'pchain':'p',  	蛋白鎖ID
#  'presi': 'ASP',	蛋白残基
#  'rchain':'q' , 	RNA鎖ID
#  'rresi': 'U',  	RNA塩基
#  'pp':[3,4,2,1],	pp hbond 数のリスト
#  'pr':[1], 		pr
#  'rr':[],         rr
#  'rp':[23, 22],   rp
#  'exp':'EM'}      実験方法
#  'rr_chain'			rr 総鎖数
#  'rp_chain'			rp 総鎖数
#  'pr_chain'			pr 総鎖数
#  'pp_chain'			pp 総鎖数
#  'all_chain'			総鎖数
# ----------------------------------------------------------

def hb_to_summary(from_path, summary_file):
	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------
	import os
	from ast import literal_eval

	# ----------------------------------------------------------
	# constants
	# ----------------------------------------------------------
	with open(summary_file, 'w') as fo:
		fo.writelines('pdbid	exp	presi	pchain	rresi	rchain	pp	pr	rp	rr	allchains	allchains3\n')

	# ----------------------------------------------------------
	# main
	# ----------------------------------------------------------
	with open(summary_file, 'a') as fo:
		for dir in os.listdir(from_path):
			if '.DS' in dir:
				continue
			for file in os.listdir(from_path + dir):
				if '.DS' in file:
					continue
				with open(from_path + dir + '/' + file) as f:
					for lines in f.readlines(): # each hbond
						# 0  1   2     3     4  5 6   7
						# #0 ASN 212.A ND2   #0 U 5.P O4
						pdbid = dir
						element = lines.split()
						if len(element[1].strip()) == 3 and len(element[5].strip()) == 1:
							presi = element[1].strip()
							rresi = element[5].strip()
							pchain = file.split('.')[1] + "_" + element[2].strip().split('.')[1]
							rchain = element[6].strip().split('.')[1]
						elif len(element[1].strip()) == 1 and len(element[5].strip()) == 3:
							presi = element[5].strip()
							rresi = element[1].strip()
							pchain = file.split('.')[1] + "_" + element[6].strip().split('.')[1]
							rchain = element[2].strip().split('.')[1]
						else:
							continue # skip when pp or rr interactions

						fo.writelines(f'{pdbid}	dck	{presi}	{pchain}	{rresi}	{rchain}\n')

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import subprocess, os

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
idlist = ["2von_A_C","2y9h_O_P","1qa6_A_C","1hc8_B_D","6nut_A_D","6nme_A_G","5a7a_A_R","2go5_6_9","2om3_A_R","3j46_5_4","6i2n_D_U","5xwy_A_B","5mq0_V_3","3j0l_F_5","5y88_W_x","3iz4_B_A","4uft_B_R","6e9e_A_B","2xea_A_R","3izz_F_D","3j0q_k_9","5fn1_A_B","3izy_P_N","6iv6_A_G","3j0d_G_A","4ue4_C_A","2xkv_C_B","3j06_A_R","3iyq_B_A","4udv_A_R","3iyr_B_A","5z9w_A_R","4d5n_A_X","6h5q_B_R","6h5s_C_E","1mj1_A_D","5a79_A_R"]
ipath = '/Users/tkimura/Desktop/RNP/zdock/cleaned_hbonds/'
opath = '/Users/tkimura/Desktop/RNP/zdock/'

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
# for id in idlist:
# 	pdbid = id.split('_')[0]
# 	# pchain = id.split('_')[1]
# 	# rchain = id.split('_')[2]
# 	if not os.path.exists(opath + pdbid):
# 		os.mkdir(opath + pdbid)
from_p = ipath
sum_file = opath + 'hbond_summary.csv'

hb_to_summary(from_p, sum_file)