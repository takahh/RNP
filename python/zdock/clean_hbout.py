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
					if 'HOH' not in line:
						#0 7MG 1.D N1 #0 G 1.D N7
						#0 7MG 1.D N2 #0 G 1.D N7
						if line.split()[2] != line.split()[6]:
							fo.writelines(line)

from_p = '/Users/tkimura/Desktop/RNP/zdock/chimera_format/3iyq/'
to_p = '/Users/tkimura/Desktop/RNP/zdock/cleaned_hbonds/3iyq/'
clean_hbonds(from_p, to_p)