# ----------------------------------------------------------
# this code is for running hbplus
# to the output files from ZDock server
# ----------------------------------------------------------

def runhbplus(in_folder, out_folder):

	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------
	import subprocess, os

	# ----------------------------------------------------------
	# constants
	# ----------------------------------------------------------

	# ----------------------------------------------------------
	# functions
	# ----------------------------------------------------------
	os.chdir(out_folder)
	subprocess.call(['pwd'])
	for files in os.listdir(in_folder):
		if '.DS' in files or 'hb2' in files:
			continue
		subprocess.call(['hbplus', in_folder + files])

	# ----------------------------------------------------------
	# main
	# ----------------------------------------------------------

runhbplus('/Users/tkimura/Desktop/RNP/zdock/pdb/3iyq/', '/Users/tkimura/Desktop/RNP/zdock/hb2/3iyq/')