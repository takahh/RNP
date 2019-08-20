# ----------------------------------------------------------
# this code is for extracting rows including model#0 from raw hb output
# /Users/tkimura/Desktop/RNP/check_contact/chimera_hb_out/xray_cif/4gkj.hb2
# を、model #0 を含む行のみ取り出し、新ファイルとして、
# /Users/tkimura/Desktop/RNP/check_contact/hb_out_cleaned/xray/   に作成。
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import os

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
xprm_list = ['xray', 'EM']
path = '/Users/tkimura/Desktop/RNP/check_contact/'
root_path_from = path + 'chimera_hb_out/'
root_path_to = path + 'hb_out_cleaned/'

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------

# row example
#           111111111122222222223333
# 0123456789012345678901234567890123456789
# #0 SER 18.A OG    #0 HOH 664.A O    no hydrogen  2.769  N/A

for xprm in xprm_list:
	for file in os.listdir(root_path_from + xprm + '_cif/'):
		if '.DS' in file:
			continue
		with open(root_path_to + xprm + '/' + file, 'w') as fo:
			with open(root_path_from + xprm + '_cif/' + file) as f:
				for line in f.readlines():
					if line[0:2] == '#0' and 'HOH' not in line:
						fo.writelines(line)