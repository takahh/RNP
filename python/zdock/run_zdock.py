# ----------------------------------------------------------
# this code is for running zdock
# on T3
# input : pchain_pdb file, rchain_pdb file
# output : *.out
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import subprocess
import pandas as pd

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
path = '/gs/hs0/tga-science/kimura/zdock/'
idlist = ['5on3_A_B', '5on3_D_E', '5wqe_A_B', '2iz9_A_R', '2iz9_C_S', '2b2e_C_S', '2bq5_C_S', '5wea_A_B', '4aq7_A_B', '4aq7_D_E', '2b2d_C_S', '4pkd_B_V', '1zho_E_F', '5on2_A_B', '5on2_D_E', '4prf_A_B', '2cv2_A_C', '2cv2_B_D', '2xlj_A_B', '2det_A_C', '1b7f_A_P', '2izm_C_S', '3epk_A_E', '3epk_B_F', '5vw1_A_C', '2ab4_A_B', '1zjw_A_B', '5z9x_A_R', '3sn2_A_B', '5w1i_A_B', '5w1i_C_D', '5w1h_A_B', '2yjy_A_C', '2yjy_B_D', '5u34_A_B', '4jvh_A_D', '1n78_A_C', '1n78_B_D', '5xbl_A_B', '4pr6_A_B', '3snp_A_C', '3snp_B_D', '1lng_A_B', '3foz_A_C', '3foz_B_D', '6h9i_B_E', '5vm9_A_B', '5vm9_C_D', '2dxi_A_C', '2dxi_B_D', '1y39_A_C', '1y39_B_D', '4zt9_A_B', '4zt9_C_D', '2re8_A_B', '1gtr_A_B', '3t5q_E_F', '3t5q_K_L', '1gts_A_B', '3q0n_B_D', '5wtk_A_B', '3qjj_A_Q', '3qjj_B_R', '6oon_A_B', '4n0t_A_B', '2oih_A_B', '1cvj_A_M', '1cvj_B_N', '1cvj_E_Q', '1cvj_F_R', '1cvj_G_S', '5wwr_A_C', '5wwr_B_D', '3am1_A_B', '3q0l_B_D', '3q0m_A_C', '3q0m_B_D', '5b63_A_B', '5wws_A_C', '5wws_B_D', '2db3_A_E', '1ob5_A_B', '3k4e_A_B', '3k4e_C_D', '3k4e_E_F', '4pmw_A_C', '4pmw_B_D', '5d6g_A_0', '3amu_A_B', '6gc5_A_E', '5wzg_A_B', '1ivs_A_C', '1ivs_B_D', '3amt_A_B', '1vc6_A_B', '2vpl_C_D', '1ob2_A_B', '6aay_A_B', '2hw8_A_B', '1euq_A_B', '5wwt_A_C', '5wwt_B_D', '2y8w_A_B', '6iv8_A_B', '6iv8_C_D', '6iv9_A_B', '2pjp_A_B', '5wlh_A_B', '4olb_A_B', '1g59_A_B', '1g59_C_D', '4f3t_A_R', '5wty_B_D', '6aax_C_D', '4b3g_A_G', '3wqy_A_C', '1m8y_B_D', '5f5f_G_H', '3q0q_A_B', '4zt0_A_B', '4zt0_C_D', '4tyy_A_B', '5wzh_A_B', '5w6v_A_R', '5bz1_A_B', '5wzi_A_B', '3q0p_B_D', '6qic_D_H', '5msf_A_R', '1mms_A_C', '1mms_B_D', '1m8x_B_D', '3k49_A_B', '3k49_C_D', '3k49_E_F', '1qru_A_B', '5ah5_A_C', '5ah5_B_D', '1drz_A_B', '1e7k_A_C', '3q0s_A_B', '1gax_A_C', '1gax_B_D', '6fpx_A_B', '6fpx_C_D', '1qrt_A_B', '5wt3_A_C', '5bzv_A_B', '5bym_A_C', '1ec6_B_C', '2rd2_A_B', '4tv0_A_B', '1ffy_A_T', '1qrs_A_B', '5yyn_A_B', '1u0b_B_A', '5bzu_A_B', '5bz5_A_B', '1euy_A_B', '5wt1_A_C', '5wt1_B_F', '3ktw_A_C', '3ktw_B_D', '5tf6_A_B', '5tf6_C_D', '1s03_H_A', '1s03_G_B', '3r9x_A_C', '1fxl_A_B', '6dtd_A_C', '4jxz_A_B', '6i3p_C_G', '2i82_A_E', '2i82_B_F', '2i82_D_H', '5i9h_A_B', '1n77_A_C', '1n77_B_D', '5dea_B_A', '1qu3_A_T', '6du5_A_B', '5de5_B_A', '5de5_D_C', '1qa6_B_D', '3akz_C_G', '6ifo_A_C', '6ifo_B_D', '5ng6_A_B', '5ng6_C_D', '5ng6_E_F', '5ng6_G_H', '4jxx_A_B', '6du4_A_B', '1qu2_A_T', '2zzm_A_B', '2zuf_A_B', '1o0b_A_B', '1vfg_B_D', '5npm_A_B', '1o0c_A_B', '1hc8_A_C', '2czj_C_D', '1mfq_B_A', '2vod_A_C', '2zxu_A_C', '2zxu_B_D', '5js1_A_B', '2zm5_A_C', '2zm5_B_D', '2bs0_C_S', '4jyz_A_B', '6f4h_A_B', '6f4h_C_D', '6f4h_E_F', '5onh_A_B', '5onh_D_E', '2vop_A_B', '1qtq_A_B', '2om7_K_J', '6nma_B_G', '3j5s_F_A', '5zey_C_A', '3j0l_J_1', '1ry1_B_A', '5osg_h_2', '6mcb_A_B', '3deg_H_G', '6mcc_A_B', '2j37_B_A', '5zal_A_C', '6nm9_B_G', '6nm9_D_E', '5vzl_A_B']
bpath = '/Users/tkimura/Desktop/RNP/check_contact/'
idfile = bpath + 'pdbid_hfrac_ltoeq_0.5.csv'

# ----------------------------------------------------------
# preprocess
# ----------------------------------------------------------
# with open(idfile) as f:
# 	for lines in f.readlines():
# 		idlist = lines.replace('\ufeff','').split(',')
# 		break
#
# print(idlist)

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
# zdock
# -R path + 'pdb/1hc8/1hc8_p.pdb'
# -L path + 'pdb/1hc8/1hc8_r.pdb'
# -O path + 'outs/1hc8.out'
# -N 10000

for id in idlist:
	pdbid = id.split('_')[0]
	pchain = id.split('_')[1]
	rchain = id.split('_')[2]

	# preprocess
	command = 'mark_sur ' + path + 'pdb/' + id + '/' + pdbid + '_p.pdb ' + path + 'pdb/' + id + '/' + id + '_p_m.pdb'
	subprocess.call([command], shell=True)
	command = 'mark_sur ' + path + 'pdb/' + id + '/' + pdbid + '_r.pdb ' + path + 'pdb/' + id + '/' + id + '_r_m.pdb'
	subprocess.call([command], shell=True)
	command = 'zdock -o ' + path + 'outs/' + id + '.out -N 10000 -R ' + path + 'pdb/' + id + '/' + id + '_p_m.pdb -L ' + path + 'pdb/' + id + '/' + id + '_r_m.pdb'
	subprocess.call([command], shell=True)
	print(f'{pdbid} is done')


# This is the README file for release 3.0 of ZDOCK program. ZDOCK is an
# initial stage protein-protein docking program, developed initially by
# Rong Chen and Zhiping Weng in 2002. It optimizes pairwise shape
# complementarity, an interface contact potential called IFACE, and
# electrostatic energies using the Fast Fourier Transform algorithm. Please
# cite "Mintseris J, Pierce B, Wiehe K, Anderson R, Chen R, and Weng Z.
# Integrating Statistical Pair Potentials into Protein Complex Prediction.
# Proteins (in press)".
#
# This distribution includes an executable file (zdock) of the ZDOCK program,
# PDB processing file (mark_sur, uniCHARMM, block.pl), and auxiliary files
# (create.pl, create_lig) to create predicted complex structures from a ZDOCK
# output. All executables have been compiled on a 32-bit Linux system. This
# version of ZDOCK 3.0 uses the FFTW3 library to perform its FFTs.
#
# Example:
# mark_sur PDB new_PDB
# zdock -R receptor.pdb -L ligand.pdb -o zdock.out
# create.pl zdock.out
#
# Attention: receptor.pdb, ligand.pdb and create_lig must be in your current
# directory when you try to create all predicted structures using create.pl.
#
# Standard PDB format files must be processed by mark_sur before used as the
# input of ZDOCK. Formatted PDB files of docking benchmark can be downloaded at
# http://zlab.bu.edu/zdock/benchmark.shtml. If you know that some atoms
# are not in the binding site, you can block them by changing their ACE type
# (column 55-56) to 19. This blocking procedure can improve docking
# performance significantly. A blocking script block.pl is included, type
# "block.pl" for usage information.