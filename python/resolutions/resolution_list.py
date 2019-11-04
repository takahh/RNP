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
path = '/Users/tkimura/Desktop/RNP/resolutions/'
em_pdb = path + 'em_pdb.csv'
em_cif = path + 'em_cif.csv'
xray_pdb = path + 'xray_pdb.csv'
xray_cif = path + 'xray_cif.csv'
file_list = [em_pdb, em_cif, xray_pdb, xray_cif]

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
def resolution_list(limit_reso):
	for file in file_list:
		df = pd.read_csv(file, header=None)
		if file == em_pdb:
			pass
		else:
			df = pd.concat([df, last_df])
		last_df = df
	last_df.columns = ['id', 'resolution']
	last_df.set_index('id', inplace=True)

	def filter_by_reso(x):
		try:
			if float(x) < limit_reso:
				return float(x)
			else:
				return None
		except ValueError:
			return None

	selected_df = last_df['resolution'].apply(filter_by_reso).dropna()

	return selected_df