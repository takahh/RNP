# ----------------------------------------------------------
# this code is for running the last parts of svm
# depending on all_chains and resolution
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
from python.svm.search_best_angles import search_best_angles
# from python.svm.study_search_best_angle import search_best_angles
from python.svm.apply_mean_w import apply_mean
from python.svm.all_indi_compare_plot import indi_common_plot

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
reso_limit_list = [2.5, 3.0]
contact_limit_list = [0.5, 1.0, 1.5, 2.0]
# contact_limit_list = [0.5, 1, 1.5, 2.0]
# reso_limit_list = [3.5]
# contact_limit_list = [0.5]
remove_id_list = ['2bs0_C_S']
# remove_id_list = []
exp = 'xray'

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
for reso_limit in reso_limit_list:
	for contact_limit in contact_limit_list:
		search_best_angles(reso_limit, contact_limit, remove_id_list, exp)
		apply_mean(reso_limit, contact_limit, remove_id_list, exp)
		indi_common_plot(reso_limit, contact_limit)
