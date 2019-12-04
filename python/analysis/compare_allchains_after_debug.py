# ----------------------------------------------------------
# this code is for comparing the ids of pre-debug and
# post-debug and see if I need to run zdock more
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
source = '/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt'
out = '/Users/tkimura/Desktop/RNP/check_contact/pdbid_hfrac_ltoeq_2.csv'

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------

df = pd.read_csv(source)
df_2 = df[df['all_chains'] <= 2]
# df_2 = df_tmp[df_tmp['all_chains'] >= 0.5]
plt.hist(df['all_chains'], bins=200, range=(0, 200))
plt.show()
plt.close()

print(len(df_2))
gap_list = []

new_id_list = df_2['vec_id'].tolist()
idlist = ["2von_A_C","2y9h_O_P","1qa6_A_C","1hc8_B_D","6nut_A_D","6nme_A_G","5a7a_A_R","2go5_6_9","2om3_A_R","3j46_5_4","6i2n_D_U","5xwy_A_B","5mq0_V_3","3j0l_F_5","5y88_W_x","3iz4_B_A","4uft_B_R","6e9e_A_B","2xea_A_R","3izz_F_D","3j0q_k_9","5fn1_A_B","3izy_P_N","6iv6_A_G","3j0d_G_A","4ue4_C_A","2xkv_C_B","3j06_A_R","3iyq_B_A","4udv_A_R","3iyr_B_A","5z9w_A_R","4d5n_A_X","6h5q_B_R","6h5s_C_E","1mj1_A_D","5a79_A_R"]
print(len(new_id_list))

with open(out, 'w') as f:
	for item in new_id_list:
		f.writelines(item)
		if item != new_id_list[-1]:
			f.writelines(',')
