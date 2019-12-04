def get_anisous():
	import pandas as pd
	anisous = '/Users/tkimura/Desktop/RNP/check_contact/anisou_list_xray.csv'
	# make anisou_list
	df = pd.read_csv(anisous, header=None)
	anisou_list = df[0].tolist()
	return anisou_list

