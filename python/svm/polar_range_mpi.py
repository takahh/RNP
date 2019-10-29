# ----------------------------------------------------------
# this code is for calculating a range of angle that
# keeps the best positive count in each set
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

svm = '/Users/tkimura/Desktop/RNP/svm/svm_out_normed.csv'
negatives = "/Users/tkimura/Desktop/RNP/zdock/vectors.csv"
negatives_dir = "/Users/tkimura/Desktop/RNP/zdock/vectors/"
positive = "/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt"
angles = []
debug = '/Users/tkimura/Desktop/RNP/svm/debug.csv'

# ----------------------------------------------------------
# preprocess : read files and simplify vector.csv
# ----------------------------------------------------------
# df_nega = pd.read_csv(negatives)
# df_nega['vec_id_short'] = df_nega['vec_id'].apply(lambda x: x.split('_')[0] + '_' + x.split('_')[1] + '_' + x.split('_')[2])
df_posi = pd.read_csv(positive)
num_list = list(range(79))

# make a column list for output file
column_names = ['id']
for i in range(len(num_list)):
	column_names.append(',' + str(num_list[i]))
column_names.append('\n')

# idlist = df_nega.vec_id_short.unique().tolist()
# for id in idlist: # divide a large file into pieces
# 	df = df_nega[df_nega['vec_id_short'] == id]
# 	df.to_csv(negatives_dir + id + '.csv')
# 	print(id)

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
def check_done(pair_id, outfile):
	df = pd.read_csv(outfile)
	if pair_id in df['id'].values.tolist():
		return 1
	else:
		return 0


def find_limit(id_list, converge_thrhd, half_rate, rank):
	range_max = '/Users/tkimura/Desktop/RNP/svm/w_range_max_' + str(rank) + '.csv'
	range_min = '/Users/tkimura/Desktop/RNP/svm/w_range_min_' + str(rank) + '.csv'
	initialize_file(range_max)
	initialize_file(range_min)
	with open(debug, 'a') as f:
		f.writelines(id_list)

	for id in id_list:
		if check_done(id, range_min) == 1:
			continue
		init_incre = [1/(np.pi)] * 79
		with open(debug, 'a') as f:
			try:
				vec = df_svm[df_svm['chain'] == id].values.tolist()[0][5:85]  # svm'ed solution : Cartesian
			except IndexError:
				f.writelines('Indexerror\n')
				f.writelines(df_svm[df_svm['chain'] == id].values.tolist())
				f.writelines(str(id) + '\n')
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

max_all_chain = 0.1 # filter id by the frequency of contacts

df_svm = pd.read_csv(svm)
all_list = df_posi[df_posi['all_chains'] <= max_all_chain]['vec_id'].unique().tolist()
# all_list = df_svm.chain.unique().tolist()

# if rank == 0:
# 	id_list = all_list[0:43]
# if rank == 1:
# 	id_list = all_list[43:86]
# if rank == 2:
# 	id_list = all_list[86:129]
# if rank == 3:
# 	id_list = all_list[129:172]
# if rank == 4:
# 	id_list = all_list[172:215]
# if rank == 5:
# 	id_list = all_list[215:258]
# elif rank == 6:
# 	id_list = all_list[258:300]

if rank == 0:
	id_list = all_list[0:9]
if rank == 1:
	id_list = all_list[9:18]
if rank == 2:
	id_list = all_list[18:27]
if rank == 3:
	id_list = all_list[27:36]
if rank == 4:
	id_list = all_list[36:45]
if rank == 5:
	id_list = all_list[45:54]
elif rank == 6:
	id_list = all_list[54:60]

converge_thrhd = 0.000001
half_rate = 0.3
# rank = 0

find_limit(id_list, converge_thrhd, half_rate, rank)
# find_limit(all_list, converge_thrhd, half_rate, rank)