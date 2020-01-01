# ----------------------------------------------------------
# this code is for testing ** mean ** w as solution
# 1. take the mean w as a list from the file
# 2. multiply it to 3600 dekois and 1 native
# 3. see how largest the native score is
# 4. compare the #3 results with the svm results
#    (maybe make a plot)
# ----------------------------------------------------------

def apply_mean(limit_reso, max_all_chain, remove_list, exp):
	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------
	import pandas as pd
	import math, csv, copy
	from subprocess import call
	from python.resolutions.resolution_list import resolution_list as reso
	# ----------------------------------------------------------
	# constants
	# ----------------------------------------------------------
	path = '/Users/tkimura/Desktop/RNP/'
	bpath = '/Users/tkimura/Desktop/RNP/svm/'
	# apath = '/gs/hs0/tga-science/kimura/zdock/'
	apath = '/Users/tkimura/Desktop/t3_mnt/zdock/'
	vec_path = apath + 'vectors/'

	means = bpath + "best_w.csv"
	svm = apath + 'python/polar_range_mpi/data_from_laptop/svm_out_normed.csv'
	# svm = '/Users/tkimura/Desktop/t3_mnt/zdock/python_vdw/polar_range_mpi/data_from_laptop/svm_out_normed.csv'

	positive = path + "check_contact/non_redun_positives.txt"
	ranking_results = bpath + 'ranking_results_mean_reso_' + str(limit_reso) + '_touch_' + str(max_all_chain) + '.csv'

	# ----------------------------------------------------------
	# preprocess
	# ----------------------------------------------------------
	print('reading file1..')
	df_posi = pd.read_csv(positive)  # ['vec_id', 'exp', 'ALA_A'
	print('reading file2..')
	df_mean = pd.read_csv(means)  # ['vec_id', 'exp', 'ALA_A'
	print('reading file3..')
	df_svm = pd.read_csv(svm)  # ['vec_id', 'exp', 'ALA_A'
	print("df_svm.head(10)")
	print(df_svm.head(10))
	print("df_svm read")
	# mode_list = ['mean', 'median']
	mode_list = ['mean']
	selected_list = df_posi[df_posi['all_chains'] <= max_all_chain]['vec_id'].unique().tolist()
	print('selected list :' + str(len(selected_list)))
	mean_angles = df_mean[' average'].values.tolist()
	if exp != []:
		df_posi = pd.read_csv(positive)
		list_filtered_by_exp = df_posi[df_posi['exp'] == exp]['vec_id'].tolist()
		selected_list = [x for x in selected_list if x in list_filtered_by_exp]
	id_list = []
	selected_list = [x for x in selected_list if x not in remove_list]

	# ----------------------------------------------------------
	# function
	# ----------------------------------------------------------
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

	# make a list for vec_id limited by resolution
	reso_id_list = reso(limit_reso).index.to_list()
	for vec_id in df_svm['chain'].values:
		if vec_id[0:4] in reso_id_list:
			id_list.append(vec_id)

	with open(ranking_results.replace('ranking_results_mean_reso_', 'raw_wx_'), 'w') as fo2:
		fo2.writelines('id,label,score\n')

	# ----------------------------------------------------------
	# main
	# ----------------------------------------------------------
	for mode in mode_list:
		with open(ranking_results, 'w') as fo:
			fo.writelines('id, rank, svm_rank\n')
			for id in id_list:
				# for id in ['2xli_A_B']:
				if id not in selected_list:
					continue
				# prepare data
				print('applying w to ' + str(id))
				df_nega = pd.read_csv(vec_path + id + '.csv')
				# df_nega['vec_id_short'] = df_nega['vec_id'].apply(lambda x: x.split('_')[0] + '_' + x.split('_')[1] + '_' + x.split('_')[2])
				df_nega_target = df_nega
				posi_vec = df_posi[df_posi['vec_id'] == id].values.tolist()[0][2:82]

				# ----------------------------------------------------------
				# get w mean/median
				# ----------------------------------------------------------
				mean_w = pol2car(mean_angles)

				wx_list = []

				# calcluate wx and make a dataframe
				for index, row in df_nega_target.iterrows():
					n_vec = row.tolist()[2:82]
					wx = sum([x*y for x,y in zip(n_vec, mean_w)])
					wx_list.append([0, wx])
				wx = sum([x * y for x, y in zip(posi_vec, mean_w)])
				wx_list.append([1, wx])

				####  write raw wx data to a file  ####
				wx_list2 = copy.deepcopy(wx_list)
				for item in wx_list2:
					item.insert(0, id)

				with open(ranking_results.replace('ranking_results_mean_reso_', 'raw_wx_'), 'a') as fo2:
					writer = csv.writer(fo2)
					writer.writerows(wx_list2)

				# sort by wx values
				print(wx_list)
				df_result_sorted = pd.DataFrame(wx_list, columns=['p_or_n', 'wx']).sort_values('wx', ascending=True)

				# find the ranking of the positive
				i = 1
				for index, row in df_result_sorted.iterrows():
					if row['p_or_n'] == 1:
						rank = i
						fo.writelines(id + ',' + str(rank) + ',')
						break
					else:
						i += 1
				# get posi_count in the svm result
				df_svm = pd.read_csv(svm)
				fo.writelines(str(df_svm[df_svm['chain'] == id]['posi_count'].values[0]) + '\n')
				# print(str(df_svm[df_svm['chain'] == id]['posi_count'].values[0]) + '\n')