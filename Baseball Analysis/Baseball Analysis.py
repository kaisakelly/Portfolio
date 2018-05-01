import pandas as pd
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

### Load Data
all_salaries = pd.read_csv('.../Salaries.csv')
all_team = pd.read_csv('.../Teams.csv')
all_batting = pd.read_csv('...Batting.csv')

### Organize data for Steroid Era Stats
steroid_years = list(range(1990,2004))
steroid = all_batting[['playerID','yearID','teamID','G','AB','R','H', 'HR', 'RBI','BB','2B', '3B', 'HBP', 'SF']]
steroid = steroid[steroid['yearID'].isin(steroid_years)]

steroid = steroid.groupby(['playerID', 'yearID'], as_index = False).sum()
steroid = steroid[steroid['G'] > 100]
steroid = steroid.groupby(['playerID'], as_index = False).sum()
steroid = steroid.drop(columns = ['yearID'])

## Calculate addition baseball stats
steroid['AVG'] = round((steroid['H'] / steroid['AB']),3)
steroid['TB'] = ((steroid['2B']*2) + (steroid['3B']*3) + (steroid['HR']*4) + (steroid['H'] - steroid['HR'] - steroid['3B'] - steroid['2B']))
steroid['OBP'] = round((steroid['H'] + steroid['BB'] + steroid['HBP']) / (steroid['AB'] + steroid['BB'] + steroid['HBP'] + steroid['SF']), 3)
steroid['SLG'] = round((steroid['TB'] / steroid['AB']), 3)
steroid['OPS'] = round((steroid['OBP'] + steroid['SLG']), 3)


## Replace missing data with mean of stat
steroid['OBP'] = steroid['OBP'].replace(np.nan, round(steroid['OBP'].mean(),3))
steroid['SLG'] = steroid['SLG'].replace(np.nan, round(steroid['SLG'].mean(),3))
steroid['OPS'] = steroid['OPS'].replace(np.nan, round(steroid['OPS'].mean(),3))
steroid['HBP'] = steroid['HBP'].replace(np.nan, round(steroid['HBP'].mean(),0))
steroid['SF'] = steroid['SF'].replace(np.nan, round(steroid['SF'].mean(),0))






### Organize data for Modern Era Stats
modern_years = list(range(2004,2017))
modern = all_batting[['playerID','yearID','teamID','G','AB','R','H', 'HR', 'RBI','BB','2B', '3B', 'HBP', 'SF']]
modern = modern[modern['yearID'].isin(modern_years)]

modern = modern.groupby(['playerID', 'yearID'], as_index = False).sum()
modern = modern[modern['G'] > 100]
modern = modern.groupby(['playerID'], as_index = False).sum()
modern = modern.drop(columns = ['yearID'])

## Calculate addition baseball stats
modern['AVG'] = round((modern['H'] / modern['AB']),3)
modern['TB'] = ((modern['2B']*2) + (modern['3B']*3) + (modern['HR']*4) + (modern['H'] - modern['HR'] - modern['3B'] - modern['2B']))
modern['OBP'] = round((modern['H'] + modern['BB'] + modern['HBP']) / (modern['AB'] + modern['BB'] + modern['HBP'] + modern['SF']), 3)
modern['SLG'] = round((modern['TB'] / modern['AB']), 3)
modern['OPS'] = round((modern['OBP'] + modern['SLG']), 3)


## Replace missing data with mean of stat
modern['OBP'] = modern['OBP'].replace(np.nan, round(modern['OBP'].mean(),3))
modern['SLG'] = modern['SLG'].replace(np.nan, round(modern['SLG'].mean(),3))
modern['OPS'] = modern['OPS'].replace(np.nan, round(modern['OPS'].mean(),3))
modern['HBP'] = modern['HBP'].replace(np.nan, round(modern['HBP'].mean(),0))
modern['SF'] = modern['SF'].replace(np.nan, round(modern['SF'].mean(),0))






from bokeh.io import output_file,show,output_notebook,push_notebook
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource,HoverTool,CategoricalColorMapper
from bokeh.layouts import row,column,gridplot,widgetbox
from bokeh.models.widgets import Tabs,Panel,DataTable, DateFormatter, TableColumn,NumberFormatter,Select
from bokeh.models import NumeralTickFormatter





output_notebook()




top_steroid = steroid.sort_values(['HR'], ascending=False)
top_steroid = top_steroid.head(100)


## Set Up Data Sources
source = ColumnDataSource(top_steroid)


hover = HoverTool(
            tooltips = [
                ('Year', '@{yearID}'),
                ('Player','@{playerID}'),
                ('AVG', '@{AVG}{0,0}'),
                ('HR', '@{HR}{0,0}'),
                ('RBI', '@{RBI}{0,0}'),
                ('OBP', '@{OBP}{0,0}'),
                ('SLG', '@{SLG}{0,0}'),
                ('OPS', '@{HR}{0.03}'),
                ])





# Set Up Plots

### Monthly Sales (last 12 months)
plot = figure(plot_width = 900, plot_height = 500, tools = [hover, 'box_zoom', 'pan','reset'], active_drag = 'box_zoom',x_axis_type = 'datetime', title = 'Monthly Sales Last 12 Months')
plot.line(x = 'HR', y = 'RBI', source=source)

plot.title.align = 'center'
plot.title.text_font_size = '20pt'
plot.yaxis[0].formatter = NumeralTickFormatter(format="0,0")

plot.xaxis.axis_label = 'Year'
plot.xaxis.axis_label_standoff = 20
plot.xaxis.axis_label_text_font_style = 'normal'
plot.xaxis.axis_label_text_font_size = '12pt'


plot.yaxis.axis_label = 'Units Sold'
plot.yaxis.axis_label_standoff = 20
plot.yaxis.axis_label_text_font_style = 'normal'
plot.yaxis.axis_label_text_font_size = '12pt'












### Create function that returns scatter plot for a list of baseball stats compared to Runs. Also returns correlation of each stat vs Runs
def runs_analysis(data, statistics):
    for stat in statistics:
        t = 'R'
        x = data[stat]
        y = data[t]
        plt.figure()
        plt.scatter(x,y)
        plt.title('{} vs {}'.format(stat,t))
        plt.ylabel('Runs')
        plt.xlabel('{}'.format(stat))
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), 'r--')
        print('The correlation between average {} and {} is {:0.3f}'.format(stat, t, data.corr()[stat][t]))



stats = ['AVG','OPS','OBP', 'SLG']

runs_analysis(steroid, stats)

runs_analysis(modern, stats)







from sklearn.model_selection import train_test_split
from sklearn import linear_model



### Runs predictions for modern

steroid_sample = steroid[['H', 'HR', 'RBI','AVG','OPS','OBP', 'SLG']]
steroid_runs = np.array(steroid['R'])

steroid_train, steroid_test, steroid_runs_train, steroid_runs_test = train_test_split(steroid_sample, steroid_runs, test_size = 0.2)


# fit a model
lm1 = linear_model.LinearRegression()

model1 = lm1.fit(steroid_train, steroid_runs_train)
predictions1 = lm1.predict(steroid_test)


model1.score(steroid_test, steroid_runs_test)









### Runs predictions for modern

modern_sample = modern[['H', 'HR', 'RBI','AVG','OPS','OBP', 'SLG']]
modern_runs = np.array(modern['R'])

modern_train, modern_test, modern_runs_train, modern_runs_test = train_test_split(modern_sample, modern_runs, test_size = 0.2)


# fit a model
lm2 = linear_model.LinearRegression()

model2 = lm2.fit(modern_train, modern_runs_train)
predictions2 = lm2.predict(modern_test)


model2.score(modern_test, modern_runs_test)









