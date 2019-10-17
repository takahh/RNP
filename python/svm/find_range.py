# ----------------------------------------------------------
# this code is for finding a range of possible hyperplanes
# with keeping the number of positive pose/native
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
negatives = "/Users/tkimura/Desktop/RNP/zdock/vectors.csv"
positive = "/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt"
svm_solution = "/Users/tkimura/Desktop/RNP/svm/svm_out_normed.csv"
svm_summary = "/Users/tkimura/Desktop/RNP/svm/svm_summary.csv"
summary_fig = "/Users/tkimura/Desktop/RNP/svm/summary_fig.png"
columnnames = ['chain', 'posi_count', 'native_exist', 'c_value', 'iter',
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
skipcolumns = ['posi_count', 'native_exist', 'iter']
# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
df = pd.read_csv(svm_solution)
with open(svm_summary, 'w') as f:
	f.writelines(f'column,mean,sd,median\n')
	for column in df.columns:
		if column == 'chain' or column == 'bias' or column == 'c_value':
			continue
		if column in skipcolumns:
			continue
		f.writelines(f'{column},{df[column].mean()},{df[column].std()},{df[column].median()}\n')

dfs = pd.read_csv(svm_summary)
plt.figure()
dfs.plot()
plt.legend(fontsize=8)
plt.xticks(np.arange(0,80,step=1),labels=dfs['column'], rotation='vertical', fontsize=5)
plt.savefig(summary_fig, dpi=400, bbox_inches='tight')
plt.show()