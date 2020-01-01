# ----------------------------------------------------------
# this code is for plotting wx
#
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
source = '/Users/tkimura/Desktop/RNP/svm/raw_wx_2.5_touch_0.8.csv'
fig = '/Users/tkimura/Desktop/RNP/svm/wx_2.5_touch_0.8.png'

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
wx = pd.read_csv(source)
chart = sn.stripplot(x='id', y='score',data=wx,hue='label')
chart.set_xticklabels(chart.get_xticklabels(), rotation='90')
handles,labels = chart.get_legend_handles_labels()
plt.legend(handles=handles,labels=['dekoi', 'native'])
plt.xlabel(xlabel='')
plt.ylabel(ylabel='SCORE')
plt.savefig(fig, dpi=500, bbox_inches='tight')
plt.show()
plt.close()