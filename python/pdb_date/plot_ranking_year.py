# ----------------------------------------------------------
# this code is for plotting ranking and year correlations
#
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
year_list = '/Users/tkimura/Desktop/RNP/pdb_date/year_list.csv'
rankings = '/Users/tkimura/Desktop/RNP/svm/ranking_results_mean_reso_2.5_touch_0.5.csv'

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
df_year = pd.read_csv(year_list)
df_rank = pd.read_csv(rankings)
df_rank['shortid'] = df_rank['id'].str[0:4]
dfm = pd.merge(df_year, df_rank, right_on='shortid', left_on='id', how='outer')
dfm_cld = dfm[np.isfinite(dfm[' rank'])]
print(dfm_cld)
plt.figure()
plt.scatter(dfm_cld['year'], dfm_cld[' rank'])
plt.show()

