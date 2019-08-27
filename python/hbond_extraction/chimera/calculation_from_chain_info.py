# ----------------------------------------------------------
# this code is for summarizing chain info
# generates csv file with the following columns
#   input: /Users/tkimura/Desktop/RNP/check_contact/chain_summary/xray/xray_chain_summary.csv#
#   output: /Users/tkimura/Desktop/RNP/check_contact/chain_summary/xray/xray_chain_calclulated.csv
#
#  1 PDBID					pdbid
#  2 chain					chain
#  3 type					type
#  4 R chains in contact	r_chains
#  5 hbbonds with R			r_hbonds
#  6 Avg. hbbonds with R	r_avg_hbonds
#  7 P chains in contact	p_chains
#  8 hbbonds with P			p_hbonds
#  9 Avg. hbonds with P		p_avg_hbonds
#  10 models in contact		models
#  11 hbonnds with models	model_hbonds

# {'chain': '4wta#0.Ap', '#0.Ap': 176, '#2.Ap': 14, '#4.Ap': 4,
# 	'#0.Tr': 10, '#0.Tp': 1, '#5.Ap': 1, '#3.Ap': 9, '#0.Pr': 9,
# 	'#0.Pp': 6}
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
from ast import literal_eval

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
xprm_list = ['xray', 'EM']
path = '/Users/tkimura/Desktop/RNP/check_contact/'
root_path_from = path + 'chain_summary/'
root_path_to = path + 'chain_summary/'

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
for xprm in xprm_list:
	with open(f'{root_path_from}{xprm}/chain_summary_calculated.csv', 'w') as fo:
		fo.writelines("pdbid,chain,type,r_chains,r_hbonds,avg_r_hbonds,p_chains,p_hbonds,avg_p_hbonds,models,models_hbonds\n")
		with open(f'{root_path_from}{xprm}/{xprm}_chain_summary.csv') as f:
			for line in f.readlines():
				# initialize
				type = ''
				r_chains, p_chains, p_hbonds, r_hbonds = 0, 0, 0, 0
				avg_r_hbonds, avg_p_hbonds = 0, 0
				models, models_hbonds = 0, 0
				r_chain_dic, p_chain_dic, model_dic = {}, {}, {}
				# read from csv and change it to dictionary type
				line_dic = literal_eval(line)
				pdbid = line_dic['chain'][0:4]
				chain = line_dic['chain'][7:-1]
				for key, value in line_dic.items():
					if key == 'chain':
						type = value[-1]
						continue
					model = key.split('.')[0]
					# collect model information
					if model not in model_dic.keys():
						model_dic[model] = 1
					else:
						model_dic[model] += 1
					# '#0.Ap': 176
					# collect p informatin
					if key[-1] == 'p':
						model_chain = key[:-1] # e.g. '#0.A'
						if model_chain not in p_chain_dic:
							p_chain_dic[model_chain] = value
						else:
							p_chain_dic[model_chain] += value
					# collect r
					elif key[-1] == 'r':
						model_chain = key[:-1] # e.g. '#0.A'
						if model_chain not in r_chain_dic.keys():
							r_chain_dic[model_chain] = value
						else:
							r_chain_dic[model_chain] += value
				if len(p_chain_dic) > 0:
					p_chains = len(p_chain_dic)
					p_hbonds = sum(p_chain_dic.values())
					avg_p_hbonds = sum(p_chain_dic.values())/p_chains
				else:
					avg_p_hbonds = 0
				if len(r_chain_dic) > 0:
					r_chains = len(r_chain_dic.values())
					r_hbonds = sum(r_chain_dic.values())
					avg_r_hbonds = sum(r_chain_dic.values())/r_chains
				else:
					avg_r_hbonds = 0
				models = len(model_dic)-1
				model_dic.pop(model)
				models_hbonds = sum(model_dic.values())
				fo.writelines(f'{pdbid},{chain},{type},{r_chains},{r_hbonds},{avg_r_hbonds},{p_chains},{p_hbonds},{avg_p_hbonds},{models},{models_hbonds}\n')
