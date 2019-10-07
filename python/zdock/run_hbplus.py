# ----------------------------------------------------------
# this code is for running hbplus
# to the output files from ZDock server
# ----------------------------------------------------------


def run_hbplus(ipath, opath):
	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------
	import subprocess, os

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
	for id in os.listdir(ipath):
		if '.DS' in id:
			continue
		if not os.path.exists(opath + id):
			os.mkdir(opath + id)
		if len(os.listdir(opath + id)) > 3580:
			print('skip ' + id)
			continue
		else:
			print('running ' + id)
			runhbplus(ipath + id + '/', opath + id + '/')