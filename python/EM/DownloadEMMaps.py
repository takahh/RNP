# ----------------------------------------------------------
# this code is for downloading EM Maps from PDB
#
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import os, shutil, time
from contextlib import closing
from urllib.request import urlopen

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
path = '/Users/tkimura/Desktop/RNP/check_contact/PDBfiles/EM/'

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------

done_list = os.listdir('/Users/tkimura/Desktop/RNP/check_contact/EMmaps/')

for files in os.listdir(path):
	id = ''
	if files.replace('.pdb', '.map') in done_list:
		continue
	if '.pdb' in files:
		print('processing ' + files)
		with open(path + files) as f:
			for lines in f.readlines():
				if ' RELATED DB: EMDB' in lines:
					id = lines.split()[4]
					break
	if id == '':
		print('EMDB NOT FOUND')
		continue
	else:
		url = f'ftp://ftp.wwpdb.org/pub/emdb/structures/{id}/map/emd_{id.replace("EMD-", "")}.map.gz'
		target_path = f'/Users/tkimura/Desktop/RNP/check_contact/EMmaps/{files.replace(".pdb", "")}.map'
		print(target_path)
		print('accessing ' + url)
		time.sleep(5)
		with closing(urlopen(url)) as source:
			with open(target_path, 'wb') as target:
				print('writing... ')
				shutil.copyfileobj(source, target)
		print(files + ' done')
	time.sleep(10)