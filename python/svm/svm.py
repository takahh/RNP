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

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
non_natives = "/Users/tkimura/Desktop/RNP/zdock/vectors.csv"
natives = "/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt"
EM_reso = "/Users/tkimura/Desktop/RNP/filterEM/reso_summary.csv"
fig_path = "/Users/tkimura/Desktop/RNP/svm/svm_test.png"
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
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------

# preprocess : add 'pdbid' column to each dataframe
df_nega = pd.read_csv(non_natives)
df_nega["pdbid"] = df_nega.apply(lambda row: row.vec_id[0:4], axis=1)
df_nega["chpair"] = df_nega.apply(lambda row: row.vec_id[-3:], axis=1)

nega_pdbid_list = df_nega['pdbid'].unique()

df_posi = pd.read_csv(natives)
df_posi["pdbid"] = df_posi.apply(lambda row: row.vec_id[0:4], axis=1)
df_posi["chpair"] = df_posi.apply(lambda row: row.vec_id.replace(row.vec_id[0:4], ''), axis=1)

df_EMreso = pd.read_csv(EM_reso, header=None)

df_tmp = df_EMreso[df_EMreso[1] != ' .']
df_tmp['reso'] = df_tmp[1].astype(float)
df_lt35 = df_tmp[df_tmp['reso'] <= 3.5]

good_EM_list = df_lt35[0].to_list()

# make the run list ## need to increase the final list??

posi_pdbid_list = df_posi["pdbid"].unique()
run_list = []

for id in nega_pdbid_list:
	if id in good_EM_list and id in posi_pdbid_list:
		run_list.append(id)

### RUN SVM
# good_EM_list : a list of EM with resolution <= 3.5
# df_posi, df_nega : vectors in df

for id in run_list:
	print(f'running {id} ....')
	posi_1_df = df_posi[df_posi['pdbid'] == id and df_posi['pdbid'] == id][column_list]
	posi_array = posi_1_df.values

	nega_1_df = df_nega[df_nega['pdbid'] == id][column_list]
	nega_array = nega_1_df.values

	print(type(nega_array))
	print(type(posi_array))

	data_array = np.concatenate((posi_array, nega_array), axis=0)
	print(f'{len(posi_array)} positives')
	print(f'{len(nega_array)} negatives')
	print(f'{len(data_array)} vectors')
	labels = [0] * (len(nega_array) + 1)
	labels[0] = 1
	print(f'{len(labels)} labels')

	## SVM
	lin_clf = svm.LinearSVC()
	lin_clf.fit(data_array, labels)
	dec = lin_clf.decision_function(data_array)

	# index of predicted positive data
	print(lin_clf.predict(data_array).nonzero())

	# scores
	scores = lin_clf.decision_function(data_array)
	for score in scores:
		if score > 0:
			print(score)

	# weight vectors?
	print(lin_clf.coef_)

	# length of w
	print(len(lin_clf.coef_[0]))
