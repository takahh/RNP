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
reso_summary = '/Users/tkimura/Desktop/RNP/resolutions/xray_cif.csv'
reso_list = []

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
with open(reso_summary, 'w') as fo:
	for files in os.listdir(path):
		id = ''
		reso = 100
		if '.cif' in files:
			# print(files)
			with open(path + files) as f:
				for lines in f.readlines():
					try:
						if '_reflns.d_resolution_high' in lines:
							# print('1')
							# print(lines)
							reso = lines.split()[1]
							break
						# elif '_em_3d_reconstruction.resolution_' in lines:
						# 	print('2')
						# 	if 'FSC' in lines.split()[1] or '?' in lines.split()[1]:
						# 		continue
						#
						# elif '_em_3d_reconstruction.resolution' in lines:
						# 	print('3')
						# 	print(lines)
						# 	reso = lines.split()[1]
					except IndexError:
						print(lines)
					except ValueError:
						print(lines)
		if reso == 100:
			print('resolution not found')
			continue
		# print(f'{files[0:4]}:{reso}')
		if reso == 'NULL':
			continue
		else:
			try:
				fo.writelines(f'{files[0:4]}, {reso}\n')
				reso_list.append(float(reso))
			except ValueError:
				print(reso)
print('The length is ' + str(len(reso_list)))
binwidth = 1
plt.hist(reso_list, bins=range(round(min(reso_list)), round(max(reso_list)) + 1, binwidth))
plt.show()