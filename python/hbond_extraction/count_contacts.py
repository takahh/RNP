path = '/Users/tkimura/Desktop/'
input_file = path + '1a34.hb2'
pdb_name = '1a34'

'''
01234567890123456789012345678901234567890123456789
A0014-GLY N   B0011-  U OP1 2.13 MH  -2 -1.00 154.8  1.20 132.9 141.8     1
A2172-HOH O   A0017-SER O   3.09 HM  -2 -1.00 151.3  2.17 130.4 133.2     2
'''

########################################################
# get a list of unique chain id
########################################################

with open(input_file) as f:
	i = 0
	unique_chain_list = []
	for lines in f.readlines():
		i += 1
		if i >= 9:
			chain1 = lines[0]
			chain2 = lines[14]
			if chain1 not in unique_chain_list:
				unique_chain_list.append(chain1)
			if chain2 not in unique_chain_list:
				unique_chain_list.append(chain2)

########################################################
# make a contact table for each chain
# the output will be like 'A 3 4 2'
########################################################

print('chain,count_pp,count_rr,count_pr')
for chain in unique_chain_list:
	count_pp = 0
	count_rr = 0
	count_pr = 0
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
				elif (chain == chain1) or (chain == chain2):
					# check the row is for a base and a residue
					if len(node1) + len(node2) != 4:
						# p-p
						if len(node1) + len(node2) == 6:
							count_pp += 1
						# r-r
						elif len(node1) + len(node2) == 2:
							# print(lines)
							count_rr += 1
					# when the sum is 4 (p-r contacts)
					else:
						# p-r
						count_pr += 1
		print(pdb_name + ', ' + chain + ', ' + str(count_pp) + ',' +str(count_rr) + ',' + str(count_pr))
