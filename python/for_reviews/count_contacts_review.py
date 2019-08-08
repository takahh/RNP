file = '/Users/tkimura/Desktop/2cv1.hb2'
ofile = '/Users/tkimura/Desktop/2cv1_sub.csv'
i = 0
with open(ofile, 'w') as fo:
	with open(file) as f:
		for lines in f.readlines():
			i += 1
			if i <= 8:
				continue
			if lines[0] == lines[14]:
				continue
			if lines[6:9] != 'HOH' and lines[20:23] != 'HOH':
				fo.writelines(f'{lines[0]},{lines[6:9]},{lines[14]},{lines[20:23]}\n')

#           11111111112222222222333333
# 012345678901234567890123456789012345678901234567890123456789
# A0411-ALA N   A0408-THR OG1 2.86 MS   3  5.10 170.1  1.87 151.4 154.2   959