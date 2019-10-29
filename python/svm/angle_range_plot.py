# ----------------------------------------------------------
# this code is for searching best angles from the results
# of ranges of angles
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
angles_max = '/Users/tkimura/Desktop/RNP/svm/w_range_max.csv'
angles_min = '/Users/tkimura/Desktop/RNP/svm/w_range_min.csv'
output = '/Users/tkimura/Desktop/RNP/svm/best_w.csv'
svm = '/Users/tkimura/Desktop/RNP/svm/svm_out_normed.csv'

df_svm = pd.read_csv(svm)
all_list = df_svm['chain'].values.tolist()

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------

angle_set_list = []

# conncatenate max data
df_max = pd.read_csv('/Users/tkimura/Desktop/RNP/svm/w_range_max_0.csv')
for i in range(6):
	df_toadd = pd.read_csv('/Users/tkimura/Desktop/RNP/svm/w_range_max_' + str(i+1) + '.csv')
	df_max = pd.concat([df_max, df_toadd])
df_max.reset_index(inplace=True)

# conncatenate min data
df_min = pd.read_csv('/Users/tkimura/Desktop/RNP/svm/w_range_min_0.csv')
for i in range(6):
	df_toadd = pd.read_csv('/Users/tkimura/Desktop/RNP/svm/w_range_min_' + str(i+1) + '.csv')
	df_min = pd.concat([df_min, df_toadd])
df_min.reset_index(inplace=True)

print(df_max)
plt.figure()
plt.plot(df_max['1'])
plt.plot(df_min['1'])
plt.show()