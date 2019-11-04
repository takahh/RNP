# %%

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
posi_path = '/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt'
# posi_path = '/Users/tkimura/Desktop/RNP/check_contact/filtered_xray_positives.txt'
posi_path_selected = '/Users/tkimura/Desktop/RNP/check_contact/selected_positives.txt'
neg_path = '/Users/tkimura/Desktop/RNP/zdock/vectors.csv'
path = '/Users/tkimura/Desktop/RNP/check_contact/nega_posi_all_vectors.txt'
# path = '/Users/tkimura/Desktop/RNP/check_contact/filtered_xray_positives.txt'
# figpath =  '/Users/tkimura/Desktop/RNP/check_contact/UMAP/positives_filtered_xray.png'
figpath = '/Users/tkimura/Desktop/RNP/check_contact/UMAP/all.png'
limit_reso = 2.5

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
from scipy.sparse.csgraph import connected_components
import umap, numpy as np
from sklearn.datasets import load_digits
from scipy.sparse.csgraph import connected_components
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.manifold import TSNE
import numba
from numba import njit
from python.resolutions.resolution_list import resolution_list as reso

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
uscls = tuple(range(2, 82))
# print(uscls)

# make a list for vec_id limited by resolution
reso_id_list = reso(limit_reso).index.to_list()

# filter positive vectors
with open(posi_path_selected, 'w') as fo:
	with open(posi_path) as f1:
		for lines in f1.readlines():
			if 'vec_id' in lines:
				fo.writelines(lines)
			else:
				element = lines.split(',')
				if element[0][0:4] not in reso_id_list:
					continue
				if float(element[82]) < 0.5:  # cap here !!!!
					fo.writelines(lines)

# # merge neg and posi vector files
# with open(path, 'w') as fo:
# 	with open(posi_path_selected) as f1:
# 		for lines in f1.readlines():
# 			fo.writelines(lines)
# 	with open(neg_path) as f2:
# 		for lines in f2.readlines():
# 			if 'vec_id' in lines:
# 				continue
# 			else:
# 				fo.writelines(lines)


@numba.njit()
def red_channel_dist(a, b):
	return np.abs(a[0] - b[0])


def run_UMAP(input_file):
	vec_data = np.loadtxt(input_file, delimiter=',', usecols=uscls, skiprows=1)
	reducer = umap.UMAP()
	label_data = np.loadtxt(input_file, delimiter=',', usecols=82, skiprows=1)
	pdbid_data = np.loadtxt(input_file, delimiter=',', usecols=0, skiprows=1, dtype='str')

	embedding = reducer.fit_transform(vec_data)
	fig = plt.figure()
	# plt.scatter(embedding[:, 0], embedding[:, 1], c=label_data, cmap='tab20c', s=10, alpha=0.5)
	plt.scatter(embedding[:, 0], embedding[:, 1], c=label_data, cmap='tab20c', s=0.1, alpha=0.5)
	plt.colorbar()
	for i in range(embedding.shape[0]):
		if label_data[i] == 0:
			# print('zero!!!!')
			# plt.text(embedding[i,0], embedding[i,1], str(label_data[i]).replace('.0', ''), fontsize=7)
			plt.text(embedding[i, 0], embedding[i, 1], str(pdbid_data[i]).replace('.0', ''), fontsize=7)
	fig.savefig(figpath, dpi=600)


run_UMAP(posi_path_selected)
