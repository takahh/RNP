import plotly.plotly as py
import plotly.graph_objs as go

def piplot(source_counts):
    sources_pie = go.Pie(labels=source_counts.index,
                         values=source_counts,
                         marker=dict(line=dict(color='#FFF', width=2)),
                         domain={'x': [0.0, .4], 'y': [0.0, 1]},
    showlegend=False, name='Sources of Pie', textinfo='label+percent')
    layout = go.Layout(height = 600,
                       width = 1000,
                       autosize = False,
                       title = 'Pie Consumption Patterns in the United States')
    fig = go.Figure(data = sources_pie, layout = layout)
    py.iplot(fig, filename='basic_pie_chart')


