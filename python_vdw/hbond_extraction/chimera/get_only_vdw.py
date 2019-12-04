# ----------------------------------------------------------
# this code returns vdw list after removing hbonds
# ----------------------------------------------------------


def remove_hbonds(all_contact_file, hbond_cleaned_file):
	hblist = []

	###################################
	# get hbonds
	###################################
	with open(hbond_cleaned_file) as f:
		for lines in f.readlines():
			if '#' in lines:
				hblist.append(lines.split()[:8])

	###################################
	# get allcontacts
	###################################
	vdwlist = []
	with open(all_contact_file) as f:
		for lines in f:
			if '#' in lines:
				vdwlist.append(lines.split()[4:8] + lines.split()[:4])

	###################################
	# find common
	###################################
	commonlist = [x for x in vdwlist if x in hblist]

	###################################
	# find remaining vdws
	###################################
	return_list = []
	with open(all_contact_file) as f:
		for lines in f:
			if lines.split()[:8] not in commonlist:
				return_list.append(lines.split()[:8])
	return return_list