# ----------------------------------------------------------
# this code is for combining vdw and hb vectors
#
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import pandas as pd
import os

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
vdw = '/Users/tkimura/Desktop/t3_mnt/zdock/vectors_vdw/'
hb = '/Users/tkimura/Desktop/t3_mnt/zdock/vectors/'
out = '/Users/tkimura/Desktop/t3_mnt/zdock/vectors_hb_vdw/'
columns = ['vec_id', 'exp', 'ALA_A', 'ALA_C', 'ALA_G', 'ALA_U', 'ARG_A', 'ARG_C',
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

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
k = 0
for hbfile in os.listdir(hb):
	if hbfile in os.listdir(vdw):
		if hbfile[0] == '.':
			continue
		if os.path.exists(out + hbfile):
			continue
		df_hb = pd.read_csv(hb + hbfile)
		if 'vec_id' not in df_hb.columns:
			try:
				df_hb.columns = columns
			except ValueError as e:
				print(e)
				print(hbfile)
				continue
		df_vdw = pd.read_csv(vdw + hbfile, names=df_hb.columns)
		df_hb = df_hb[df_hb.columns[:-1]]
		try:
			df_vdw.drop(labels='exp', axis=1, inplace=True)
		except KeyError:
			print(hbfile)
		# df_vdw = df_vdw[df_vdw.columns[2:]]
		# print(df_vdw)
		# print(df_hb)
		try:
			df_merged = df_hb.merge(df_vdw, left_on=['vec_id'], right_on=['vec_id'], how='inner', suffixes=('_hb', '_vdw'))
		except KeyError:
			print(df_hb.columns)
			print(df_vdw.columns)
		df_merged.to_csv(out + hbfile)