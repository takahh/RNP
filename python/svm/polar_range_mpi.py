# ----------------------------------------------------------
# this code is for calculating a range of angle that
# keeps the best positive count in each set
# YOU SHOULD RUN THIS IN TSUBAME LIKE bacth.sh > test.sh with "MPIEXEC -N 28 ...
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import numpy as np
import math
import pandas as pd

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------

basepath = '/gs/hs0/tga-science/kimura/zdock/python/polar_range_mpi/data_from_laptop/'
svm = basepath + 'svm_out_normed.csv'
# negatives = basepath + "vectors.csv"
# negatives = '/gs/hs0/tga-science/kimura/zdock/vectors.csv'
negatives_dir = basepath + "vectors/"
positive = basepath + "non_redun_positives.txt"
raw_outs = basepath + 'outs/'
angles = []

# ----------------------------------------------------------
# preprocess : read files and simplify vector.csv
# ----------------------------------------------------------
df_posi = pd.read_csv(positive)
num_list = list(range(79))

# make a column list for output file
column_names = ['id']
for i in range(len(num_list)):
	column_names.append(',' + str(num_list[i]))
column_names.append('\n')

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# convert cartesian to polar coordinates
def car2pol(vec):
	pol = []
	for i in range(0, 79):
		tsum = 0

		# calculate the denominator part
		for idx, val in enumerate(vec):# i=77, 78th
			if idx < i: # idx < 77
				continue
			else:  # idx = 77, 78, 79
				tsum += val**2
		if tsum == 0:
			pol.append(0)
		else:
			# calculate each polar
			if i != 78:
				pol.append(np.arccos(vec[i]/tsum**0.5))
			else:
				if vec[-1] >= 0:
					pol.append(np.arccos(vec[i]/tsum**0.5))
				else:
					pol.append(2*np.pi - np.arccos(vec[i]/tsum**0.5))
	return pol


# convert polar to cartesian coordinates
def pol2car(pol):
	vec = []
	for i in range(0, 80): # i == 79
		val = 1
		if i != 79:
			for j in range(i + 1): # i == 79, j = 0 - 79
				if j != i: # except j = 79
					val *= math.sin(pol[j])
				else:  # when i = j = 79
					val *= math.cos(pol[j])
		else: # i = 79, last x
			for j in range(i):
				val *= math.sin(pol[j])
		vec.append(val)
	return vec


# count posi count with the wc
def count_posi(pol, id):
	vec = pol2car(pol) # weights to cartesian for calculating dot product
	wx_list = []
	df_nega_target = pd.read_csv(negatives_dir + id + '.csv')
	print('len(df_nega_target) :' + str(len(df_nega_target)))
	posi_vec = df_posi[df_posi['vec_id'] == id].values.tolist()[0][2:82]
	# calcluate wx and make a dataframe
	for index, row in df_nega_target.iterrows():
		n_vec = row.tolist()[3:83]
		wx = sum([x * y for x, y in zip(n_vec, vec)])
		wx_list.append([0, wx])
	wx = sum([x * y for x, y in zip(posi_vec, vec)])
	wx_list.append([1, wx])

	# sort by wx values
	df_result_sorted = pd.DataFrame(wx_list, columns=['p_or_n', 'wx']).sort_values('wx', ascending=False)
	# find the ranking of the positive
	i = 1

	if df_result_sorted.iloc[0]['p_or_n'] == 1:
		if df_result_sorted.iloc[0]['wx'] - df_result_sorted.iloc[1]['wx'] < converge_thrhd:
			return -1 # almost at the limit
		else:
			return 1
	else:
		for index, row in df_result_sorted.iterrows():
			if row['p_or_n'] == 1:
				rank = i
				break
			else:
				i += 1
		return rank


def initialize_file(file):
	with open(file, 'w') as fo:
		fo.writelines(column_names)


def write_a_list(pairid, pollist, outfile):
	print('writing for ' + pairid + '...\n')
	with open(outfile, 'a') as fo:
		fo.writelines(str(pairid))
		for i in range(len(pollist)):
			fo.writelines(',' + str(pollist[i]))
		fo.writelines('\n')


def sweep_angles(outfile, mode, polar, initial_rank, limit_polar, chid, initial_incre, half_rate, cv_thrhd):
	for j in range(79):
		print(j)
		# ----------------------------------------------
		# initialize variables
		# ----------------------------------------------
		incre = initial_incre
		tmp_pol = polar # can be too large/small
		best_pol = polar  # best polar allowed

		# search a range
		for k in range(0, 1000):
			# ----------------------------------------------
			# update the angle (invcrease or decrease 1 angle)
			# ----------------------------------------------
			if mode == 'max':
				tmp_pol = [tmp_pol[i] + incre[i] if i == j else tmp_pol[i] for i in range(len(tmp_pol))]  # increment an angle
			else:
				tmp_pol = [tmp_pol[i] - incre[i] if i == j else tmp_pol[i] for i in range(len(tmp_pol))]  # decrement an angle

			# ----------------------------------------------
			# calculate the rank
			# ----------------------------------------------
			rank = count_posi(tmp_pol, chid)

			# ----------------------------------------------
			# return or not?
			# ----------------------------------------------
			#  restart the previous when the rank changes
			# or the increase was beyond the angle range
			if (j != 78 and (tmp_pol[j] < 0 or tmp_pol[j] > np.pi)) \
				or (j == 78 and (tmp_pol[j] < 0 or tmp_pol[j] > 2 * np.pi))\
				or (initial_rank != rank):
				incre[j] = incre[j] * half_rate
				tmp_pol = best_pol
				continue

			# ----------------------------------------------
			# converge or not? get out if the top is very close to the second
			# the step is small? get out!
			# ----------------------------------------------
			if rank == -1 or incre[j] < cv_thrhd:  #
				best_pol = tmp_pol
				break

			# ----------------------------------------------
			# continue
			# ----------------------------------------------
			best_pol = tmp_pol

		limit_polar[j] = best_pol[j]
		print(limit_polar[j])
	write_a_list(chid, limit_polar, outfile)


# check if the id is already in the output
def update_id_list(outfile, id_list):
	df = pd.read_csv(outfile)
	new_id_list = [id for id in id_list if id not in df['id'].values.tolist()]
	return new_id_list


def find_limit(id_list, converge_thrhd, half_rate, rank):
	range_max = raw_outs + 'w_range_max_' + str(rank) + '.csv'
	range_min = raw_outs + 'w_range_min_' + str(rank) + '.csv'
	initialize_file(range_max)
	initialize_file(range_min)

	id_list = update_id_list(range_min, id_list)

	for id in id_list:
		# if check_done(id, range_min) == 1:
		# 	continue
		vec = []
		init_incre = [1/(np.pi)] * 79
		try:
			vec = df_svm[df_svm['chain'] == id].values.tolist()[0][5:85]  # svm'ed solution : Cartesian
		except IndexError:
			# f.writelines('Indexerror\n')
			# f.writelines(df_svm[df_svm['chain'] == id].values.tolist())
			# f.writelines(str(id) + '\n')
			continue
		pol = car2pol(vec)  # to polar: initial angles
		ini_rank = count_posi(pol, id) # keep this rank
		limit_pol = [0] * 79

		sweep_angles(range_max, 'max', pol, ini_rank, limit_pol, id, init_incre, half_rate, converge_thrhd)
		sweep_angles(range_min, 'min', pol, ini_rank, limit_pol, id, init_incre, half_rate, converge_thrhd)


# ----------------------------------------------------------
# main
# ----------------------------------------------------------

# prepare mpi
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# max_all_chain = 0.5 # filter id by the frequency of contacts

df_svm = pd.read_csv(svm)
# all_list = df_posi[df_posi['all_chains'] <= max_all_chain]['vec_id'].unique().tolist()
# alllist = ['5on3_A_B', '5on3_D_E', '5wqe_A_B', '2iz9_A_R', '2iz9_C_S', '2b2e_C_S', '2bq5_C_S', '5wea_A_B', '4aq7_A_B', '4aq7_D_E', '2b2d_C_S', '4pkd_B_V', '1zho_E_F', '5on2_A_B', '5on2_D_E', '4prf_A_B', '2cv2_A_C', '2cv2_B_D', '2xlj_A_B', '2det_A_C', '1b7f_A_P', '2izm_C_S', '3epk_A_E', '3epk_B_F', '5vw1_A_C', '2ab4_A_B', '1zjw_A_B', '5z9x_A_R', '3sn2_A_B', '5w1i_A_B', '5w1i_C_D', '5w1h_A_B', '2yjy_A_C', '2yjy_B_D', '5u34_A_B', '4jvh_A_D', '1n78_A_C', '1n78_B_D', '5xbl_A_B', '4pr6_A_B', '3snp_A_C', '3snp_B_D', '1lng_A_B', '3foz_A_C', '3foz_B_D', '6h9i_B_E', '5vm9_A_B', '5vm9_C_D', '2dxi_A_C', '2dxi_B_D', '1y39_A_C', '1y39_B_D', '4zt9_A_B', '4zt9_C_D', '2re8_A_B', '1gtr_A_B', '3t5q_E_F', '3t5q_K_L', '1gts_A_B', '3q0n_B_D', '5wtk_A_B', '3qjj_A_Q', '3qjj_B_R', '6oon_A_B', '4n0t_A_B', '2oih_A_B', '1cvj_A_M', '1cvj_B_N', '1cvj_E_Q', '1cvj_F_R', '1cvj_G_S', '5wwr_A_C', '5wwr_B_D', '3am1_A_B', '3q0l_B_D', '3q0m_A_C', '3q0m_B_D', '5b63_A_B', '5wws_A_C', '5wws_B_D', '2db3_A_E', '1ob5_A_B', '3k4e_A_B', '3k4e_C_D', '3k4e_E_F', '4pmw_A_C', '4pmw_B_D', '5d6g_A_0', '3amu_A_B', '6gc5_A_E', '5wzg_A_B', '1ivs_A_C', '1ivs_B_D', '3amt_A_B', '1vc6_A_B', '2vpl_C_D', '1ob2_A_B', '6aay_A_B', '2hw8_A_B', '1euq_A_B', '5wwt_A_C', '5wwt_B_D', '2y8w_A_B', '6iv8_A_B', '6iv8_C_D', '6iv9_A_B', '2pjp_A_B', '5wlh_A_B', '4olb_A_B', '1g59_A_B', '1g59_C_D', '4f3t_A_R', '5wty_B_D', '6aax_C_D', '4b3g_A_G', '3wqy_A_C', '1m8y_B_D', '5f5f_G_H', '3q0q_A_B', '4zt0_A_B', '4zt0_C_D', '4tyy_A_B', '5wzh_A_B', '5w6v_A_R', '5bz1_A_B', '5wzi_A_B', '3q0p_B_D', '6qic_D_H', '5msf_A_R', '1mms_A_C', '1mms_B_D', '1m8x_B_D', '3k49_A_B', '3k49_C_D', '3k49_E_F', '1qru_A_B', '5ah5_A_C', '5ah5_B_D', '1drz_A_B', '1e7k_A_C', '3q0s_A_B', '1gax_A_C', '1gax_B_D', '6fpx_A_B', '6fpx_C_D', '1qrt_A_B', '5wt3_A_C', '5bzv_A_B', '5bym_A_C', '1ec6_B_C', '2rd2_A_B', '4tv0_A_B', '1ffy_A_T', '1qrs_A_B', '5yyn_A_B', '1u0b_B_A', '5bzu_A_B', '5bz5_A_B', '1euy_A_B', '5wt1_A_C', '5wt1_B_F', '3ktw_A_C', '3ktw_B_D', '5tf6_A_B', '5tf6_C_D', '1s03_H_A', '1s03_G_B', '3r9x_A_C', '1fxl_A_B', '6dtd_A_C', '4jxz_A_B', '6i3p_C_G', '2i82_A_E', '2i82_B_F', '2i82_D_H', '5i9h_A_B', '1n77_A_C', '1n77_B_D', '5dea_B_A', '1qu3_A_T', '6du5_A_B', '5de5_B_A', '5de5_D_C', '1qa6_B_D', '3akz_C_G', '6ifo_A_C', '6ifo_B_D', '5ng6_A_B', '5ng6_C_D', '5ng6_E_F', '5ng6_G_H', '4jxx_A_B', '6du4_A_B', '1qu2_A_T', '2zzm_A_B', '2zuf_A_B', '1o0b_A_B', '1vfg_B_D', '5npm_A_B', '1o0c_A_B', '1hc8_A_C', '2czj_C_D', '1mfq_B_A', '2vod_A_C', '2zxu_A_C', '2zxu_B_D', '5js1_A_B', '2zm5_A_C', '2zm5_B_D', '2bs0_C_S', '4jyz_A_B', '6f4h_A_B', '6f4h_C_D', '6f4h_E_F', '5onh_A_B', '5onh_D_E', '2vop_A_B', '1qtq_A_B', '2om7_K_J', '6nma_B_G', '3j5s_F_A', '5zey_C_A', '3j0l_J_1', '1ry1_B_A', '5osg_h_2', '6mcb_A_B', '3deg_H_G', '6mcc_A_B', '2j37_B_A', '5zal_A_C', '6nm9_B_G', '6nm9_D_E', '5vzl_A_B']

idfile = '/gs/hs0/tga-science/kimura/zdock/pdbid_hfrac_ltoeq_2.csv'
with open(idfile) as f:
	for lines in f.readlines():
		alllist = lines.replace('\ufeff','').split(',')
		break

# -----------------------
# dstribute id to f_node
# -----------------------
each_amount = round(len(alllist)/28) + 1
id_list = []

for i in range(0, 28):
	if str(rank) == str(i):
		n_from = each_amount*i
		n_to = each_amount*(i+1)
		id_list = alllist[n_from : n_to]

path = '/gs/hs0/tga-science/kimura/zdock/python/'
log = path + 'polar_range_mpi.py.log'

converge_thrhd = 0.000001
half_rate = 0.3

find_limit(id_list, converge_thrhd, half_rate, rank)