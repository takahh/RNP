# ----------------------------------------------------------
# this code is for running zdock
# on T3
# input : pchain_pdb file, rchain_pdb file
# output : *.out
# ----------------------------------------------------------
def run_zdock(idlist):
	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------
	import subprocess, sys, os

	# ----------------------------------------------------------
	# constants
	# ----------------------------------------------------------
	path = '/Users/tkimura/Desktop/t3_mnt/zdock/'
	idfile = path + 'pdbid_hfrac_ltoeq_2.csv'
	log = path + 'python/run_zdock.py.log'

	# with open(path + 'python/printout.txt', 'w') as fo:
	# 	fo.writelines('making idlist')
	# 	with open(idfile) as f:
	# 		for lines in f.readlines():
	# 			idlist = lines.replace('\ufeff','').split(',')
	# 			break
	# 	fo.writelines('idlist')
	# 	fo.writelines(idlist)

	# ----------------------------------------------------------
	# main
	# ----------------------------------------------------------
	# zdock
	# -R path + 'pdb/1hc8/1hc8_p.pdb'
	# -L path + 'pdb/1hc8/1hc8_r.pdb'
	# -O path + 'outs/1hc8.out'
	# -N 10000

	# make a done_list
	done_list = []
	for file in os.listdir(path + 'outs'):
		done_list.append(file.replace('.out', ''))

	with open(log, 'w') as fo:
		pass

	for id in idlist:
		with open(log, 'a') as fo:
			if id in done_list:
				continue
			pdbid = id.split('_')[0]
			# pchain = id.split('_')[1]
			# rchain = id.split('_')[2]

			# preprocess
			command = 'mark_sur ' + path + 'pdb/' + id + '/' + pdbid + '_p.pdb ' + path + 'pdb/' + id + '/' + id + '_p_m.pdb'
			subprocess.call([command], shell=True)
			fo.writelines(command + '\n')

		with open(log, 'a') as fo:
			command = 'mark_sur ' + path + 'pdb/' + id + '/' + pdbid + '_r.pdb ' + path + 'pdb/' + id + '/' + id + '_r_m.pdb'
			subprocess.call([command], shell=True)
			fo.writelines(command + '\n')

		with open(log, 'a') as fo:
			command = 'zdock -o ' + path + 'outs/' + id + '.out -N 10000 -R ' + path + 'pdb/' + id + '/' + id + '_p_m.pdb -L ' + path + 'pdb/' + id + '/' + id + '_r_m.pdb'
			subprocess.call([command], shell=True)
			fo.writelines(command + '\n')
			fo.writelines(pdbid + ' is done\n')


import mpi4py, pandas
from mpi4py import MPI

# ----------------------------------------------------------
# preprocess
# ----------------------------------------------------------
path = '/Users/tkimura/Desktop/t3_mnt/zdock/'
log = path + 'python/run_zdock.py.log'

# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# size = comm.Get_size()

# if rank == 0:
# 	with open(log, 'a') as fo:
# 		fo.writelines('test!!!!!')

# -----------------------
# dstribute id to f_node
# -----------------------
idfile = '/Users/tkimura/Desktop/t3_mnt/zdock/pdbid_hfrac_ltoeq_2.csv'
anifile = '/Users/tkimura/Desktop/t3_mnt/zdock/python/zdock/anisou_to_rerun_all.csv'

with open(idfile) as f:
	for lines in f.readlines():
		alllist = lines.replace('\ufeff','').split(',')
		break
runlist = []
with open(anifile) as af:
	for lines in af.readlines():
		runlist.append(lines.replace('\n', ''))
runlist_long = []
for item in alllist:
	if item[0:4] in runlist:
		runlist_long.append(item)
		print(item)

each_amount = round(len(runlist_long)/28) + 1

# with open(log, 'a') as fo:
# for i in range(0, 28):
# 	if str(rank) == str(i):
# 		n_from = each_amount*i
# 		n_to = each_amount*(i+1)
# 		id_list = runlist_long[n_from : n_to]


