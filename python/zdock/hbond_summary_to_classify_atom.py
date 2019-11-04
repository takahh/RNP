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
def hbond_summary_to_classify(ipath, opath):

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
			fo.writelines('pdbid	exp	presi	pchain	rresi	rchain	pp	pr	rp	rr	allchains	allchains3	patom	ratom\n')

		# ----------------------------------------------------------
		# main
		# ----------------------------------------------------------
		with open(summary_file, 'a') as fo:
			for dir in os.listdir(from_path):
				if '.DS' in dir:
					continue
				if len(dir) < 5:
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
								patom = element[3].strip()
								ratom = element[7].strip()
							elif len(element[1].strip()) == 1 and len(element[5].strip()) == 3:
								presi = element[5].strip()
								rresi = element[1].strip()
								pchain = file.split('.')[1] + "_" + element[6].strip().split('.')[1]
								rchain = element[2].strip().split('.')[1]
								patom = element[7].strip()
								ratom = element[3].strip()
							else:
								continue # skip when pp or rr interactions
							print(f'{pdbid}	dck	{presi}	{pchain}	{rresi}	{rchain}	{patom}	{ratom}\n')
							fo.writelines(f'{pdbid}	dck	{presi}	{pchain}	{rresi}	{rchain}	{patom}	{ratom}\n')

	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------
	import subprocess, os

	# ----------------------------------------------------------
	# main
	# ----------------------------------------------------------
	from_p = ipath
	sum_file = opath + 'hbond_summary_atom.csv'

	hb_to_summary(from_p, sum_file)