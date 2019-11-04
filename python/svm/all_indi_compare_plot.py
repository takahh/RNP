# ----------------------------------------------------------
# this code is for searching best angles from the results
# of ranges of angles
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
infile = '/Users/tkimura/Desktop/RNP/svm/ranking_results_mean.csv'
df_svm = pd.read_csv(infile)
print(df_svm.columns)

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------

angle_set_list = []
print(df_svm.columns)
plt.figure()
plt.gca().invert_yaxis()
# plt.plot(df_svm[' rank'])
# plt.plot(df_svm[' svm_rank'])
x= df_svm[' svm_rank'].index
y = df_svm[' svm_rank'].values
plt.scatter(x, y, s=9)
x= df_svm[' rank'].index
y = df_svm[' rank'].values
plt.scatter(x, y, s=9)
# plt.scatter(df_svm[' svm_rank'])
plt.ylabel('rank')
plt.xlabel('pair')
plt.gca().legend(('individual', 'common'))
plt.text(-10, -270, 'average: ' + str(df_svm[' rank'].values.mean()))
plt.show()