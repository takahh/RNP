# ----------------------------------------------------------
# this code is for identifying pdbid that should be
# re-run for all processes
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
from python.svm.filter_by_contacts import filter_by_contacts
from python.resolutions.resolution_list import resolution_list
import pandas as pd

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
origin = '/Users/tkimura/Desktop/RNP/check_contact/pdbid_hfrac_ltoeq_2.csv'
anisous = '/Users/tkimura/Desktop/RNP/check_contact/anisou_list_xray.csv'
anisou_rerun_list = '/Users/tkimura/Desktop/RNP/check_contact/anisou_to_rerun.csv'

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------
# make anisou_list
df = pd.read_csv(anisous, header=None)
anisou_list = df[0].tolist()
print(anisou_list)
print(len(anisou_list))

# make reso 2.5 list
df_reso = resolution_list(2.5)
reso25_list = df_reso.index.tolist()
print(reso25_list)
print(len(reso25_list))

# make allchain list
allchains_list = filter_by_contacts(2)
allchains_list_short = [x[0:4] for x in allchains_list]
print(allchains_list_short)
print(len(allchains_list_short))

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
rerun_list = []
for item in anisou_list:
	if item in reso25_list:
		if item in allchains_list_short:
			rerun_list.append(item)
print('rerun')
print(len(rerun_list))
#
# with open(anisou_rerun_list, 'w') as fo:
# 	for item in rerun_list:
# 		fo.writelines(item + '\n')
# ['1hq1', '2asb', '2xli', '2xlk', '2xnr', '2xs2', '2xs7', '2y8w', '2y8y', '2y9h', '3am1', '3k5q', '3k5y', '3k5z', '3k61', '3k62', '3k64', '3mxh', '3nmr', '3nna', '3ova', '3ovb', '3pew', '3pey', '3q0q', '3q0s', '3qg9', '3qgb', '3qgc', '3r2c', '3r9w', '3sqw', '3sqx', '3t5n', '3ts2', '3v6y', '3v74', '3zgz', '3zjt', '3zjv', '4al5', '4al7', '4aq7', '4as1', '4ato', '4bw0', '4c8y', '4c8z', '4d25', '4d26', '4ed5', '4f02', '4f3t', '4hor', '4i67', '4kre', '4krf', '4kxt', '4lgt', '4m4o', '4mdx', '4n0t', '4ngb', '4ngc', '4ohy', '4ohz', '4oi0', '4oi1', '4prf', '4qm6', '4qu6', '4qu7', '4w5o', '4w5t', '4wal', '4wan', '4yco', '4z0c', '4z4c', '4z4d', '4z4e', '4z4h', '5aor', '5bz1', '5bzu', '5bzv', '5c0y', '5det', '5dno', '5elh', '5elk', '5elr', '5f5h', '5gjb', '5guh', '5h3u', '5i4a', '5i9g', '5i9h', '5id6', '5kla', '5mfx', '5o58', '5sze', '5tf6', '5the', '5ud5', '5w0m', '5w1h', '5w1i', '5wlh', '5wzj', '5ytx', '6cmn', '6d12', '6dcl', '6dtd', '6du4', '6f4g', '6fpq', '6fpx', '6fq3', '6fql', '6gc5', '6jim', '6m7k', '6n6a', '6n6c', '6n6d', '6n6e', '6n6f', '6n6g', '6n6h', '6nof', '6noh', '6oon', '4qu6', '4qu7']