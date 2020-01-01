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
	path = '/Users/tkimura/Desktop/RNP/svm/'
	infile = path + 'ranking_results_mean_reso_' + str(reso_limit) + '_touch_' + str(contact_limit) + '.csv'
	df_svm = pd.read_csv(infile)
	outfile = path + 'indi_common_plot_reso_' + str(reso_limit) + '_touch_' + str(contact_limit) + '.png'
	df_its_raw = pd.read_csv('/Users/tkimura/Desktop/t3_mnt/zdock/itscorepr/rankings.csv')
	df_svm = pd.merge(df_svm, df_its_raw, left_on='id', right_on='id', how='left')
	print('######')
	print(df_svm[' its_rank'].mean())
	print(df_svm[' rank'].mean())
	print(df_svm[' svm_rank'].mean())
	# ----------------------------------------------------------
	# main
	# ----------------------------------------------------------
	angle_set_list = []
	x = list(range(0, len(df_svm)))

	plt.figure()
	plt.gca().invert_yaxis()
	x = df_svm[' svm_rank'].index
	y = df_svm[' svm_rank'].values
	plt.scatter(x, y, s=9)
	x = df_svm[' rank'].index
	y = df_svm[' rank'].values
	plt.scatter(x, y, s=9)

	# insert itscore here
	x = df_svm[' its_rank'].index
	y = df_svm[' its_rank']
	plt.scatter(x, y, s=9)

	# plt.scatter(df_svm[' svm_rank'])
	print(df_svm.columns)
	plt.ylabel('rank')
	plt.xlabel('pair')
	plt.title(f'resolution: {reso_limit}, contact: {contact_limit}')
	plt.gca().legend(('individual', 'common', 'itscorepr'))
	plt.text(0, -140, 'average: ' + str(round(df_svm[' rank'].mean(), 3)))
	plt.text(0, 140, 'average: ' + str(round(df_svm[' its_rank'].mean(), 3)))
	plt.savefig(outfile)
	plt.show()