# ----------------------------------------------------------
# this code is for summarizing hbond raw hbond data
# to make a data file for info per chain
# output example
# {'chain': '4wta#0P', '#0Ap': 230, '#0Tp': 1, '#5Ap': 1, '#3Ap': 9, '#0Pr': 25, '#0Pp': 7}
# '#0Ap': 230 means that model #0, chain A, protein chain, 230 hbonds to chain 4wta#0P
# (4wta#0P means PDBID 4wta, chain id P, model#0)
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import os

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
xprm_list = ['EM']
# xprm_list = ['xray', 'EM']
path = '/Users/tkimura/Desktop/RNP/check_contact/'
root_path_from = path + 'hb_out_cleaned/'
root_path_to = path + 'chain_summary/'
file_counts = 0

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------
def unique_chain_list(experiment):
	# ----------------------------------------------------
	# return unique chain list for model #0
	# find a string that has '#0', and take the chain id
	# ----------------------------------------------------
	# input row example
	# 012345678901234567890123456789
	# 0  1   2    3      4  5   6
	# #0 ARG 28.B NE     #0 GLU 92.A OE1    no hydrogen  2.393  N/A

	list_of_unique_chains = []
	with open(root_path_from + experiment + "/" + file) as f:
		for line in f.readlines():
			try:
				element = line.split()
				if len(element[1]) == 1:
					type1 = "r"
				else:
					type1 = "p"
				if len(element[5]) == 1:
					type2 = "r"
				else:
					type2 = "p"
				chain1 = f'{element[0]}.{element[2].split(".")[1]}{type1}'
				chain2 = f'{element[4]}.{element[6].split(".")[1]}{type2}'
				for chain in [chain1, chain2]:
					if chain not in list_of_unique_chains and '#0' in chain:
						list_of_unique_chains.append(chain)
			except IndexError:
				print(file)
				print(line)
	return list_of_unique_chains


# ----------------------------------------------------------
# main
# ----------------------------------------------------------
# input row example
# 012345678901234567890123456789
# 0  1   2    3      4  5   6    7      8            9
# #0 ARG 28.B NE     #0 GLU 92.A OE1    no hydrogen  2.393  N/A

# noinspection DuplicatedCode
for xprm in xprm_list:
	with open(root_path_to + xprm + '/' + xprm + '_chain_summary.csv', 'w') as fo:
		for file in os.listdir(root_path_from + xprm + '/'):
			file_counts += 1
			if '.DS' in file:
				continue
			chain_list = unique_chain_list(xprm)
			for chain in chain_list: # collect touching chains info per unique chain
				touching_chain_dic = {}
				touching_chain_dic['chain'] = file[0:4] + chain
				with open(root_path_from + xprm + '/' + file) as f:
					for line in f.readlines():
						element = line.split()
						# find rows including '#0:' and the chain id
						model1 = element[0]
						model2 = element[4]
						chain1 = element[2].split('.')[1]
						chain2 = element[6].split('.')[1]
						if len(element[1]) == 1:
							type1 = "r"
						else:
							type1 = "p"
						if len(element[5]) == 1:
							type2 = "r"
						else:
							type2 = "p"
						if f'{model1}.{chain1}{type1}' == chain:
							touching_chain = f'{model2}.{chain2}{type2}'
							if touching_chain == chain: # if contact is in the same chain
								continue
							if touching_chain not in touching_chain_dic.keys():
								touching_chain_dic[touching_chain] = 1
							else:
								touching_chain_dic[touching_chain] += 1
						elif f'{model2}.{chain2}{type2}' == chain:
							touching_chain = f'{model1}.{chain1}{type1}'
							if touching_chain == chain: # if contact is in the same chain
								continue
							if touching_chain not in touching_chain_dic.keys():
								touching_chain_dic[touching_chain] = 1
							else:
								touching_chain_dic[touching_chain] += 1
					fo.writelines(str(touching_chain_dic) + '\n')