# ----------------------------------------------------------
# this code is for extracting some files from
# tar ball of chimera formats in T3
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
from subprocess import call

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
idfile = '/Users/tkimura/Desktop/t3_mnt/zdock/pdbid_hfrac_ltoeq_2.csv'
anifile = '/Users/tkimura/Desktop/t3_mnt/zdock/anisou_to_rerun_all.csv'

# all allchains <= 2.0
alllist = []
with open(idfile) as f:
	for lines in f.readlines():
		alllist = lines.replace('\ufeff','').split(',')
		break

# anisous list
anilist = []
with open(anifile) as af:
	for lines in af.readlines():
		anilist.append(lines.replace('\n', ''))

# long anisou list = run list
anilist_long = []
for item in alllist:
	if item[0:4] in anilist:
		anilist_long.append(item)
print(sorted(anilist_long))
import os, sys
os.chdir('/Users/tkimura/Desktop/t3_mnt/zdock/chimera_format_tarred/')

for item in anilist_long:
	if item[0] != '4':
		continue
	# command = ['tar', '-xvf', './chimera_hb'+ str(item[0]) + '.gz','--wildcards', '*' + item + '*']
	command = 'tar -xvf chimera_hb'+ str(item[0]) + '.gz --wildcards *' + item + '*'
	# command = 'tar -xvf chimera_hb'+ str(item[0]) + '.gz *' + item + '*'
	print(command)
	call(command, shell=True)