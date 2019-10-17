# ----------------------------------------------------------
# this code is for running hbplus
# to the output files from ZDock server
# ----------------------------------------------------------
import mpi4py

def run_hbplus(ipath, opath):
	# ----------------------------------------------------------
	# import
	# ----------------------------------------------------------
	import subprocess, os
	all_list = ["1qa6_A_C", "5a7a_A_R", "2go5_6_9", "3j46_5_4", "6i2n_D_U", "5y88_W_x", "3iz4_B_A", "4uft_B_R", "3j0q_k_9", "6iv6_A_G", "3j0d_G_A", "3iyr_B_A", "5z9w_A_R", "2iz9_A_R", "4jvh_A_D", "1zdj_A_R", "1y39_A_C", "6aax_C_D", "2vop_A_B", "6mcc_A_B", "6nm9_D_E", "3bx3_A_C", "4prf_A_B", "3epk_A_E", "5w1i_C_D", "4zt9_A_B", "5o1z_A_B", "5wwr_B_D", "2db3_A_E", "6gc5_A_E", "3b0v_C_A", "3rtj_A_D", "1euq_A_B", "5wwt_A_C", "4tuw_A_C", "5msf_A_R", "1gax_A_C", "5bym_A_C", "2rd2_A_B", "2bny_C_S", "3g0h_A_E", "5aka_5_7", "4aq7_D_E", "3eph_A_E", "3epk_B_F", "2yjy_B_D", "5vm9_C_D", "3q0n_B_D", "5wws_A_C", "3k4e_A_B", "1fka_H_A", "4zt0_C_D", "4tux_A_C", "4tz0_A_B", "6f4h_E_F", "3j46_T_2", "2ct8_A_C", "2dxi_A_C", "5bte_A_C", "3t5q_E_F", "3t5q_I_J", "1cvj_G_S", "6iv8_C_D", "1wpu_A_C", "1g59_C_D", "5hc9_A_C", "1p6v_A_B", "1vby_A_B", "6cf2_A_G", "5ng6_C_D", "4oi1_A_B", "5t8y_B_X", "2iz9_C_S", "1vq4_N_9", "1jbt_B_D", "3q0n_A_C", "1cvj_C_O", "3q0m_B_D", "3g6e_N_9", "4tuw_B_D", "4b3g_B_H", "1yit_N_9", "2x1a_A_B", "1yi2_N_9", "1uvn_E_F", "3zgz_D_E", "2i82_C_G", "5gxi_A_B", "2otj_N_9", "2zzm_A_B", "5o58_A_B", "1xpr_A_G", "1uvi_A_D", "2otl_N_9", "3er9_B_D", "3j0q_J_7"]
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


	# ----------------------------------------------------------
	# main
	# ----------------------------------------------------------

	# prepare mpi
	from mpi4py import MPI

	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()

	if rank == 0:
		id_list = all_list[0:14]
	if rank == 1:
		id_list = all_list[14:28]
	if rank == 2:
		id_list = all_list[28:42]
	if rank == 3:
		id_list = all_list[42:56]
	if rank == 4:
		id_list = all_list[56:70]
	if rank == 5:
		id_list = all_list[70:84]
	if rank == 6:
		id_list = all_list[84:96]

	pre_hbplus(id_list)

poses = '/Users/tkimura/Desktop/t3_mnt/zdock/poses/'
hb2 = '/Users/tkimura/Desktop/RNP/zdock/hb2/'

run_hbplus(poses, hb2)
