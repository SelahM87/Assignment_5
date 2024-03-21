from dash import Dash, html, dcc 
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px



#load data set
df = pd.read_csv("gdp_pcap.csv")
# pivot  data frame into long 
df_long = df.melt(id_vars=['country'], value_vars=[
    '1800', '1801', '1802', '1803', '1804', '1805', '1806', '1807', '1808', '1809',
    '1810', '1811', '1812', '1813', '1814', '1815', '1816', '1817', '1818', '1819',
    '1820', '1821', '1822', '1823', '1824', '1825', '1826', '1827', '1828', '1829',
    '1830', '1831', '1832', '1833', '1834', '1835', '1836', '1837', '1838', '1839',
    '1840', '1841', '1842', '1843', '1844', '1845', '1846', '1847', '1848', '1849',
    '1850', '1851', '1852', '1853', '1854', '1855', '1856', '1857', '1858', '1859',
    '1860', '1861', '1862', '1863', '1864', '1865', '1866', '1867', '1868', '1869',
    '1870', '1871', '1872', '1873', '1874', '1875', '1876', '1877', '1878', '1879',
    '1880', '1882', '1884', '1886', '1893', '1894'
], var_name='year', value_name='gdpPercap')
#check what dataframe looks like 
df_long.head()



stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # load the CSS stylesheet

# initialize app
app = Dash(__name__, external_stylesheets=stylesheets)

server = app.server



# convert the str to int data type in the years column  
df_long['year'] = df_long['year'].astype(int)
# calulate minimuim year and maximuim year 
min_year = df_long['year'].min()
max_year = df_long['year'].max()

#Creates markers on slider so they show the values and not 2k
slider_marks = {year: str(year) for year in range(min_year, max_year + 1, 10)}

# creates the description about the dashboard 
description = """
 GDP per capita data for various countries over-time period of 1800s.  
 Please select  one or more countries the default is Angola. Adjust the years displayed on the graph. The graph below shows the GDP 
per capita trend for the selected countries over-time.
"""

app.layout = html.Div([
    #Title and description 
    html.H1("GDP per Capita Visualization"),   
    html.P(description),  
   # dropdown for country 
    html.Div([
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': country, 'value': country} for country in df_long['country'].unique()],
            multi=True,
            # Place holder
            placeholder='Select Country(s)',  
            className="six columns"
        ),
        # the slider 
        html.Div([
            dcc.RangeSlider(
                id='year_slider',
                min=min_year,
                max=max_year,
                value=[min_year, max_year], 
                marks=slider_marks,
                className="six columns"
            ),
        ], className="row"),

        html.Div([
            dcc.Graph(id='line_chart', config={'displayModeBar': True })
        ], className="row"),
    ])
])


@app.callback(
    Output('line_chart', 'figure'),
    [Input('dropdown', 'value'),
     Input('year_slider', 'value')])
def update_figure(selected_countries, selected_year):
    
    #default value found on slack
    selected_countries = selected_countries or ['Angola']
    
# put df in correct  range
    filtered_df = df_long[(df_long['country'].isin(selected_countries)) &
                          (df_long['year'] >= selected_year[0]) &
                          (df_long['year'] <= selected_year[1])]
    
    # Create line graph 
    fig = px.line(filtered_df, 
                  x="year",
                  y="gdpPercap", 
                  color="country")
    
    # Update graph layout with title and axis labels
    fig.update_layout(
        title="GDP per Capita Over Time",
        xaxis_title="Year",
        yaxis_title="GDP per Capita",
        transition_duration=500
    )
    
    return fig



if __name__ == "__main__":
 app.run_server(debug=True)