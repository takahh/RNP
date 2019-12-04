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
from python.svm.filter_by_contacts import filter_by_contacts

# ----------------------------------------------------------
# constants changeable
# ----------------------------------------------------------
limit_reso = 2.5
allchains = 2.0
# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
output = '/Users/tkimura/Desktop/RNP/svm/best_w.csv'
svm = '/Users/tkimura/Desktop/RNP/svm/svm_out_normed.csv'
path = '/Users/tkimura/Desktop/RNP/svm/angle_range_fig/'
rpath = '/Users/tkimura/Desktop/t3_mnt/zdock/python/polar_range_mpi/data_from_laptop/outs/'
# ----------------------------------------------------------
# preprocess
# ----------------------------------------------------------
df_svm = pd.read_csv(svm)
all_list = [x[0:4] for x in df_svm['chain'].values.tolist()]
angle_set_list = []
reso_id_list = reso(limit_reso).index.to_list()
allchainlist = [x[0:4] for x in filter_by_contacts(allchains)]
run_list = []
for item in all_list:
	if item in reso_id_list and item in allchainlist:
		run_list.append(item)
length = len(run_list)

# ----------------------------------------------------------
# main
# ----------------------------------------------------------

# conncatenate max data
df_max = pd.read_csv(rpath + 'w_range_max_0.csv')
for i in range(27):
	df_toadd = pd.read_csv(rpath + 'w_range_max_' + str(i+1) + '.csv')
	df_max = pd.concat([df_max, df_toadd])
df_max.reset_index(inplace=True)
df_max2 = df_max[df_max.id.str[0:4].isin(run_list)]

# conncatenate min data
df_min = pd.read_csv(rpath + 'w_range_min_0.csv')
for i in range(27):
	df_toadd = pd.read_csv(rpath + 'w_range_min_' + str(i+1) + '.csv')
	df_min = pd.concat([df_min, df_toadd])
df_min.reset_index(inplace=True)
df_min2 = df_min[df_min['id'].str[0:4].isin(run_list)]
x = list(range(0, length))
labels = df_max2['id'].tolist()

# get best range (max, min, and avg)
best_w = '/Users/tkimura/Desktop/RNP/svm/best_w.csv'
bestw_df = pd.read_csv(best_w)
print(bestw_df.columns)

for i in range(79):
	fig = plt.figure()
	plt.scatter(df_max2['id'], df_max2[str(i)], s=1, marker='1')
	plt.scatter(df_min2['id'], df_min2[str(i)], s=1)
	plt.axis([0, length, 0, 6.4])
	plt.xticks(x, labels, rotation=90, size=2)
	# add horizontal lines for solutions
	print(bestw_df.iloc[i][' average'])
	plt.axhline(y=bestw_df.iloc[i][' average'], color='k', linewidth=0.5, linestyle=':')
	plt.axhline(y=bestw_df.iloc[i][' min_angle'], color='r', linewidth=0.3, linestyle=':')
	plt.axhline(y=bestw_df.iloc[i][' max_angle'], color='r', linewidth=0.3, linestyle=':')
	# plt.grid(True)
	plt.savefig(path + str(i) + '.png', dpi=400)
	plt.close()
	print(i)