# ----------------------------------------------------------
# this code is for extracting nonredundant positive dataset
# with simplest classification : amino acid - base
# ----------------------------------------------------------

def gen_vectors(path, opath):

	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------

	# ----------------------------------------------------------
	# constants
	# ----------------------------------------------------------
	aminos = ['ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLU', 'GLN', 'GLY', 'HIS', 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL']
	baces = ['A', 'C', 'G', 'U']
	vector = [0] * 80
	all_ch_dic, unique_dic = {}, {}

	# ----------------------------------------------------------
	# functions
	# ----------------------------------------------------------


	# takes amino acid and bbace, and return the index of the list
	def locate_pair(amino, bace):
		# 0      1      2       3       4
		# Ala-A  Ala-C	Ala-G	Ala-U	Arg-A
		try:
			return 4 * aminos.index(amino) + baces.index(bace)
		except ValueError as e:
			print(e)
			return -1


	native_dic = {}
	with open('/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt') as f:
		for lines in f.readlines():
			if 'vec_id' in lines:
				continue
			element = lines.split(',')
			native_dic[element[0]] = element[2:82]


	def judge_native_vector(vec_id, vec):
		vec_id = f"{vec_id.split('_')[0]}_{vec_id.split('_')[1][-1]}_{vec_id.split('_')[2]}"
		if native_dic[vec_id] == vec:
			return True
		else:
			return False


	# add or append the count vector to exsinting one if any
	def append_or_add(unique_dic, vecid, exp, count_vector):
		if vecid not in unique_dic.keys():
			unique_dic[vecid] = [exp, count_vector]
		else:
			new_ct_vec = [unique_dic[vecid][1][i] + count_vector[i] for i in range(80)]
			unique_dic[vecid] = [exp, new_ct_vec]
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


	# write each vector/list to a file at the last step
	def write_dic_to_file(file, unique_dictionary):
		for key in unique_dictionary.keys():
			vecid = key
			exp = unique_dictionary[vecid][0]
			count_vector = unique_dictionary[vecid][1]
			if judge_native_vector(vecid, count_vector):
				print(vecid)
				continue
			# fetch 'allchains' by vec_id
			with open(file, 'a') as fo:
				fo.writelines(f'{vecid},{exp},')
				i = 0
				for item in count_vector:
					if i == 79:
						fo.writelines(f'{item},-10\n')
					else:
						fo.writelines(f'{item},')
					i += 1

	# ----------------------------------------------------------
	# main
	# ----------------------------------------------------------
	with open(path) as f:
		last_vec_id = ''
		open_ofile()
		for lines in f.readlines():
			if 'pdbid' in lines: # skip the header row
				continue
			if lines == "": # when EOF, update the dic of vectors
				unique_dic = append_or_add(unique_dic, vec_id, element[1], vector) # unique_dic updated
			# 0		1		2		3		4		5		6	7	8	9	10			11
			# pdbid	exp		presi	pchain	rresi	rchain	pp	pr	rp	rr	allchains	allchains3
			# 2cv1	xray	THR		A		A		C
			element = lines.split('\t')
			pdbid = element[0]
			pchain = element[3]
			rchain = element[5][:-1]
			presi = element[2]
			rresi = element[4]

			# skip if the residue or the base is uncanonical
			if presi not in aminos or rresi not in baces:
				print(lines)
				continue

			vec_id = f'{pdbid}_{pchain}_{rchain}'
			if last_vec_id == '' or last_vec_id == vec_id: # the first data row or continued row
				vector = add_one(element[2], element[4], vec_id, vector)
			elif vec_id != last_vec_id: # different chain pair
				unique_dic = append_or_add(unique_dic, vec_id, element[1], vector) # unique_dic updated
				vector = [0] * 80
				vector = add_one(element[2], element[4], vec_id, vector)
			last_vec_id = vec_id
		# write unique_dic to the file
		write_dic_to_file(opath, unique_dic)


ifile = '/Users/tkimura/Desktop/RNP/zdock/hbond_summary.csv'
ofile = '/Users/tkimura/Desktop/RNP/zdock/vectors.csv'

gen_vectors(ifile, ofile)