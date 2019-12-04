# ----------------------------------------------------------
# this code is for running a series of scripts
# 1 run_hbplus, 2 hbplus_to_chimera, 3 clean_hbout.py
# 4 hbond_summary_to_classify, 5 non_redundant_positives
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
# from run_hbplus_mpi import run_hbplus
# from hbplus_to_chimera import hbplus_to_chimera
# from run_chimera import run_chimera
# from clean_hbout import clean_hbout
from hbond_summary_to_classify import hbond_summary_to_classify
# from python.zdock.hbond_summary_to_classify_atom import hbond_summary_to_classify
from non_redundant_positives import non_redundant_negatives
# # from python.zdock.non_redundant_positives_atom import non_redundant_negatives
# from combine_summary_files import combine

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
# bpath = '/Users/tkimura/Desktop/RNP/python/zdock/'
cleaned = '/gs/hs0/tga-science/kimura/zdock/cleaned_hbonds/'
# poses = bpath + 'poses/'
# hb2 = bpath + 'hbplus/'
# chimera = bpath + 'chimera_format/'
# cleaned = bpath + 'cleaned_hbonds/'
summary = '/gs/hs0/tga-science/kimura/zdock/'
summaryfile = '/gs/hs0/tga-science/kimura/zdock/hbond_summary.csv'
vector = '/gs/hs0/tga-science/kimura/zdock/vectors.csv'
# summary = bpath
# summaryfile = bpath + 'hbond_summary.csv'
# vector = bpath + 'vectors.csv'

# ----------------------------------------------------------
# main
# ----------------------------------------------------------

# prepare mpi
from mpi4py import MPI
from subprocess import call

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
id_list = []

# -----------------------
# dstribute id to f_node
# -----------------------
idfile = '/Users/tkimura/Desktop/t3_mnt/zdock/pdbid_hfrac_ltoeq_2.csv'

with open(idfile) as f:
	for lines in f.readlines():
		alllist = lines.replace('\ufeff','').split(',')
		break

each_amount = int(round(len(alllist)/28) + 1)

for i in range(0, 28):
	if str(rank) == str(i):
		n_from = each_amount*i
		n_to = each_amount*(i+1)
		id_list = alllist[n_from : n_to]

# args_to_pass = '/Users/tkimura/Desktop/RNP/python/zdock/run_chimera.py ' + poses + ' ' + chimera + ' ' + str(rank)
# call(['pychimera', '--nogui', '--script', args_to_pass], shell=True)

# run_chimera(poses, chimera, id_list)
# run_chimera(poses, chimera, alllist)

# run_hbplus(poses, hb2, id_list)
# hbplus_to_chimera(hb2, chimera, id_list)
# clean_hbout(chimera, cleaned, id_list)
hbond_summary_to_classify(cleaned, summary)
# combine(summary, summaryfile)
non_redundant_negatives(summaryfile, vector)