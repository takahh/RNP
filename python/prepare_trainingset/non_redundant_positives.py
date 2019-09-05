# ----------------------------------------------------------
# this code is for extracting nonredundant positive dataset
# with simplest classification : amino acid - base
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
path = '/Users/tkimura/Desktop/RNP/check_contact/hbond_summary.txt'
opath = '/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt'
aminos = ['ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLU', 'GLN', 'GLY', 'HIS', 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL']
baces = ['A', 'C', 'G', 'U']
vector = [0] * 80
all_ch_dic, unique_dic = {}, {}

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------


# make allchains dictionary
def make_all_chains_dic():
	with open(path) as f:
		for line in f.readlines():
			element = line.split('\t')
			# 0		1	2		3		4		5		6	7	8	9	10			11
			# pdbid	exp	presi	pchain	rresi	rchain	pp	pr	rp	rr	allchains	allchains3
			# 2cv1	xray	THR	A	A	C	[]	[]	[37]	[]	1	1
			key = f'{element[0]}_{element[3]}_{element[5]}'
			if key not in all_ch_dic.keys():
				all_ch_dic[key] = element[10]
	return all_ch_dic


# takes amino acid and bbace, and return the index of the list
def locate_pair(amino, bace):
	# 0      1      2       3       4
	# Ala-A  Ala-C	Ala-G	Ala-U	Arg-A
	try:
		return 4 * aminos.index(amino) + baces.index(bace)
	except ValueError as e:
		print(e)
		return -1


# write each vector/list to a file at the last step
def write_dic_to_file(file, unique_dictionary, allchain_dic):
	for key in unique_dictionary.keys():
		vecid = key
		exp = unique_dictionary[vecid][0]
		count_vector = unique_dictionary[vecid][1]
		# fetch 'allchains' by vec_id
		allchains = allchain_dic[vecid]
		with open(file, 'a') as fo:
			fo.writelines(f'{vecid},{exp},')
			i = 0
			for item in count_vector:
				if i == 79:
					fo.writelines(f'{item},{allchains}\n')
				else:
					fo.writelines(f'{item},')
				i += 1


# add or append the count vector to exsinting one if any
def append_or_add(unique_dic, vecid, exp, count_vector):
	if vec_id not in unique_dic.keys():
		unique_dic[vecid]  = [exp, count_vector]
	else:
		new_ct_vec = [unique_dic[vecid][1][i] + count_vector[i] for i in range(80)]
		unique_dic[vecid]  = [exp, new_ct_vec]
	return unique_dic


# make a string of column names separated by a comma
def make_column_names():
	column_strings = 'vec_id,exp'
	for amino in aminos:
		for bace in baces:
			column_strings = f'{column_strings},{amino}_{bace}'
	column_strings = f'{column_strings},all_chains'
	return column_strings


# open the output file bebfore adding rows
def open_ofile():
	with open(opath, 'w') as fo:
		columns = make_column_names()
		fo.writelines(columns)
		fo.writelines('\n')


# add 1 to the index of the vector
def add_one(presi, rresi, vecid, cvector):
	# add one, and write
	index = locate_pair(presi, rresi)
	if index == -1:
		print(vecid)
		return cvector
	cvector[index] += 1
	return cvector


# ----------------------------------------------------------
# main
# ----------------------------------------------------------
with open(path) as f:
	last_vec_id = ''
	open_ofile()
	all_chains_dic = make_all_chains_dic()
	for lines in f.readlines():
		if 'pdbid' in lines: # skip the header row
			continue
		# 0		1		2		3		4		5		6	7	8	9	10			11
		# pdbid	exp		presi	pchain	rresi	rchain	pp	pr	rp	rr	allchains	allchains3
		# 2cv1	xray	THR		A		A		C
		element = lines.split('\t')
		pdbid = element[0]
		pchain = element[3]
		rchain = element[5]
		presi = element[2]
		rresi = element[4]

		# skip if the residue or the base is uncanonical
		if presi not in aminos or rresi not in baces:
			print(lines)
			continue

		vec_id = f'{pdbid}_{pchain}_{rchain}'
		if last_vec_id == '' or last_vec_id == vec_id: # the first data row or continued row
			vector = add_one(element[2], element[4], vec_id, vector)
		elif vec_id != last_vec_id: # continued pdbid
			unique_dic = append_or_add(unique_dic, vec_id, element[1], vector) # unique_dic updated
			vector = [0] * 80
			vector = add_one(element[2], element[4], vec_id, vector)
		last_vec_id = vec_id
	# write unique_dic to the file
	write_dic_to_file(opath, unique_dic, all_chains_dic)
