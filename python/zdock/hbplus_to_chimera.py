# ----------------------------------------------------------
# this code is for converting hbplus output to chimera output
# input: a folder of hbplus output
# output: a folder of chimera style output
# ----------------------------------------------------------


def hbout_to_chimeraout(i_path, o_path):

	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------
	import os

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


input_path = '/Users/tkimura/Desktop/RNP/zdock/hb2/3iyq/'
output_path = '/Users/tkimura/Desktop/RNP/zdock/chimera_format/3iyq/'

hbout_to_chimeraout(input_path, output_path)