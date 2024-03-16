'''
https://data-analytics.fun/2021/06/08/plotly-data-visualization-1/
'''

import plotly.graph_objects as go

# -----------


x = ['1', '2', '3']
y = [50, 20, 30]

data = go.Bar(x=x, y=y)
	
go.Figure(data).show()



# -----------


from sklearn.datasets import load_iris

iris = load_iris()
x1 = iris['data'][:50, 0]
y1 = iris['data'][:50, 1]
x2 = iris['data'][50: 100, 0]
y2 = iris['data'][50:100, 1]

data1 = go.Scatter(x=x1,
                   y=y1,
                   mode='markers',
                   name='setosa'
                   )
data2 = go.Scatter(x=x2,
                   y=y2,
                   mode='markers',
                   name='versicolor')
go.Figure([data1, data2]).show()

# -----------


import plotly.express as px

df = px.data.iris()

fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
fig.show()


# -----------

