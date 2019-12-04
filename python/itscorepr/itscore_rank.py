# ----------------------------------------------------------
# this code returns id and itscore rank
# depending on reolution and allchains
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import pandas as pd

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
posi_score = '/Users/tkimura/Desktop/t3_mnt/zdock/itscorepr/positive.csv'
nega_score_dir = '/Users/tkimura/Desktop/t3_mnt/zdock/itscorepr/'
its_rank_result = '/Users/tkimura/Desktop/t3_mnt/zdock/itscorepr/rankings.csv'

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------

# run only one time
with open(its_rank_result, 'w') as fo:
	with open(posi_score) as f:
		fo.writelines('id, its_rank' + '\n')
		for lines in f.readlines():
			rank = 1
			if '.' in lines:
				print(lines)
				id = lines.split(',')[0]
				print(id)
				posi_score = lines.split(',')[1].replace('\n', '')
				try:
					df = pd.read_csv(nega_score_dir + id + '.csv')
				except FileNotFoundError:
					continue
				nega_score_list = df['score'].tolist()
				for score in nega_score_list:
					try:
						if score < float(posi_score):
							rank += 1
					except TypeError:
						print(score)
				fo.writelines(id + ',' + str(rank) + '\n')