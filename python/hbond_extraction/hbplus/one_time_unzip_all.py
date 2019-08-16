path = '/Users/tkimura/Desktop/RNP/check_contact/PDBfiles/'
EM_path = path + 'EM/'
xray_path = path + 'xray/'

import sys, pathlib, os, shutil, subprocess

# for file in os.listdir(xray_path):
	# if '.pdb1.' in file:
		# print(path + file)
		# os.remove(xray_path + file)
	# if '.gz' in file:
	# 	subprocess.call(['gunzip', xray_path + file])
	# if 'bundle' in file:
		# print(path + file)
		# os.remove(xray_path + file)
	# subprocess.call(['hbplus', xray_path + file])

for file in os.listdir(EM_path):
	# if '.pdb1.' in file:
		# print(path + file)
		# os.remove(EM_path + file)
	# if '.gz' in file:
	# 	subprocess.call(['gunzip', EM_path + file])
	# if 'bundle' in file:
		# print(path + file)
		# os.remove(EM_path + file)
	subprocess.call(['cd', '/Users/tkimura/Desktop/RNP/check_contact/hbplus_out/EM'])
	subprocess.call(['hbplus', EM_path + file])