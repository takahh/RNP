# ----------------------------------------------------------
# this code is for searching best angles from the results
# of ranges of angles
# ----------------------------------------------------------

def indi_common_plot(reso_limit, contact_limit):
	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------
	import pandas as pd
	import matplotlib.pyplot as plt

	# ----------------------------------------------------------
	# constants
	# ----------------------------------------------------------
	path =  '/Users/tkimura/Desktop/RNP/svm/'
	infile = path + 'ranking_results_mean.csv'
	df_svm = pd.read_csv(infile)
	outfile = path + 'indi_common_plot_reso_' + str(reso_limit) + '_touch_' + str(contact_limit) + '.png'

	# ----------------------------------------------------------
	# main
	# ----------------------------------------------------------
	angle_set_list = []
	x = list(range(0, 80))

	plt.figure()
	plt.gca().invert_yaxis()
	x = df_svm[' svm_rank'].index
	y = df_svm[' svm_rank'].values
	plt.scatter(x, y, s=9)
	x= df_svm[' rank'].index
	y = df_svm[' rank'].values
	plt.scatter(x, y, s=9)
	# plt.scatter(df_svm[' svm_rank'])
	plt.ylabel('rank')
	plt.xlabel('pair')
	plt.gca().legend(('individual', 'common'))
	plt.text(-10, -240, 'average: ' + str(df_svm[' rank'].values.mean()))
	plt.savefig(outfile)
	plt.show()