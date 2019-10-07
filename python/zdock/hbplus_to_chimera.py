# ----------------------------------------------------------
# this code is for converting hbplus output to chimera output
# input: a folder of hbplus output
# output: a folder of chimera style output
# ----------------------------------------------------------


def hbplus_to_chimera(ipath, opath):
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
		print(input_list)
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
	# main
	# ----------------------------------------------------------
	for dir in os.listdir(ipath):
		if '.DS' in dir or len(dir) == 4:
			continue
		if not os.path.exists(opath + dir):
			os.mkdir(opath + dir)
		if len(os.listdir(opath + id)) > 3590:
			print(f'skip {id}')
			continue
		print(f'{dir} is being processed')
		hbout_to_chimeraout(ipath + dir + '/', opath + dir + '/')

