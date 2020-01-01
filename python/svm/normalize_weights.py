# ----------------------------------------------------------
# this code is for normalizing the output from SVM
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
svm_solution = "/Users/tkimura/Desktop/RNP/svm/svm_out.csv"
# svm_solution = "/Users/tkimura/Desktop/RNP/svm/svm_out_vdw.csv"
svm_norm = "/Users/tkimura/Desktop/t3_mnt/zdock/python/polar_range_mpi/data_from_laptop/svm_out_normed.csv"
# svm_norm = "/Users/tkimura/Desktop/t3_mnt/zdock/python/polar_range_mpi/data_from_laptop/svm_out_vdw_normed.csv"
skipcolumns = ['posi_count', 'native_exist', 'iter']
# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
df = pd.read_csv(svm_solution)
with open(svm_norm, 'w') as fo:
	with open(svm_solution) as f:
		for lines in f.readlines():
			if 'ALA' in lines:
				fo.writelines(lines)
				continue

			# calculate norm to normalize
			# chain,posi_count,native_exist,c_value,norm,iter,ALA_A,
			ele = lines.split(',')
			normsq = 0
			# for weight in ele[5:165]:
			for weight in ele[5:85]:
				normsq += float(weight)**2.0
			norm = normsq**0.5

			# normalize and make a new file
			for idx, val in enumerate(ele):
				# if idx >= 5 and idx != 165:
				if idx >= 5 and idx != 85:
					val = val.replace('[', '').replace(']', '').replace('\n', '')
					fo.writelines(str(float(val)/norm) + ',')
				# elif idx == 165:
				elif idx == 85:
					fo.writelines(val)
				else:
					fo.writelines(val + ',')