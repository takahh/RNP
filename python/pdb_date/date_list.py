# ----------------------------------------------------------
# this code returns  a list of id and resolution
#
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import pandas as pd

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
path = '/Users/tkimura/Desktop/RNP/pdb_date/'
xray_pdb = path + 'xray_pdb.csv'
xray_cif = path + 'xray_cif.csv'

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
def date_list(limit_year):
	df1 = pd.read_csv(xray_pdb, header=None)
	df2 = pd.read_csv(xray_cif, header=None)
	df = pd.concat([df1, df2])
	df.columns = ['id', 'year']
	# df.set_index('id', inplace=True)
	df.to_csv(path + 'year_list.csv')

	def filter_by_year(x):
		try:
			if int(x) <= limit_year:
				return float(x)
			else:
				return None
		except ValueError:
			return None

	selected_df = df['year'].apply(filter_by_year).dropna()

	return selected_df

date_list(2020)