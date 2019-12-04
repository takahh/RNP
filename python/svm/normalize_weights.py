# ----------------------------------------------------------
# this code is for normalizing the output from SVM
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
svm_solution = "/Users/tkimura/Desktop/RNP/svm/svm_out.csv"
svm_norm = "/Users/tkimura/Desktop/t3_mnt/zdock/python/polar_range_mpi/data_from_laptop/svm_out_normed.csv"

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

# "ALA_A_sc", "ALA_C_sc", "ALA_G_sc", "ALA_U_sc", "ARG_A_sc", "ARG_C_sc", "ARG_G_sc", "ARG_U_sc", "ASN_A_sc", "ASN_C_sc", "ASN_G_sc", "ASN_U_sc", "ASP_A_sc", "ASP_C_sc", "ASP_G_sc", "ASP_U_sc", "CYS_A_sc", "CYS_C_sc", "CYS_G_sc", "CYS_U_sc", "GLU_A_sc", "GLU_C_sc", "GLU_G_sc", "GLU_U_sc", "GLN_A_sc", "GLN_C_sc", "GLN_G_sc", "GLN_U_sc", "GLY_A_sc", "GLY_C_sc", "GLY_G_sc", "GLY_U_sc", "HIS_A_sc", "HIS_C_sc", "HIS_G_sc", "HIS_U_sc", "ILE_A_sc", "ILE_C_sc", "ILE_G_sc", "ILE_U_sc", "LEU_A_sc", "LEU_C_sc", "LEU_G_sc", "LEU_U_sc", "LYS_A_sc", "LYS_C_sc", "LYS_G_sc", "LYS_U_sc", "MET_A_sc", "MET_C_sc", "MET_G_sc", "MET_U_sc", "PHE_A_sc", "PHE_C_sc", "PHE_G_sc", "PHE_U_sc", "PRO_A_sc", "PRO_C_sc", "PRO_G_sc", "PRO_U_sc", "SER_A_sc", "SER_C_sc", "SER_G_sc", "SER_U_sc", "THR_A_sc", "THR_C_sc", "THR_G_sc", "THR_U_sc", "TRP_A_sc", "TRP_C_sc", "TRP_G_sc", "TRP_U_sc", "TYR_A_sc", "TYR_C_sc", "TYR_G_sc", "TYR_U_sc", "VAL_A_sc", "VAL_C_sc", "VAL_G_sc", "VAL_U_sc", "all_chains", "ALA_A_bb", "ALA_C_bb", "ALA_G_bb", "ALA_U_bb", "ARG_A_bb", "ARG_C_bb", "ARG_G_bb", "ARG_U_bb", "ASN_A_bb", "ASN_C_bb", "ASN_G_bb", "ASN_U_bb", "ASP_A_bb", "ASP_C_bb", "ASP_G_bb", "ASP_U_bb", "CYS_A_bb", "CYS_C_bb", "CYS_G_bb", "CYS_U_bb", "GLU_A_bb", "GLU_C_bb", "GLU_G_bb", "GLU_U_bb", "GLN_A_bb", "GLN_C_bb", "GLN_G_bb", "GLN_U_bb", "GLY_A_bb", "GLY_C_bb", "GLY_G_bb", "GLY_U_bb", "HIS_A_bb", "HIS_C_bb", "HIS_G_bb", "HIS_U_bb", "ILE_A_bb", "ILE_C_bb", "ILE_G_bb", "ILE_U_bb", "LEU_A_bb", "LEU_C_bb", "LEU_G_bb", "LEU_U_bb", "LYS_A_bb", "LYS_C_bb", "LYS_G_bb", "LYS_U_bb", "MET_A_bb", "MET_C_bb", "MET_G_bb", "MET_U_bb", "PHE_A_bb", "PHE_C_bb", "PHE_G_bb", "PHE_U_bb", "PRO_A_bb", "PRO_C_bb", "PRO_G_bb", "PRO_U_bb", "SER_A_bb", "SER_C_bb", "SER_G_bb", "SER_U_bb", "THR_A_bb", "THR_C_bb", "THR_G_bb", "THR_U_bb", "TRP_A_bb", "TRP_C_bb", "TRP_G_bb", "TRP_U_bb", "TYR_A_bb", "TYR_C_bb", "TYR_G_bb", "TYR_U_bb", "VAL_A_bb", "VAL_C_bb", "VAL_G_bb", "VAL_U_bb"]


skipcolumns = ['posi_count', 'native_exist', 'iter']
# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
df = pd.read_csv(svm_solution)
with open(svm_norm, 'w') as fo:
	with open(svm_solution) as f:
		for lines in f.readlines():
			if 'ALA' in lines:
				fo.writelines(lines)
				continue

			# calculate norm to normalize
			# chain,posi_count,native_exist,c_value,norm,iter,ALA_A,
			ele = lines.split(',')
			normsq = 0
			for weight in ele[5:85]:
				normsq += float(weight)**2.0
			norm = normsq**0.5

			# normalize and make a new file
			for idx, val in enumerate(ele):
				if idx >= 5 and idx != 85:
					val = val.replace('[', '').replace(']', '').replace('\n', '')
					fo.writelines(str(float(val)/norm) + ',')
				elif idx == 85:
					fo.writelines(val)
				else:
					fo.writelines(val + ',')