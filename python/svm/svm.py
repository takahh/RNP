# ----------------------------------------------------------
# this code is for testing SVM for selected good data
#
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import sys
sys.path.append("..")
sys.path.append(".")
import pandas as pd
import sklearn.svm as svm
import numpy as np
import warnings
import os
sys.path.append(".")
from subprocess import call
from resolutions.resolution_list import resolution_list

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
base_path = '/Users/tkimura/Desktop/RNP/'
remo_path = '/Users/tkimura/Desktop/t3_mnt/zdock/'
fig_path = base_path + "svm/svm_test.png"
out_file = base_path + "svm/svm_out.csv"
full_columns = ['vec_id', 'exp', 'ALA_A', 'ALA_C', 'ALA_G', 'ALA_U', 'ARG_A', 'ARG_C',
       'ARG_G', 'ARG_U', 'ASN_A', 'ASN_C', 'ASN_G', 'ASN_U', 'ASP_A', 'ASP_C',
       'ASP_G', 'ASP_U', 'CYS_A', 'CYS_C', 'CYS_G', 'CYS_U', 'GLU_A', 'GLU_C',
       'GLU_G', 'GLU_U', 'GLN_A', 'GLN_C', 'GLN_G', 'GLN_U', 'GLY_A', 'GLY_C',
       'GLY_G', 'GLY_U', 'HIS_A', 'HIS_C', 'HIS_G', 'HIS_U', 'ILE_A', 'ILE_C',
       'ILE_G', 'ILE_U', 'LEU_A', 'LEU_C', 'LEU_G', 'LEU_U', 'LYS_A', 'LYS_C',
       'LYS_G', 'LYS_U', 'MET_A', 'MET_C', 'MET_G', 'MET_U', 'PHE_A', 'PHE_C',
       'PHE_G', 'PHE_U', 'PRO_A', 'PRO_C', 'PRO_G', 'PRO_U', 'SER_A', 'SER_C',
       'SER_G', 'SER_U', 'THR_A', 'THR_C', 'THR_G', 'THR_U', 'TRP_A', 'TRP_C',
       'TRP_G', 'TRP_U', 'TYR_A', 'TYR_C', 'TYR_G', 'TYR_U', 'VAL_A', 'VAL_C',
       'VAL_G', 'VAL_U', 'all_chains']
column_list = ['ALA_A', 'ALA_C', 'ALA_G', 'ALA_U', 'ARG_A', 'ARG_C', 'ARG_G', 'ARG_U','ASN_A','ASN_C','ASN_G','ASN_U','ASP_A','ASP_C','ASP_G','ASP_U','CYS_A','CYS_C','CYS_G','CYS_U','GLU_A','GLU_C','GLU_G','GLU_U','GLN_A','GLN_C','GLN_G','GLN_U','GLY_A','GLY_C', 'GLY_G', 'GLY_U', 'HIS_A', 'HIS_C', 'HIS_G', 'HIS_U', 'ILE_A', 'ILE_C', 'ILE_G', 'ILE_U', 'LEU_A', 'LEU_C', 'LEU_G', 'LEU_U', 'LYS_A', 'LYS_C', 'LYS_G', 'LYS_U', 'MET_A', 'MET_C', 'MET_G', 'MET_U', 'PHE_A', 'PHE_C', 'PHE_G', 'PHE_U', 'PRO_A', 'PRO_C', 'PRO_G', 'PRO_U', 'SER_A', 'SER_C', 'SER_G', 'SER_U', 'THR_A', 'THR_C', 'THR_G', 'THR_U', 'TRP_A', 'TRP_C', 'TRP_G', 'TRP_U', 'TYR_A', 'TYR_C', 'TYR_G', 'TYR_U', 'VAL_A', 'VAL_C', 'VAL_G', 'VAL_U', ]
natives = base_path + "/check_contact/non_redun_positives.txt"

# ----------------------------------------------------------
# preprocess
# add necessary columns to dataframes, make some lists
# ----------------------------------------------------------
df_posi = pd.read_csv(natives)
posi_pdbid_list = df_posi["vec_id"].unique()
nega_list = [x.replace('.csv', '') for x in os.listdir(remo_path + 'vectors/')]
reso_list = resolution_list(2.5).index.tolist()

with open(out_file, 'w') as fo:
	fo.writelines(f'chain,posi_count,native_exist,c_value,iter,w_vec,{column_list}\n')
	# ----------------------------------------------------------
	# good_EM_list : a list of EM with resolution <= 3.5
	# df_posi, df_nega : vectors in df
	# ----------------------------------------------------------
	for id in nega_list:
		if id[0] == '.':
			continue
		if id in ['2wwa_I_F']:
			continue
		non_natives = remo_path + 'vectors/' + str(id) + '.csv'
		print('processing ' + str(id))
		df_nega = pd.read_csv(non_natives) # includes pose number '1abc_100_A_B'
		try:
			df_nega["vec_id_cld"] = df_nega.apply(lambda row: row.vec_id.split('_')[0] + '_' + row.vec_id.split('_')[1] + '_' + row.vec_id.split('_')[2], axis=1)
		except AttributeError:
			df_nega.columns = df_posi.columns
			df_nega["vec_id_cld"] = df_nega.apply(lambda row: row.vec_id.split('_')[0] + '_' + row.vec_id.split('_')[1] + '_' + row.vec_id.split('_')[2], axis=1)
		nega_pdbid_list = df_nega['vec_id_cld'].unique()
		chain = id
		posi_1_df = df_posi[df_posi['vec_id'] == id][column_list]
		posi_array = posi_1_df.values
		nega_1_df = df_nega[df_nega['vec_id_cld'] == id][column_list]
		if len(nega_1_df) < 3300:
			print(id + ' does not have enough vectors!!')
			continue
		else:
			print(id)
		nega_array = nega_1_df.values

		# remove a vector that's same as the positive if any
		new_list = []
		for array in nega_array.tolist():
			if np.array_equal(posi_array, array):
				continue
			else:
				new_list.append(array)
		nega_array = np.asarray(new_list)

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
