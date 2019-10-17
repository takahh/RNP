# ----------------------------------------------------------
# this code is for 
# make correct indat section in hip.inp file
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
file = '/Users/tkimura/Desktop/atoms_tofragment.txt'
indatfile = '/Users/tkimura/Desktop/hip_indat.txt'

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
lastresi = '0'
with open(indatfile, 'w') as fo:
	with open(file) as f:
		for lines in f.readlines():
			try:
				#           11111111112222222
				# 012345678901234567890123456
				# ATOM   5378 HE21 GLN A 412      34.401 -14.519  47.361  1.00  0.00           H
				if lines[0:3] == 'TER':
					continue
				if lines[22:26].strip() != lastresi: # new resi
					start_atom = lines[4:11].strip()
					if lastresi != '0':
						fo.writelines(last_startatom + '\t-' + lastatom + '\t' + '0\n')
				lastresi = lines[22:26].strip()
				lastatom = lines[4:11].strip()
				last_startatom = start_atom
			except AttributeError:
				print(lines)
