# ----------------------------------------------------------
# this code is for identifying resolutions from PDB files
#
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import os
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
path = '/Users/tkimura/Desktop/RNP/check_contact/PDBfiles/xray/'
date_summary = '/Users/tkimura/Desktop/RNP/pdb_date/xray_pdb.csv'
date_list = []

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
with open(date_summary, 'w') as fo:
	for files in os.listdir(path):
		id = ''
		year = ''
		if '.pdb' in files:
			with open(path + files) as f:
				for lines in f.readlines():
					try:
						if 'DATE OF DATA COLLECTION' in lines:
							date = lines.split(':')[1].strip() # 08-AUG-02
							print(date)
							year = int(date.split('-')[2])
							if year > 80:
								year = 1900 + year
							else:
								year = 2000 + year
							break
					except IndexError:
						print('inderror')
						print(lines)
					except ValueError:
						print('valerror')
						print(lines)
		if year == 'NULL' or year == '':
			continue
		else:
			try:
				fo.writelines(f'{files[0:4]}, {year}\n')
				date_list.append(year)
			except ValueError:
				print('val2')
# print('The length is ' + str(len(reso_list)))
binwidth = 1
print(date_list)
plt.hist(date_list, bins=range(min(date_list), max(date_list) + 1, binwidth))
plt.show()