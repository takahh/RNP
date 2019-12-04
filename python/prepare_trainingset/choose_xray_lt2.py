# ----------------------------------------------------------
# this code is for making a list of id
# after choosing only xray
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import pandas as pd

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
path = '/Users/tkimura/Desktop/t3_mnt/zdock/'
lt_2_xray_file = path + 'pdbid_hfrac_ltoeq_2.csv'
lt_2_file = path + 'pdbid_hfrac_ltoeq_2_tmp.csv'
xray_file = path + 'xray_chain_summary_calculated.csv'

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------

df = pd.read_csv('/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt')
df_tmp = df[df['exp'] == 'xray']
print(df_tmp.columns)
xray_lt2_list = df_tmp[df_tmp['all_chains'].astype(float) <= 2.0]['vec_id'].tolist()
print(xray_lt2_list)
print(len(xray_lt2_list))


# with open(lt_2_file) as f:
# 	for lines in f.readlines():
# 		alllist = lines.replace('\ufeff','').split(',')
# 		break
# print(len(alllist))

with open(lt_2_xray_file) as f:
	for lines in f.readlines():
		alllist2 = lines.replace('\ufeff','').split(',')
		break
print(len(alllist2))