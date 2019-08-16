########################################################
# this program counts contacts of each chain in the
# outputs of HBPLUS.
#
# make a contact table for each chain
# the output will be like
# PDBID, CHAINID, PP, RR, PR, N_CHAIN_PP, N_CHAIN_RR, N_CHAIN_PR,
########################################################
'''
01234567890123456789012345678901234567890123456789
A0014-GLY N   B0011-  U OP1 2.13 MH  -2 -1.00 154.8  1.20 132.9 141.8     1
A2172-HOH O   A0017-SER O   3.09 HM  -2 -1.00 151.3  2.17 130.4 133.2     2
'''

import sys, pathlib, os, shutil, subprocess


def contact_table(input_file, output_file):
	pdb_name = input_file.split('/')[-1].replace('.hb2', '')

	########################################################
	# get a list of unique chain id
	########################################################
	with open(input_file) as f:
		i = 0
		unique_chain_list = []
		for lines in f.readlines():
			i += 1
			if i >= 9: # skip the first 8 lines
				chain1 = lines[0]
				chain2 = lines[14]
				restyp1 = lines[6:9].replace(' ', '')
				restyp2 = lines[20:23].replace(' ', '')
				for res, chain in [[restyp1, chain1], [restyp2, chain2]]:
					if res == 'HOH':
						continue
					else: # assign the res protein or RNA
						if len(res.replace(' ', '')) == 1:
							restyp = 'rna'
						elif len(res.replace(' ', '')) == 3:
							restyp = 'pro'
						else:
							continue
					if [chain, restyp] not in unique_chain_list:
						unique_chain_list.append([chain, restyp])

	########################################################
	# a function to update unique_chain_list
	########################################################
	def add_chain_list(ref_chain, chain1, chain2, unique_ch_list):
		if ref_chain == chain1 and chain2 not in unique_ch_list:
			unique_ch_list.append(chain2)
		elif ref_chain == chain2 and chain1 not in unique_ch_list:
			unique_ch_list.append(chain1)
		return unique_ch_list


	########################################################
	# make a contact table for each chain
	########################################################
	with open(output_file, 'a+') as fo1:
		for chain in unique_chain_list:
			count_pp_contacts = 0 # # of contacts
			count_rr_contacts = 0
			count_pr_contacts = 0
			unique_pp_chains_list = [] # # of other chains in contact
			unique_rr_chains_list = []
			unique_pr_chains_list = []
			with open(input_file) as f:
				for lines in f.readlines():
					if 'HBPLUS' in lines:
						continue
					else:
						node1 = lines[6:9].replace(' ', '')
						node2 = lines[20:23].replace(' ', '')
						chain1 = lines[0]
						chain2 = lines[14]
						if chain1 == chain2:
							continue
						# check HOH is not included
						if 'HOH' in node1 or 'HOH' in node2:
							continue
						elif (chain[0] == chain1) or (chain[0] == chain2):
							if len(node1) + len(node2) != 4:
								if len(node1) + len(node2) == 6: # p-p
									count_pp_contacts += 1
									unique_pp_chains_list = add_chain_list(chain[0], chain1, chain2, unique_pp_chains_list)
								elif len(node1) ==1 and len(node2) == 1: # r-r
									count_rr_contacts += 1
									unique_rr_chains_list = add_chain_list(chain[0], chain1, chain2, unique_rr_chains_list)
							else: # when len + len == 4
								count_pr_contacts += 1					# p-r
								unique_pr_chains_list = add_chain_list(chain[0], chain1, chain2, unique_pr_chains_list)
			# fo1.writelines(pdb_name + ',' + chain[0] + ',' + chain[1] + ',' + str(count_pp_contacts) + ','\
			# 			+ str(count_rr_contacts) + ',' + str(count_pr_contacts) + str(len(unique_pp_chains_list))\
			# 			+ ',' + str(len(unique_rr_chains_list)) + ',' + str(len(unique_pr_chains_list)) + '\n')
			fo1.writelines(f'{pdb_name},{chain[0]},{chain[1]},{len(unique_pp_chains_list)},{count_pp_contacts},{len(unique_rr_chains_list)},\
								{count_rr_contacts},{len(unique_pr_chains_list)},{count_pr_contacts}\n')

########################################################
# constants
########################################################
path = '/Users/tkimura/Desktop/RNP/check_contact/hbplus_out/'
EM_path = path + 'EM/'
xray_path = path + 'xray/'
opath = '/Users/tkimura/Desktop/RNP/check_contact/'
xray_summary = opath + 'xray_contacts_summary.csv'
EM_summary = opath + 'EM_contacts_summary.csv'


########################################################
# main function
########################################################
def make_contact_table(path, output_file):
	i = 1
	# make a new output file
	with open(output_file, 'w') as f:
		pass
	# write columnn names
	with open(output_file, 'a') as fo:
		fo.writelines('pdb_entry,chain,restyp,ppchain,count_pp,rrchain,count_rr,prchain,count_pr' + '\n')
	# make a contact summary table
	for file in os.listdir(path):
		if 'hb2' in file:
			contact_table(path + file, output_file)
			i += 1
		# if i == 5:
		# 	break


make_contact_table(xray_path, xray_summary)
make_contact_table(EM_path, EM_summary)