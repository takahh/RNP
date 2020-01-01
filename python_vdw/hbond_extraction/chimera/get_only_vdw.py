# ----------------------------------------------------------
# this code returns vdw list after removing hbonds
# ----------------------------------------------------------
import os

def remove_hbonds(all_contact_file, hbond_cleaned_file, vdw_only_file):
	hblist = []

	###################################
	# get hbonds
	###################################
	with open(hbond_cleaned_file) as f:
		for lines in f.readlines():
			if '#' in lines:
				hblist.append(lines.split()[:8])
	print(f'hb : {len(hblist)}')
	print(hblist)

	###################################
	# get allcontacts
	###################################
	vdwlist = []
	vdwlist2 = []
	with open(all_contact_file) as f:
		for lines in f:
			if '#' in lines:
				vdwlist.append(lines.split()[4:8] + lines.split()[:4])
				vdwlist2.append(lines.split()[:4] + lines.split()[4:8])
	print(f'vdw : {len(vdwlist)}')
	print(vdwlist)

	###################################
	# find common
	###################################
	commonlist = [x for x in vdwlist if x in hblist]
	vdw_only_list = [x for x in vdwlist if x not in hblist]
	vdw_only_list2 = [x for x in vdwlist2 if x not in hblist]
	print('common')
	print(len(commonlist))
	print('vdw only')
	print(len(vdw_only_list))
	print('vdw only2')
	print(len(vdw_only_list2))

	vdw_only_list2_reverse = [x[4:8] + x[:4] for x in vdw_only_list2]
	print(len(vdw_only_list2_reverse))
	print(vdw_only_list)
	vdw_only_common = [x for x in vdw_only_list2_reverse if x in vdw_only_list]
	print(vdw_only_common)
	print(len(vdw_only_common))

	###################################
	# find remaining vdws
	###################################
	with open(vdw_only_file, 'w') as fo:
		for item in vdw_only_common:
			fo.writelines("\t".join(item) + '\n')
	# return vdw_only_list


path = '/Users/tkimura/Desktop/RNP/check_contact/vdw_out_cleaned/xray/'
path_ref = '/Users/tkimura/Desktop/RNP/check_contact/hb_out_cleaned/xray/'
a = '/Users/tkimura/Desktop/RNP/check_contact/vdw_out_cleaned/xray/1qtq.hb2'
b = '/Users/tkimura/Desktop/RNP/check_contact/hb_out_cleaned/xray/1qtq.hb2'
c = '/Users/tkimura/Desktop/RNP/check_contact/vdw_out_cleaned/xray/1qtq_cleaned.hb2'

for files in os.listdir(path):
	if files[0] == '.' or 'clean' in files:
		continue
	out = files.replace('.hb2', '_cleaned.hb2')
	if os.path.exists(out):
		continue
	remove_hbonds(path + files, path_ref + files, path + out)