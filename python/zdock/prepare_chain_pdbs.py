# ----------------------------------------------------------
# this code is for preparing two pdbb files
# INPUT : (pdbid + chainid) list, PDB file
# OUTPUT : pdb file1, pdb file2
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import os, sys
import pandas as pd

# ----------------------------------------------------------
# make runlist
# ----------------------------------------------------------
def get_anisous():
	anisou_list = []
	anisous = '/Users/tkimura/Desktop/RNP/check_contact/anisou_list_xray.csv'
	# make anisou_list
	with open(anisous) as f:
		for lines in f.readlines():
			anisou_list.append(lines.replace('\n', '').replace('\r', ''))
	return anisou_list

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
# idlist = ['5on3_A_B', '5on3_D_E', '5wqe_A_B', '2iz9_A_R', '2iz9_C_S', '2b2e_C_S', '2bq5_C_S', '5wea_A_B', '4aq7_A_B', '4aq7_D_E', '2b2d_C_S', '4pkd_B_V', '1zho_E_F', '5on2_A_B', '5on2_D_E', '4prf_A_B', '2cv2_A_C', '2cv2_B_D', '2xlj_A_B', '2det_A_C', '1b7f_A_P', '2izm_C_S', '3epk_A_E', '3epk_B_F', '5vw1_A_C', '2ab4_A_B', '1zjw_A_B', '5z9x_A_R', '3sn2_A_B', '5w1i_A_B', '5w1i_C_D', '5w1h_A_B', '2yjy_A_C', '2yjy_B_D', '5u34_A_B', '4jvh_A_D', '1n78_A_C', '1n78_B_D', '5xbl_A_B', '4pr6_A_B', '3snp_A_C', '3snp_B_D', '1lng_A_B', '3foz_A_C', '3foz_B_D', '6h9i_B_E', '5vm9_A_B', '5vm9_C_D', '2dxi_A_C', '2dxi_B_D', '1y39_A_C', '1y39_B_D', '4zt9_A_B', '4zt9_C_D', '2re8_A_B', '1gtr_A_B', '3t5q_E_F', '3t5q_K_L', '1gts_A_B', '3q0n_B_D', '5wtk_A_B', '3qjj_A_Q', '3qjj_B_R', '6oon_A_B', '4n0t_A_B', '2oih_A_B', '1cvj_A_M', '1cvj_B_N', '1cvj_E_Q', '1cvj_F_R', '1cvj_G_S', '5wwr_A_C', '5wwr_B_D', '3am1_A_B', '3q0l_B_D', '3q0m_A_C', '3q0m_B_D', '5b63_A_B', '5wws_A_C', '5wws_B_D', '2db3_A_E', '1ob5_A_B', '3k4e_A_B', '3k4e_C_D', '3k4e_E_F', '4pmw_A_C', '4pmw_B_D', '5d6g_A_0', '3amu_A_B', '6gc5_A_E', '5wzg_A_B', '1ivs_A_C', '1ivs_B_D', '3amt_A_B', '1vc6_A_B', '2vpl_C_D', '3b0v_C_A', '3b0v_D_B', '1ob2_A_B', '6aay_A_B', '2hw8_A_B', '1euq_A_B', '5wwt_A_C', '5wwt_B_D', '2y8w_A_B', '6iv8_A_B', '6iv8_C_D', '6iv9_A_B', '2pjp_A_B', '5wlh_A_B', '4olb_A_B', '1g59_A_B', '1g59_C_D', '4f3t_A_R', '5wty_B_D', '6aax_C_D', '4b3g_A_G', '3wqy_A_C', '1m8y_B_D', '5f5f_G_H', '3q0q_A_B', '4zt0_A_B', '4zt0_C_D', '4tyy_A_B', '5wzh_A_B', '5w6v_A_R', '5bz1_A_B', '5wzi_A_B', '3q0p_B_D', '6qic_D_H', '5msf_A_R', '1mms_A_C', '1mms_B_D', '1m8x_B_D', '3k49_A_B', '3k49_C_D', '3k49_E_F', '1qru_A_B', '5ah5_A_C', '5ah5_B_D', '1drz_A_B', '1e7k_A_C', '3q0s_A_B', '1gax_A_C', '1gax_B_D', '6fpx_A_B', '6fpx_C_D', '1qrt_A_B', '5wt3_A_C', '5bzv_A_B', '5bym_A_C', '1ec6_B_C', '2rd2_A_B', '4tv0_A_B', '1ffy_A_T', '1qrs_A_B', '5yyn_A_B', '1u0b_B_A', '5bzu_A_B', '5bz5_A_B', '1euy_A_B', '5wt1_A_C', '5wt1_B_F', '3ktw_A_C', '3ktw_B_D', '5tf6_A_B', '5tf6_C_D', '1s03_H_A', '1s03_G_B', '3r9x_A_C', '1fxl_A_B', '6dtd_A_C', '4jxz_A_B', '6i3p_C_G', '2i82_A_E', '2i82_B_F', '2i82_D_H', '5i9h_A_B', '1n77_A_C', '1n77_B_D', '5dea_B_A', '1qu3_A_T', '6du5_A_B', '5de5_B_A', '5de5_D_C', '1qa6_B_D', '3akz_C_G', '6ifo_A_C', '6ifo_B_D', '5ng6_A_B', '5ng6_C_D', '5ng6_E_F', '5ng6_G_H', '4jxx_A_B', '6du4_A_B', '1qu2_A_T', '2zzm_A_B', '2zuf_A_B', '1o0b_A_B', '1vfg_B_D', '5npm_A_B', '1o0c_A_B', '1hc8_A_C', '2czj_C_D', '1mfq_B_A', '2vod_A_C', '2zxu_A_C', '2zxu_B_D', '5js1_A_B', '2zm5_A_C', '2zm5_B_D', '2bs0_C_S', '4jyz_A_B', '6f4h_A_B', '6f4h_C_D', '6f4h_E_F', '5onh_A_B', '5onh_D_E', '2vop_A_B', '1qtq_A_B', '2om7_K_J', '6nma_B_G', '3j5s_F_A', '5zey_C_A', '3j0l_J_1', '1ry1_B_A', '5osg_h_2', '6mcb_A_B', '3deg_H_G', '6mcc_A_B', '2j37_B_A', '5zal_A_C', '6nm9_B_G', '6nm9_D_E', '5vzl_A_B']
# idlist = ["1fka_H_A", "3b0v_D_B", "3iz4_B_A", "2ogm_B_0", "3b0v_C_A"]

idfile = '/Users/tkimura/Desktop/RNP/check_contact/pdbid_hfrac_ltoeq_2.csv'
with open(idfile) as f:
	for lines in f.readlines():
		idlist = lines.replace('\ufeff','').split(',')
		break

bpath = '/Users/tkimura/Desktop/RNP/check_contact/'
pdb_path_EM = '/Users/tkimura/Desktop/RNP/check_contact/PDBfiles/EM/'
pdb_path_xray = '/Users/tkimura/Desktop/RNP/check_contact/PDBfiles/xray/'
outpath = '/Users/tkimura/Desktop/RNP/zdock/pdb/' # 1ABC/1ABC_r, 1ABC/1ABC_p
path = ''
vec_file = bpath + 'non_redun_positives.txt'
run_list = get_anisous()

# ----------------------------------------------------------
# preprocess
# ----------------------------------------------------------
# df = pd.read_csv(vec_file)
# idlist = df['vec_id'].to_list()
# print(idlist)

# ----------------------------------------------------------
# main
# ----------------------------------------------------------

# prepare pdb file list
EM_pdb_list = os.listdir(pdb_path_EM)
xray_pdb_list = os.listdir(pdb_path_xray)

keepgoing = 0

for id in idlist:
	pdbid = id.split('_')[0]
	if pdbid not in run_list:
		print('passed ' + pdbid)
		continue

	# if pdbid in ['2ht1', '3b0v']:
	# 	keepgoing = 1
	#
	# if keepgoing == 1:
	# 	pass
	# else:
	# 	continue

	pchain = id.split('_')[1]
	rchain = id.split('_')[2]
	if f'{pdbid}.pdb' in EM_pdb_list:
		path = pdb_path_EM
	elif  f'{pdbid}.pdb' in xray_pdb_list:
		path = pdb_path_xray
	outdir = f'{outpath}/{id}'
	try:
		os.mkdir(outdir)
	except FileExistsError:
		pass

	# make p chain pdb file
	#0123456789012345678901
	#ATOM   3434  CA  GLY A  15
	write = 0
	try:
		with open(f'{outdir}/{pdbid}_p.pdb', 'w') as fo:
			with open(f'{path}/{pdbid}.pdb') as f:
				for lines in f.readlines():
					if write == 0:
						if lines[0:4] == 'ATOM' and len(lines[17:20].strip()) == 3 and lines[20:22].strip() == pchain:
							print('start!')
							write = 1
							fo.writelines(lines)
						else:
							continue
					elif write == 1:
						if lines[0:3] == 'TER':
							fo.writelines(lines)
							break
						else:
							fo.writelines(lines)


		# make r chain pdb file
		write = 0
		with open(f'{outdir}/{pdbid}_r.pdb', 'w') as fo:
			with open(f'{path}/{pdbid}.pdb') as f:
				for lines in f.readlines():
					if write == 0:
						#          111111111122222222
						#01234567890123456789012345678901234567890123456789
						#ATOM  18341  C4    G A 951      11.728  84.306 158.402  1.00 30.00           C
						if lines[0:4] == 'ATOM' and len(lines[17:20].strip()) == 1 and lines[20:22].strip() == rchain:
							write = 1
							fo.writelines(lines)
						else:
							continue
					elif write == 1:
						if lines[0:3] == 'TER':
							fo.writelines(lines)
							break
						else:
							fo.writelines(lines)
	except FileNotFoundError:
		print(f'{id} not done')
		continue
	print(f'{id} is done')
