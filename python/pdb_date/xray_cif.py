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
path = '/Users/tkimura/Desktop/RNP/downloads_PDB/xray_cif/'
date_summary = '/Users/tkimura/Desktop/RNP/pdb_date/xray_cif.csv'
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
		reso = 100
		if '.cif' in files:
			# print(files)
			with open(path + files) as f:
				for lines in f.readlines():
					try:
						if 'recvd_initial_deposition_date' in lines:
							date = lines.split()[1].strip() # 1999-11-28
							year = date.split('-')[0]
							break
					except IndexError:
						print(lines)
					except ValueError:
						print(lines)
		# print(f'{files[0:4]}:{reso}')
		if year == 'NULL':
			continue
		else:
			try:
				fo.writelines(f'{files[0:4]}, {year}\n')
				date_list.append(int(year))
			except ValueError:
				print(year)
print('The length is ' + str(len(date_list)))
binwidth = 1
plt.hist(date_list, bins=range(min(date_list), max(date_list) + 1, binwidth))
plt.show()