# ----------------------------------------------------------
# this code is for classifying hbonds
#              0  1   2     3     4  5 6   7
# in   hb      #0 ASN 212.A ND2   #0 U 5.P O4        no hydrogen  2.858  N/A
#      contact {'chain': '6ifr#0.Bp', '#0.Ap': 6, '#0.Ep': 11, '#0.Nr': 17, '#0.Jr': 5}
# out
# {'pdb': '1ABC', 	PDBID
#  'pchain':'p',  	蛋白鎖ID
#  'presi': 'ASP',	蛋白残基
#  'rchain':'q' , 	RNA鎖ID
#  'rresi': 'U',  	RNA塩基
#  'pp':[3,4,2,1],	pp hbond 数のリスト
#  'pr':[1], 		pr
#  'rr':[],         rr
#  'rp':[23, 22],   rp
#  'exp':'EM'}      実験方法
#  'rr_chain'			rr 総鎖数
#  'rp_chain'			rp 総鎖数
#  'pr_chain'			pr 総鎖数
#  'pp_chain'			pp 総鎖数
#  'all_chain'			総鎖数
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import os
from ast import literal_eval

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
hbpath1 = '/Users/tkimura/Desktop/RNP/check_contact/hb_out_cleaned/'
contactpath = '/Users/tkimura/Desktop/RNP/check_contact/chain_summary/'
contactfile = '_chain_summary.csv'
exp_list = ['xray', 'EM']
chaininfo_dic, out_dic = {}, {}
hbond_summary = '/Users/tkimura/Desktop/RNP/check_contact/hbond_summary.txt'

# ----------------------------------------------------------
# preparation
# ----------------------------------------------------------
# make a list of dictionaries of chain summary
# {'xray':{'1abcp':{...}, '1accr:{}, ....}, 'EM':[{}, {}, ]}

for exp in exp_list:
	subdic = {}
	with open(f'{contactpath}{exp}/{exp}{contactfile}') as f:
		for lines in f.readlines():
			if 'pdbid' in lines:
				continue
			dic = literal_eval(lines)
			subdic[dic['chain']] = dic
	chaininfo_dic[exp] = subdic

with open(hbond_summary, 'w') as fo:
	fo.writelines('pdbid	exp	presi	pchain	rresi	rchain	pp	pr	rp	rr	allchains	allchains3\n')

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
with open(hbond_summary, 'a') as fo:
	for exp in exp_list:
		for file in os.listdir(hbpath1 + exp):
			if '.DS' in file:
				continue
			with open(hbpath1 + exp + '/' +  file) as f:
				for lines in f.readlines(): # each hbond
					# 0  1   2     3     4  5 6   7
					# #0 ASN 212.A ND2   #0 U 5.P O4
					pp, pr, rp, rr = [], [], [], []
					pdbid = file[0:4]
					element = lines.split()
					if len(element[1].strip()) == 3 and len(element[5].strip()) == 1:
						presi = element[1].strip()
						rresi = element[5].strip()
						pchain = element[2].strip().split('.')[1]
						rchain = element[6].strip().split('.')[1]
					elif len(element[1].strip()) == 1 and len(element[5].strip()) == 3:
						presi = element[5].strip()
						rresi = element[1].strip()
						pchain = element[6].strip().split('.')[1]
						rchain = element[2].strip().split('.')[1]
					else:
						continue # skip when pp or rr interactions

					# '6ifr#0.Bp': {'chain': '6ifr#0.Bp', '#0.Ap': 6, '#0.Ep': 11, '#0.Nr': 17, '#0.Jr': 5}
					# get chain info on the RNA side
					try:
						rinfo_dic = chaininfo_dic[exp][f'{pdbid}#0.{rchain}r']
						for key in rinfo_dic:
							if key[-1] == 'p':
								rp.append(rinfo_dic[key])
							elif key[-1] == 'r':
								rr.append(rinfo_dic[key])
					except KeyError:
						# print(f'{exp}_KEYERROR!!!!')
						# print(f'{pdbid}#0.{rchain}r')
						pass
					# get chain info on the protein side
					try:
						pinfo_dic = chaininfo_dic[exp][f'{pdbid}#0.{rchain}p']
						for key in pinfo_dic:
							if key[-1] == 'p':
								pp.append(pinfo_dic[key])
							elif key[-1] == 'r':
								pr.append(pinfo_dic[key])
					except KeyError:
						# print(f'{exp}_KEYERROR!!!!')
						# print(f'{pdbid}#0.{rchain}p')
						pass
					all_chains = len(pp) + len(rp) + len(pr) + len(rr)
					all_chains_3 = len([num for num in pp if num >= 3]) + len([num for num in pr if num >= 3]) + len([num for num in rp if num >= 3]) + len([num for num in rr if num >= 3])
					fo.writelines(f'{pdbid}	{exp}	{presi}	{pchain}	{rresi}	{rchain}	{sorted(pp)}	{sorted(pr)}	{sorted(rp)}	{sorted(rr)}	{all_chains}	{all_chains_3}\n')