####################################################
# constants
####################################################
path = '/Users/tkimura/Desktop/RNP/check_contact/'
xray_summary = path + 'xray_contacts_summary.csv'
EM_summary = path + 'EM_contacts_summary.csv'

####################################################
# import
####################################################
import pandas as pd
from matplotlib import pyplot as plt
from chart_studio import plotly as py
import plotly.graph_objs as go

####################################################
# histogram
####################################################
def plot_hist(csvfile, name):
	df = pd.read_csv(csvfile)
	print(df.head(10))
	for column in df.columns:
		if 'ppchain' in column or 'rrchain' in column or 'prchain' in column:
			fig = plt.figure()
			df[column].plot.hist(bins=39, range=(1,40))
			plt.title(f'{column}-{name}')
			plt.show()
			fig.savefig(f'{column}-{name}.png')

# plot_hist(xray_summary, 'xray')
# plot_hist(EM_summary, 'EM')


####################################################
# pie chart (maybe this is better)
####################################################
def plot_pie(csvfile, name):
	df = pd.read_csv(csvfile)
	for column in df.columns:
		if 'ppchain' in column or 'rrchain' in column or 'prchain' in column:
			fig = plt.figure()
			label_num = len(df[column].value_counts().sort_index()[1:])
			plt.title(f'{column}-{name}')
			labellist = []
			for i in range(0, label_num):
				if i <=3:
					labellist.append(df[column].value_counts().sort_index().index[i+1])
				else:
					labellist.append('')
			print(labellist)
			df[column].value_counts()[1:].plot.pie(fontsize=17, labels=labellist)
			plt.legend(df[column].value_counts().sort_index()[1:].index,loc=5, ncol=2, bbox_to_anchor=(-0, 1))
			plt.show()
			fig.savefig(f'{column}-{name}.png')

####################################################
# pie chart by plotly
####################################################
def piplot(csvfile, name):
	df = pd.read_csv(csvfile)
	for column in df.columns:
		# if 'ppchain' in column or 'rrchain' in column or 'prchain' in column:
		if 'ppchain' in column:
			source_counts = df[column].value_counts()[1:]
			sources_pie = go.Pie(labels=source_counts.index,
								values=source_counts,
								# marker=dict(line=dict(color='#FFF', width=2)),
								# domain={'x': [0.0, .4], 'y': [0.0, 1]},
								# showlegend=False,
								# name='Sources of Pie',
								# textinfo='label+percent'
								 )
			layout = go.Layout(height = 600,
								width = 1000,
								autosize = False,
								title = 'Pie Consumption Patterns in the United States')
			fig = go.Figure(data = sources_pie, layout = layout)
			py.iplot(fig, filename=name)


# piplot(xray_summary, 'xray')

plot_pie(xray_summary, 'xray')
# plot_pie(EM_summary, 'EM')

