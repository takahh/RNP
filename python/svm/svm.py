# ----------------------------------------------------------
# this code is for testing SVM for selected good data
#
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import pandas as pd
import sklearn.svm as svm
import numpy as np
import warnings

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
non_natives = "/Users/tkimura/Desktop/RNP/zdock/vectors.csv"
natives = "/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt"
EM_reso = "/Users/tkimura/Desktop/RNP/filterEM/reso_summary.csv"
fig_path = "/Users/tkimura/Desktop/RNP/svm/svm_test.png"
out_file = "/Users/tkimura/Desktop/RNP/svm/svm_out.csv"
column_list = ['ALA_A', 'ALA_C', 'ALA_G', 'ALA_U', 'ARG_A', 'ARG_C',
			   'ARG_G', 'ARG_U', 'ASN_A', 'ASN_C', 'ASN_G', 'ASN_U', 'ASP_A', 'ASP_C',
			   'ASP_G', 'ASP_U', 'CYS_A', 'CYS_C', 'CYS_G', 'CYS_U', 'GLU_A', 'GLU_C',
			   'GLU_G', 'GLU_U', 'GLN_A', 'GLN_C', 'GLN_G', 'GLN_U', 'GLY_A', 'GLY_C',
			   'GLY_G', 'GLY_U', 'HIS_A', 'HIS_C', 'HIS_G', 'HIS_U', 'ILE_A', 'ILE_C',
			   'ILE_G', 'ILE_U', 'LEU_A', 'LEU_C', 'LEU_G', 'LEU_U', 'LYS_A', 'LYS_C',
			   'LYS_G', 'LYS_U', 'MET_A', 'MET_C', 'MET_G', 'MET_U', 'PHE_A', 'PHE_C',
			   'PHE_G', 'PHE_U', 'PRO_A', 'PRO_C', 'PRO_G', 'PRO_U', 'SER_A', 'SER_C',
			   'SER_G', 'SER_U', 'THR_A', 'THR_C', 'THR_G', 'THR_U', 'TRP_A', 'TRP_C',
			   'TRP_G', 'TRP_U', 'TYR_A', 'TYR_C', 'TYR_G', 'TYR_U', 'VAL_A', 'VAL_C',
			   'VAL_G', 'VAL_U', ]

# ----------------------------------------------------------
# preprocess
# add necessary columns to dataframes, make some lists
# ----------------------------------------------------------
df_nega = pd.read_csv(non_natives) # includes pose number '1abc_100_A_B'
df_nega["pdbid"] = df_nega.apply(lambda row: row.vec_id.split('_')[0] + '_' + row.vec_id.split('_')[2] + '_' + row.vec_id.split('_')[3], axis=1)
nega_pdbid_list = df_nega['pdbid'].unique()
df_posi = pd.read_csv(natives)
df_posi["pdbid"] = df_posi.apply(lambda row: row.vec_id[0:4], axis=1)
df_EMreso = pd.read_csv(EM_reso, header=None)
df_tmp = df_EMreso[df_EMreso[1] != ' .']
df_tmp['reso'] = df_tmp[1].astype(float)
df_lt35 = df_tmp[df_tmp['reso'] <= 3.5]
good_EM_list = df_lt35[0].to_list()
posi_pdbid_list = df_posi["vec_id"].unique()
run_list = []

for id in nega_pdbid_list:
	if id[0:4] in good_EM_list:
		if id in posi_pdbid_list:
			run_list.append(id)

with open(out_file, 'w') as fo:
	fo.writelines(f'chain,posi_count,native_exist,c_value,iter,w_vec\n')

	# ----------------------------------------------------------
	# main
	# good_EM_list : a list of EM with resolution <= 3.5
	# df_posi, df_nega : vectors in df
	# ----------------------------------------------------------
	for id in run_list:
		print(f'running {id}...')
		chain = id
		id = id[0:4]
		posi_1_df = df_posi[df_posi['vec_id'] == chain][column_list]
		posi_array = posi_1_df.values
		nega_1_df = df_nega[df_nega['pdbid'] == chain][column_list]
		nega_array = nega_1_df.values

		# remove a vector that's same as the positive if any
		new_list = []
		for array in nega_array.to_list():
			if np.array_equal(posi_array, array):
				continue
			else:
				new_list.append(array)
		posi_array = array(new_list)

		data_array = np.concatenate((posi_array, nega_array), axis=0)
		labels = [0] * (len(nega_array) + 1)
		labels[0] = 1
		c_value = 0.0001
		rate = 10
		last_posi_count = 10000
		converged = 0

		############################
		# run SVM until convergence
		############################
		for i in range(0, 30):
			with warnings.catch_warnings():
				warnings.simplefilter('ignore')
				lin_clf = svm.LinearSVC(C=c_value, class_weight='balanced')
				lin_clf.fit(data_array, labels)
				dec = lin_clf.decision_function(data_array)

				native_exist = lin_clf.predict(data_array)[0]
				posi_count = 0
				scores = lin_clf.predict(data_array)
				for score in scores:
					if score > 0:
						posi_count += 1

				w_vec = lin_clf.coef_
				bias = lin_clf.intercept_

				########################################################
				#  exit when converged
				########################################################
				if posi_count == 1 and native_exist == 1:
					converged = 1
					print('normally converged')
					fo.writelines(f"{chain},{posi_count},{native_exist},{c_value},{i + 1},{str(w_vec.tolist()).strip('[').strip(']')},{bias}\n")
					break
				else:
					print(f'itr: {i}, posi:{posi_count}, c_value:{c_value}, native:{native_exist}')

				########################################################
				#  remember values to use later
				########################################################
				if posi_count > 1 and posi_count < last_posi_count:
					two_last_posi_count = posi_count
					two_last_c_value = c_value
					last_c_value = c_value
					two_last_w_vec = w_vec

				########################################################
				#  change mode to update c_value depending on the state
				########################################################

				# A normal update
				if (last_posi_count > 1 and posi_count > 1 and last_posi_count > posi_count)\
					or (last_posi_count == 1 and last_native_exist == 0 and posi_count > 1 and posi_count < two_last_posi_count)\
					or (last_posi_count == 0 and posi_count > 1 and posi_count < two_last_posi_count):
					c_value = c_value * rate
				# B
				elif (last_posi_count > 1 and posi_count > 1 and last_posi_count <= posi_count)\
					or (last_posi_count > 1 and native_exist == 0 and posi_count == 1)\
					or (last_posi_count > 1 and posi_count == 0):
					c_value = (last_c_value + c_value) / 2
				# C
				elif (last_posi_count == 0 and posi_count == 0)\
					or (last_posi_count == 0 and posi_count == 1 and native_exist == 0)\
					or (last_posi_count == 1 and last_native_exist == 0 and posi_count == 1 and native_exist == 0)\
					or (last_posi_count == 1 and last_native_exist == 0 and posi_count == 0)\
					or (last_posi_count == 1 and last_native_exist == 0 and posi_count > 1 and posi_count >= two_last_posi_count)\
					or (last_posi_count == 0 and posi_count > 1 and posi_count >= two_last_posi_count):
					c_value = (two_last_c_value + c_value) / 2

				last_posi_count = posi_count
				last_native_exist = native_exist

				# remember best values in case of no convergence
				if native_exist == 1 and posi_count > 0:
					best_posi_count = posi_count
					best_native_exist = native_exist
					best_c_value = c_value
					best_w_vec = w_vec

		if converged == 0:
			print('not converged')
			fo.writelines(f"{chain},{best_posi_count},{best_native_exist},{best_c_value},{i + 1},{str(w_vec.tolist()).strip('[').strip(']')},{bias}\n")