# ----------------------------------------------------------
# this code is for running hbplus
# to the output files from ZDock server
# ----------------------------------------------------------
import mpi4py

def run_hbplus(ipath, opath, id_list):
	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------
	import subprocess, os
	# ----------------------------------------------------------
	# functions
	# ----------------------------------------------------------

	# run hbplus
	def runhbplus(in_folder, out_folder, idlist):
		os.chdir(out_folder)
		subprocess.call(['pwd'])
		ifile_list = os.listdir(in_folder)
		ofile_list = os.listdir(out_folder)
		if '3q0n_B_D' in in_folder:
			print(in_folder)
		for files in ifile_list:
			# complex.5.cleaned.pdb >> complex.5.cleaned.hb2
			if '.DS' in files or 'hb2' in files:
				continue
			elif 'cleaned.pdb' in files: # zdock output was cleaned for hbplus
				if files.replace('pdb', 'hb2') not in ofile_list:
					subprocess.call(['hbplus', in_folder + files])
			else:
				pass


	# adjust for environment
	def pre_hbplus(idlist):
		print(idlist)
		for id in idlist:
			if len(id) == 4:
				continue
			if not os.path.exists(opath + id):
				os.mkdir(opath + id)
			if len(os.listdir(opath + id)) > 3580:
				print('skip ' + id)
				continue
			else:
				print('running ' + id)
				runhbplus(ipath + id + '/', opath + id + '/', idlist)

	pre_hbplus(id_list)

poses = '/Users/tkimura/Desktop/t3_mnt/zdock/poses/'
hb2 = '/Users/tkimura/Desktop/RNP/zdock/hb2/'

# ----------------------------------------------------------
# main
# ----------------------------------------------------------

# prepare mpi
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

alllist = ['5on3_A_B', '5on3_D_E', '5wqe_A_B', '2iz9_A_R', '2iz9_C_S', '2b2e_C_S', '2bq5_C_S', '5wea_A_B',
		   '4aq7_A_B', '4aq7_D_E', '2b2d_C_S', '4pkd_B_V', '1zho_E_F', '5on2_A_B', '5on2_D_E', '4prf_A_B',
		   '2cv2_A_C', '2cv2_B_D', '2xlj_A_B', '2det_A_C', '1b7f_A_P', '2izm_C_S', '3epk_A_E', '3epk_B_F',
		   '5vw1_A_C', '2ab4_A_B', '1zjw_A_B', '5z9x_A_R', '3sn2_A_B', '5w1i_A_B', '5w1i_C_D', '5w1h_A_B',
		   '2yjy_A_C', '2yjy_B_D', '5u34_A_B', '4jvh_A_D', '1n78_A_C', '1n78_B_D', '5xbl_A_B', '4pr6_A_B',
		   '3snp_A_C', '3snp_B_D', '1lng_A_B', '3foz_A_C', '3foz_B_D', '6h9i_B_E', '5vm9_A_B', '5vm9_C_D',
		   '2dxi_A_C', '2dxi_B_D', '1y39_A_C', '1y39_B_D', '4zt9_A_B', '4zt9_C_D', '2re8_A_B', '1gtr_A_B',
		   '3t5q_E_F', '3t5q_K_L', '1gts_A_B', '3q0n_B_D', '5wtk_A_B', '3qjj_A_Q', '3qjj_B_R', '6oon_A_B',
		   '4n0t_A_B', '2oih_A_B', '1cvj_A_M', '1cvj_B_N', '1cvj_E_Q', '1cvj_F_R', '1cvj_G_S', '5wwr_A_C',
		   '5wwr_B_D', '3am1_A_B', '3q0l_B_D', '3q0m_A_C', '3q0m_B_D', '5b63_A_B', '5wws_A_C', '5wws_B_D',
		   '2db3_A_E', '1ob5_A_B', '3k4e_A_B', '3k4e_C_D', '3k4e_E_F', '4pmw_A_C', '4pmw_B_D', '5d6g_A_0',
		   '3amu_A_B', '6gc5_A_E', '5wzg_A_B', '1ivs_A_C', '1ivs_B_D', '3amt_A_B', '1vc6_A_B', '2vpl_C_D',
		   '1ob2_A_B', '6aay_A_B', '2hw8_A_B', '1euq_A_B', '5wwt_A_C', '5wwt_B_D', '2y8w_A_B', '6iv8_A_B',
		   '6iv8_C_D', '6iv9_A_B', '2pjp_A_B', '5wlh_A_B', '4olb_A_B', '1g59_A_B', '1g59_C_D', '4f3t_A_R',
		   '5wty_B_D', '6aax_C_D', '4b3g_A_G', '3wqy_A_C', '1m8y_B_D', '5f5f_G_H', '3q0q_A_B', '4zt0_A_B',
		   '4zt0_C_D', '4tyy_A_B', '5wzh_A_B', '5w6v_A_R', '5bz1_A_B', '5wzi_A_B', '3q0p_B_D', '6qic_D_H',
		   '5msf_A_R', '1mms_A_C', '1mms_B_D', '1m8x_B_D', '3k49_A_B', '3k49_C_D', '3k49_E_F', '1qru_A_B',
		   '5ah5_A_C', '5ah5_B_D', '1drz_A_B', '1e7k_A_C', '3q0s_A_B', '1gax_A_C', '1gax_B_D', '6fpx_A_B',
		   '6fpx_C_D', '1qrt_A_B', '5wt3_A_C', '5bzv_A_B', '5bym_A_C', '1ec6_B_C', '2rd2_A_B', '4tv0_A_B',
		   '1ffy_A_T', '1qrs_A_B', '5yyn_A_B', '1u0b_B_A', '5bzu_A_B', '5bz5_A_B', '1euy_A_B', '5wt1_A_C',
		   '5wt1_B_F', '3ktw_A_C', '3ktw_B_D', '5tf6_A_B', '5tf6_C_D', '1s03_H_A', '1s03_G_B', '3r9x_A_C',
		   '1fxl_A_B', '6dtd_A_C', '4jxz_A_B', '6i3p_C_G', '2i82_A_E', '2i82_B_F', '2i82_D_H', '5i9h_A_B',
		   '1n77_A_C', '1n77_B_D', '5dea_B_A', '1qu3_A_T', '6du5_A_B', '5de5_B_A', '5de5_D_C', '1qa6_B_D',
		   '3akz_C_G', '6ifo_A_C', '6ifo_B_D', '5ng6_A_B', '5ng6_C_D', '5ng6_E_F', '5ng6_G_H', '4jxx_A_B',
		   '6du4_A_B', '1qu2_A_T', '2zzm_A_B', '2zuf_A_B', '1o0b_A_B', '1vfg_B_D', '5npm_A_B', '1o0c_A_B',
		   '1hc8_A_C', '2czj_C_D', '1mfq_B_A', '2vod_A_C', '2zxu_A_C', '2zxu_B_D', '5js1_A_B', '2zm5_A_C',
		   '2zm5_B_D', '2bs0_C_S', '4jyz_A_B', '6f4h_A_B', '6f4h_C_D', '6f4h_E_F', '5onh_A_B', '5onh_D_E',
		   '2vop_A_B', '1qtq_A_B', '2om7_K_J', '6nma_B_G', '3j5s_F_A', '5zey_C_A', '3j0l_J_1', '1ry1_B_A',
		   '5osg_h_2', '6mcb_A_B', '3deg_H_G', '6mcc_A_B', '2j37_B_A', '5zal_A_C', '6nm9_B_G', '6nm9_D_E',
		   '5vzl_A_B']

for i in range(0, 7):
	if str(rank) == str(i):
		n_from = 42 * i
		n_to = 42 * (i + 1)
		id_list = alllist[n_from: n_to]

run_hbplus(poses, hb2, id_list)
