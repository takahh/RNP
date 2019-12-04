# ----------------------------------------------------------
# this code is for searching best angles from the results
# of ranges of angles
# ----------------------------------------------------------

def search_best_angles(reso_limit, contact_limit, remove_id_list, exp):
	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------
	import pandas as pd
	from subprocess import call
	from python.resolutions.resolution_list import resolution_list as reso
	from python.svm.filter_by_contacts import filter_by_contacts

	# ----------------------------------------------------------
	# constants
	# ----------------------------------------------------------
	bpath = '/Users/tkimura/Desktop/RNP/svm/'
	bpath2 = '/Users/tkimura/Desktop/t3_mnt/zdock/python/polar_range_mpi/data_from_laptop/outs/'
	max0 = bpath2 + 'w_range_max_0.csv'
	min0 = bpath2 + 'w_range_min_0.csv'
	output = bpath + 'study_best_w.csv'
	svm = bpath + 'svm_out_normed.csv'
	positive = "/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt"

	df_svm = pd.read_csv(svm)
	all_list = df_svm['chain'].values.tolist()
	id_list_by_contacts_filter = filter_by_contacts(contact_limit)
	if exp != []:
		df_posi = pd.read_csv(positive)
		print('before:' + str(len(id_list_by_contacts_filter)))
		list_filtered_by_exp = df_posi[df_posi['exp'] == exp]['vec_id'].tolist()
		id_list_by_contacts_filter = [x for x in id_list_by_contacts_filter if x in list_filtered_by_exp]
		print('after:' + str(len(id_list_by_contacts_filter)))
	id_list_by_contacts_filter = [x for x in id_list_by_contacts_filter if x not in remove_id_list]

	angle_set_list = []

	# conncatenate max data
	df_max = pd.read_csv(max0)
	for i in range(27):
		df_toadd = pd.read_csv(bpath2 + 'w_range_max_' + str(i+1) + '.csv')
		df_max = pd.concat([df_max, df_toadd])

	# conncatenate min data
	df_min = pd.read_csv(min0)
	for i in range(27):
		df_toadd = pd.read_csv(bpath2 + 'w_range_min_' + str(i+1) + '.csv')
		df_min = pd.concat([df_min, df_toadd])

	# make the output file
	with open(output, 'w') as fo:
		fo.writelines('i,min_count,count,count1,count2,count1,count2\n')

	################################################
	# filter max_df by resolution and all_chains
	################################################
	df_max['short_id'] = df_max['id'].str[:4]
	max_tmp_df = df_max[df_max.id.isin(id_list_by_contacts_filter)]
	selected_max_df = max_tmp_df.merge(reso(reso_limit), left_on='short_id', right_on='id')
	print('len(selected_max_df)')
	print(len(selected_max_df))

	################################################
	# filter min_df by resolution and all_chains
	################################################
	df_min['short_id'] = df_min['id'].str[:4]
	min_tmp_df = df_min[df_min.id.isin(id_list_by_contacts_filter)]
	selected_min_df = min_tmp_df.merge(reso(reso_limit), left_on='short_id', right_on='id')
	print(len(selected_min_df))

	for c in range(79):
		if c != 19:
			continue
		max_list = selected_max_df[str(c)].values.tolist()
		min_list = selected_min_df[str(c)].values.tolist()
		# find a minimum gap
		all_list = max_list + min_list

		# sweep the whole range to count big min and small max
		# and find the min count and the max angle
		with open(output, 'a') as fo:

			# count low max and high min changing a border
			min_count = 300
			best_angle = 0
			end = max(all_list)
			start = min(all_list)
			step = 0.001
			maxcount = int((end - start) / step)
			max_angle, min_angle = 0, 10

			# ----------------------------------------------------------
			# find the min_angle and the count
			# ----------------------------------------------------------
			border = start # ascending
			for i in range(maxcount):
				count1, count2 = 0, 0
				for val in max_list: # count smaller max
					if val < border:
						count1 += 1
				for val in min_list: # count bigger min
					if val > border:
						count2 += 1
				count = (count1 + count2)/2
				if count < min_count: # update the smallest angle
					min_count = count
					min_angle = border
				border += step

			# print(f'min count is {min_count} at the value {max_angle}')

			# ----------------------------------------------------------
			# find the max_angle with the previous count
			# ----------------------------------------------------------
			border = end # descending
			for i in range(maxcount):
				count1, count2 = 0, 0
				for val in max_list: # count smaller max
					if val < border:
						count1 += 1
				for val in min_list: # count bigger min
					if val > border:
						count2 += 1
				count = (count1 + count2)/2

				# if count == min_count:  # update the lowest point
				# 	max_angle = border
				# 	border -= step
				# 	# break
				# else:
				border -= step
				fo.writelines(f'{i}, {border}, {min_count}, {count}, {count1}, {count2}, {abs(count1 - count2)}\n')
