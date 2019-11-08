# ----------------------------------------------------------
# this code is for searching best angles from the results
# of ranges of angles
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
from python.resolutions.resolution_list import resolution_list as reso

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
angles_max = '/Users/tkimura/Desktop/RNP/svm/w_range_max.csv'
angles_min = '/Users/tkimura/Desktop/RNP/svm/w_range_min.csv'
output = '/Users/tkimura/Desktop/RNP/svm/best_w.csv'
svm = '/Users/tkimura/Desktop/RNP/svm/svm_out_normed.csv'
path = '/Users/tkimura/Desktop/RNP/svm/angle_range_fig/'
limit_reso = 2.5

df_svm = pd.read_csv(svm)
all_list = df_svm['chain'].values.tolist()

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------

angle_set_list = []

# make a list for vec_id limited by resolution
reso_id_list = reso(limit_reso).index.to_list()
print(reso_id_list)
# conncatenate max data
df_max = pd.read_csv('/Users/tkimura/Desktop/RNP/svm/w_range_max_0.csv')
for i in range(6):
	df_toadd = pd.read_csv('/Users/tkimura/Desktop/RNP/svm/w_range_max_' + str(i+1) + '.csv')
	df_max = pd.concat([df_max, df_toadd])
df_max.reset_index(inplace=True)
df_max2 = df_max[df_max.id.str[0:4].isin(reso_id_list)]

# conncatenate min data
df_min = pd.read_csv('/Users/tkimura/Desktop/RNP/svm/w_range_min_0.csv')
for i in range(6):
	df_toadd = pd.read_csv('/Users/tkimura/Desktop/RNP/svm/w_range_min_' + str(i+1) + '.csv')
	df_min = pd.concat([df_min, df_toadd])
df_min.reset_index(inplace=True)
df_min2 = df_min[df_min['id'].str[0:4].isin(reso_id_list)]
x = list(range(0, 80))
labels = df_max2['id'].tolist()

for i in range(80):
	fig = plt.figure()
	plt.scatter(df_max2['id'], df_max2[str(i)])
	plt.scatter(df_min2['id'], df_min2[str(i)])
	plt.axis([0, 80, 0, 6.4])
	plt.xticks(x, labels, rotation=90, size=4)
	plt.grid(True)
	plt.savefig(path + str(i) + '.png', dpi=400)
	plt.close()
	print(i)