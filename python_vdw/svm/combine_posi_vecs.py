# ----------------------------------------------------------
# this code is for combining posi vectors
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
hb_posi = '/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt'
vdw_posi = '/Users/tkimura/Desktop/RNP/check_contact/vdw_non_redun_positives.txt'
combined_posi = '/Users/tkimura/Desktop/t3_mnt/zdock/python_vdw/polar_range_mpi/data_from_laptop/non_redun_positives_hb_vdw.txt'

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
df_hb = pd.read_csv(hb_posi)
print(df_hb.columns)
new_columns = []
for item in df_hb.columns:
       if item == 'vec_id' or item == 'exp' or item == 'all_chains':
              new_columns.append(item)
       else:
              new_columns.append(f'{item}_hb')
df_hb.columns = new_columns
df_vdw = pd.read_csv(vdw_posi)
df_hb = df_hb[df_hb.columns[:-1]]
df_merged = df_hb.merge(df_vdw, left_on=['vec_id'], right_on=['vec_id'], how='inner', suffixes=('', '_vdw'))
df_merged.drop(labels='exp_vdw', axis=1, inplace=True)
df_merged.to_csv(combined_posi)