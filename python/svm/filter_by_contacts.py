# ----------------------------------------------------------
# this code is for a function that provides
# a list of chain pair ids that have a range of contacts ratio
# ----------------------------------------------------------

def filter_by_contacts(contacts_ratio):
	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------
	import pandas as pd

	# ----------------------------------------------------------
	# constants
	# ----------------------------------------------------------
	file = '/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt'

	# ----------------------------------------------------------
	# functions
	# ----------------------------------------------------------

	# ----------------------------------------------------------
	# main
	# ----------------------------------------------------------
	df = pd.read_csv(file)
	id_list = df[df['all_chains'].astype(float) < contacts_ratio]['vec_id'].tolist()
	return id_list