	# ----------------------------------------------------------
	# this code is for finding hbonds in poses from zdock
	# input : /gs/hs0/tga-science/kimura/zdock/poses/
	# out   : /gs/hs0/tga-science/kimura/zdock/chimera_format/
	# ----------------------------------------------------------
def run_chimera(pose_path, outpath, id_list):
	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------
	import os
	from chimera import runCommand as rc

	# ----------------------------------------------------------
	# constants
	# ------------------hbb----------------------------------------
	path = '/Users/tkimura/Desktop/t3_mnt/zdock/'

	# ----------------------------------------------------------
	# make a done_list and to_do_list
	# ----------------------------------------------------------
	done_list = []
	for dir in os.listdir(outpath):
		if len(os.listdir(outpath + dir)) > 3590:
			done_list.append(dir)

	# ----------------------------------------------------------
	# main
	# ----------------------------------------------------------
	os.chdir(path)
	for dir in os.listdir(pose_path):
		if dir in done_list or dir not in id_list:
			continue
		for file in os.listdir(pose_path + dir):
			rc("open " + pose_path + dir + '/' + file)
			output_file = outpath + dir + '/' + file.replace('pdb', 'hb2')
			if not os.path.isdir(outpath + dir):
				os.mkdir(outpath + dir)
		try:
			rc("hbonds namingStyle simples showDist true intraMol false intraRes false saveFile " + output_file)
			rc("close all")
		except ValueError as e:
			print('VALUEERROR!!!!!!!!!!!')
			print(e)
		except TypeError:
			print('TypeError!!!!')
			rc("close all")