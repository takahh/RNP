# ----------------------------------------------------------
# this code is for running a series of scripts
# 1 run_hbplus, 2 hbplus_to_chimera, 3 clean_hbout.py
# 4 hbond_summary_to_classify, 5 non_redundant_positives
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
from python.zdock.run_hbplus import run_hbplus
from python.zdock.hbplus_to_chimera import hbplus_to_chimera
from python.zdock.clean_hbout import clean_hbout
# from python.zdock.hbond_summary_to_classify import hbond_summary_to_classify
from python.zdock.hbond_summary_to_classify_atom import hbond_summary_to_classify
from python.zdock.non_redundant_positives import non_redundant_negatives
# from python.zdock.non_redundant_positives_atom import non_redundant_negatives

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
poses = '/Users/tkimura/Desktop/t3_mnt/zdock/poses/'
hb2 = '/Users/tkimura/Desktop/t3_mnt/zdock/hbplus/'
chimera = '/Users/tkimura/Desktop/RNP/zdock/chimera_format/'
# cleaned = '/Users/tkimura/Desktop/RNP/zdock/cleaned_hbonds/'
cleaned = '/Users/tkimura/Desktop/t3_mnt/zdock/cleaned_hbonds/'
summary = '/Users/tkimura/Desktop/RNP/zdock/'
summaryfile = '/Users/tkimura/Desktop/RNP/zdock/hbond_summary.csv'
vector = '/Users/tkimura/Desktop/RNP/zdock/vectors.csv'

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
#
# # prepare mpi
# from mpi4py import MPI
#
# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# size = comm.Get_size()
#
# for i in range(0, 28):
# 	if str(rank) == str(i):
# 		n_from = 11 * i
# 		n_to = 11 * (i + 1)
# 		id_list = alllist[n_from: n_to]

# run_hbplus(poses, hb2)
# hbplus_to_chimera(hb2, chimera, id_list)
# clean_hbout(chimera, cleaned, id_list)
hbond_summary_to_classify(cleaned, summary)
non_redundant_negatives(summaryfile, vector)