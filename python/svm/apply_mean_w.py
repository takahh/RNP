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
	import math
	from subprocess import call
	from python.resolutions.resolution_list import resolution_list as reso
	# ----------------------------------------------------------
	# constants
	# ----------------------------------------------------------
	means = "/Users/tkimura/Desktop/RNP/svm/best_w.csv"
	bpath = '/Users/tkimura/Desktop/RNP/svm/'
	svm_remote = '/gs/hs0/tga-science/kimura/zdock/python/polar_range_mpi/data_from_laptop/svm_out_normed.csv'
	svm = bpath + 'svm_out_normed.csv'
	negatives_remote = "/gs/hs0/tga-science/kimura/zdock/python/polar_range_mpi/data_from_laptop/vectors.csv"
	negatives = bpath + 'vectors.csv'
	# scp -i ~/.ssh/id_rsa 18D38035@login.t3.gsic.titech.ac.jp:/gs/hs0/tga-science/kimura/zdock/python/polar_range_mpi/data_from_laptop/svm_out_normed.csv /Users/tkimura/Desktop/RNP/svm/
	# copy remote files to local
	command1 = 'scp -i ~/.ssh/id_rsa 18D38035@login.t3.gsic.titech.ac.jp:' + negatives_remote + ' ' + negatives
	call(command1, shell=True)
	command2 = 'scp -i ~/.ssh/id_rsa 18D38035@login.t3.gsic.titech.ac.jp:' + svm_remote + ' ' + svm
	call(command2, shell=True)

	positive = "/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt"
	ranking_results = '/Users/tkimura/Desktop/RNP/svm/ranking_results_mean_reso_' + str(limit_reso) + '_touch_' + str(max_all_chain) + '.csv'

	columnnames = ['chain', 'posi_count',
				'ALA_A', 'ALA_C', 'ALA_G', 'ALA_U', 'ARG_A', 'ARG_C',
				'ARG_G', 'ARG_U', 'ASN_A', 'ASN_C', 'ASN_G', 'ASN_U', 'ASP_A', 'ASP_C',
				'ASP_G', 'ASP_U', 'CYS_A', 'CYS_C', 'CYS_G', 'CYS_U', 'GLU_A', 'GLU_C',
				'GLU_G', 'GLU_U', 'GLN_A', 'GLN_C', 'GLN_G', 'GLN_U', 'GLY_A', 'GLY_C',
				'GLY_G', 'GLY_U', 'HIS_A', 'HIS_C', 'HIS_G', 'HIS_U', 'ILE_A', 'ILE_C',
				'ILE_G', 'ILE_U', 'LEU_A', 'LEU_C', 'LEU_G', 'LEU_U', 'LYS_A', 'LYS_C',
				'LYS_G', 'LYS_U', 'MET_A', 'MET_C', 'MET_G', 'MET_U', 'PHE_A', 'PHE_C',
				'PHE_G', 'PHE_U', 'PRO_A', 'PRO_C', 'PRO_G', 'PRO_U', 'SER_A', 'SER_C',
				'SER_G', 'SER_U', 'THR_A', 'THR_C', 'THR_G', 'THR_U', 'TRP_A', 'TRP_C',
				'TRP_G', 'TRP_U', 'TYR_A', 'TYR_C', 'TYR_G', 'TYR_U', 'VAL_A', 'VAL_C',
				'VAL_G', 'VAL_U']
	# ----------------------------------------------------------
	# preprocess
	# ----------------------------------------------------------
	print('reading nega ...')
	df_nega = pd.read_csv(negatives) # ['vec_id', 'exp', 'ALA_A'
	print('reading nega done')
	df_nega['vec_id_short'] = df_nega['vec_id'].apply(lambda x: x.split('_')[0] + '_' + x.split('_')[1] + '_' + x.split('_')[2])
	df_posi = pd.read_csv(positive)  # ['vec_id', 'exp', 'ALA_A'
	df_mean = pd.read_csv(means)  # ['vec_id', 'exp', 'ALA_A'
	df_svm = pd.read_csv(svm)  # ['vec_id', 'exp', 'ALA_A'
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

	# ----------------------------------------------------------
	# main
	# ----------------------------------------------------------
	for mode in mode_list:
		with open(ranking_results, 'w') as fo:
			fo.writelines('id, rank, svm_rank\n')
			for id in id_list:
			# for id in ['2xli_A_B']:
				print('applying w to ' + str(id))
				if id not in selected_list:
					continue
				# prepare data
				df_nega_target = df_nega[df_nega['vec_id_short'] == id]
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
				print(wx_list)

				# sort by wx values
				df_result_sorted = pd.DataFrame(wx_list, columns=['p_or_n', 'wx']).sort_values('wx', ascending=True)
				print(df_result_sorted)

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