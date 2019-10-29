# ----------------------------------------------------------
# this code is for finding common range of
# possible w from all the pairs
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
range_calculated = '/Users/tkimura/Desktop/RNP/svm/w_range.csv'
max_w_angles = '/Users/tkimura/Desktop/RNP/svm/w_max.csv'
min_w_angles = '/Users/tkimura/Desktop/RNP/svm/w_min.csv'

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------


def str_to_list(string):
	new_list = string.replace('\n', '').replace(']', '').replace('[', '').replace('', '').split(',')
	return new_list


# ----------------------------------------------------------
# main
# ----------------------------------------------------------
with open(range_calculated) as f:
	start = 0
	max_list, min_list = [], []
	for lines in f.readlines():
		if start == 0:
			if '_' in lines:
				start = 1
		elif start == 1:
			if '_' not in lines:
				max_list.append(str_to_list(lines))
				start = 2
		elif start == 2:
			if '_' not in lines:
				min_list.append(str_to_list(lines))
				start = 0

	df_max = pd.DataFrame(max_list)
	df_min = pd.DataFrame(min_list)

	# plt.figure()
	# df_max.astype(float).plot()
	# plt.show()

	df_max.to_csv(max_w_angles)
	df_min.to_csv(min_w_angles)

