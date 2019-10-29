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
positive = "/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt"
range_max = '/Users/tkimura/Desktop/RNP/svm/w_range_max.csv'
range_min = '/Users/tkimura/Desktop/RNP/svm/w_range_min.csv'
angles = []

# ----------------------------------------------------------
# preprocess : read files
# ----------------------------------------------------------
df_nega = pd.read_csv(negatives)
df_nega['vec_id_short'] = df_nega['vec_id'].apply(lambda x: x.split('_')[0] + '_' + x.split('_')[1] + '_' + x.split('_')[2])
df_posi = pd.read_csv(positive)
df_svm = pd.read_csv(svm)
num_list = list(range(79))
column_names = ['id']
for i in range(len(num_list)):
	column_names.append(',' + str(num_list[i]))

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
	for i in range(0, 79): # i == 2 , x3
		val = 1
		for j in range(i + 1): # i == 2, x3
			if j != i:
				val *= math.sin(pol[j])
			else:
				val *= math.cos(pol[j])
		vec.append(val)
	return vec


# count posi count with the w
def count_posi(vec, id):

	wx_list = []
	df_nega_target = df_nega[df_nega['vec_id_short'] == id]
	posi_vec = df_posi[df_posi['vec_id'] == id].values.tolist()[0][2:82]

	# calcluate wx and make a dataframe
	for index, row in df_nega_target.iterrows():
		n_vec = row.tolist()[2:82]
		wx = sum([x * y for x, y in zip(n_vec, vec)])
		wx_list.append([0, wx])
	wx = sum([x * y for x, y in zip(posi_vec, vec)])
	wx_list.append([1, wx])

	# sort by wx values
	df_result_sorted = pd.DataFrame(wx_list, columns=['p_or_n', 'wx']).sort_values('wx', ascending=False)

	# find the ranking of the positive
	i = 1
	for index, row in df_result_sorted.iterrows():
		if row['p_or_n'] == 1:
			rank = i
			break
		else:
			i += 1
	return rank


# ----------------------------------------------------------
# main
# ----------------------------------------------------------
with open(range_max, 'w') as fo:
	fo.writelines(column_names)
	pass

with open(range_min, 'w') as fo:
	fo.writelines(column_names)
	pass

id_list = df_svm['chain'].to_list()
incre = [1/(np.pi)] * 79  # initial increment
converge_thrhd = 0.0001
half_rate = 0.3

for id in id_list:
	vec = df_svm[df_svm['chain'] == id].values.tolist()[0][5:85] # svm'ed solution (vector)
	pol = car2pol(vec)  # to polar: initial angles
	xpol = pol
	last_good_xpol = xpol
	npol = pol
	last_good_npol = npol
	ini_rank = count_posi(vec, id)
	maxpol, minpol = [], []
	print(id)

	with open(range_max, 'a') as fo:
		incre = [1/(np.pi)] * 79  # initial increment
		for j in range(79):
			# find max pol
			print(f'max {j}')
			for k in range(0, 1000):
				if incre[j] < converge_thrhd:
					break
				xpol = [xpol[i] + incre[i] if i == j else xpol[i] for i in range(len(xpol))]  # increment 1/2pi
				vec = pol2car(xpol)  # to cartesian
				if ini_rank != count_posi(vec, id):
					incre[j] = incre[j] * half_rate
					vec = last_good_xpol
				else:
					last_good_xpol = vec
					continue
			last_good_xpol.append(xpol[j])
		fo.writelines(str(id) + ',' + str(last_good_xpol) + '\n')
		print(str(id) + ',' + str(last_good_xpol) + '\n')

	with open(range_min, 'a') as fo:
		incre = [1 / (np.pi)] * 79  # initial increment
		for j in range(79):
			# find max pol
			print(f'min {j}')
			for k in range(0, 1000):
				if incre[j] < converge_thrhd:
					break
				npol = [npol[i] + incre[i] if i == j else npol[i] for i in range(len(npol))]  # increment 1/2pi
				vec = pol2car(npol)  # to cartesian
				if ini_rank != count_posi(vec, id):
					incre[j] = incre[j] * half_rate
					vec = last_good_npol
				else:
					last_good_npol = vec
					continue
			last_good_xpol.append(npol[j])
		fo.writelines(str(id) + ',' + str(last_good_npol) + '\n')
		print(str(id) + ',' + str(last_good_npol) + '\n')
