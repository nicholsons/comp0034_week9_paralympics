# Helper functions for creating the charts in the activities
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pathlib import Path

EVENT_DATA_FILEPATH = Path(__file__).parent.parent.joinpath('data', 'paralympics.csv')
MEDALS_DATA_FILEPATH = Path(__file__).parent.parent.joinpath('data', 'all_medals.csv')


def line_chart_over_time(chart_type):
    """
    Creates a line chart showing change in the number of the given parameter in the summer and winter paralympics over
    time. Options are 'EVENTS', 'SPORTS', 'COUNTRIES', 'PARTICIPANTS'

    :return: Plotly Express line chart
    """
    cols = ['REF', 'TYPE', 'YEAR', 'LOCATION', 'EVENTS', 'SPORTS', 'COUNTRIES', 'PARTICIPANTS']
    df_events = pd.read_csv(EVENT_DATA_FILEPATH, usecols=cols)
    title_text = f"Has the number of {chart_type.lower()} changed over time?"
    fig_line = px.line(df_events,
                       x='YEAR',
                       y=chart_type,
                       color='TYPE',
                       text='YEAR',
                       title=title_text,
                       labels={'YEAR': '', chart_type: '', 'TYPE': ''},
                       template="simple_white"
                       )

    fig_line.update_xaxes(showticklabels=False, ticklen=0)
    fig_line.update_traces(textposition="bottom right")

    return fig_line


def stacked_bar_gender(event_type):
    """
    Creates a stacked bar chart showing change in the number of sports in the summer and winter paralympics
    over time
    An example for exercise 2.

    :type event_type: str Winter or Summer
    :return: Plotly Express bar chart
    """
    cols = ['TYPE', 'YEAR', 'LOCATION', 'MALE', 'FEMALE', 'PARTICIPANTS']
    df_events = pd.read_csv(EVENT_DATA_FILEPATH, usecols=cols)
    # Drop Rome as there is no male/female data
    df_events.drop([0], inplace=True, )
    df_events.reset_index(drop=True)
    # Add new columns that each contain the result of calculating the % of male and female participants
    df_events['M%'] = df_events['MALE'] / df_events['PARTICIPANTS']
    df_events['F%'] = df_events['FEMALE'] / df_events['PARTICIPANTS']
    # Sort the values by Type and Year
    df_events.sort_values(['TYPE', 'YEAR'], ascending=(True, True), inplace=True)
    # Create a new column that combines Location and Year to use as the x-axis
    df_events['xlabel'] = df_events['LOCATION'] + ' ' + df_events['YEAR'].astype(str)
    # Create the stacked bar plot of the % for male and female
    df_events = df_events.loc[df_events['TYPE'] == event_type]
    fig = px.bar(df_events,
                 x='xlabel',
                 y=['M%', 'F%'],
                 title=event_type + ' paralympics',
                 labels={'xlabel': '', 'value': '', 'variable': ''},
                 color_discrete_map={'M%': 'blue', 'F%': 'magenta'},
                 template="simple_white"
                 )
    fig.update_xaxes(ticklen=0)
    return fig


def get_country_results(NOC_code):
    """
    Adds the summer/winter event_type column to the medals' data for a specified country and returns the merged data
    as a dataframe.
    :param NOC_code: NOC three digit country code
    :return: DataFrame with the medal data for all years for the specified country
    """
    df = pd.read_csv(MEDALS_DATA_FILEPATH)
    df_event = pd.read_csv(EVENT_DATA_FILEPATH, usecols=['TYPE', 'MERGE_COL'])
    df_merged = df.merge(df_event, how='left', left_on='location', right_on='MERGE_COL')
    df_sorted = df_merged.sort_values(by=['NPC', 'year'])
    df_country = df_sorted.loc[df_sorted['NPC'] == NOC_code]
    df_country['location-year'] = df_country['location'] + ' ' + df_country['year'].astype(str)
    return df_country


def scatter_mapbox_para_locations(mapbox_type):
    """
    Creates a scatter mapbox of the paralympic locations using either Open Street Map or USGS mapbox in Plotly
    Express as neither requires a token.
    :type mapbox_type: str either OSM for OpenStreetMap or USGS
    :return: Plotly Express scatter mapbox figure
    """
    valid = {'OSM', 'USGS'}
    if mapbox_type not in valid:
        raise ValueError("Mapbox type must be one of %r." % valid)
    df_locations = pd.read_csv(EVENT_DATA_FILEPATH)
    fig = px.scatter_mapbox(df_locations,
                            lat='LAT',
                            lon='LON',
                            labels={'YEAR': 'Year', 'TYPE': 'Event type'},
                            hover_name='LOCATION',
                            hover_data={
                                'LAT': False,
                                'LON': False,
                                'LOCATION': False,
                                'YEAR': True,
                                'TYPE': True
                            },
                            color_discrete_sequence=['fuchsia'],
                            zoom=1)
    if mapbox_type == 'OSM':
        fig.update_layout(mapbox_style='open-street-map')
    else:
        fig.update_layout(
            mapbox_style='white-bg',
            mapbox_layers=[
                {
                    'below': 'traces',
                    'sourcetype': 'raster',
                    'sourceattribution': "United States Geological Survey",
                    'source': [
                        "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{"
                        "y}/{x}"
                    ]
                }
            ])

    fig.update_layout(margin={"r": 5, "t": 5, "l": 5, "b": 5})
    fig.update_traces(marker_size=20)

    return fig


def get_event_highlights(location, year):
    cols = ['LOCATION', 'YEAR', 'HIGHLIGHTS']
    dtypes = {'YEAR': 'int'}
    df_highlights = pd.read_csv(EVENT_DATA_FILEPATH, usecols=cols, dtype=dtypes)
    highlight = df_highlights[(df_highlights['LOCATION'] == location) & (df_highlights['YEAR'] == year)]
    highlight_text = highlight.iloc[0, 2]
    return highlight_text


def table_top_ten_gold_table(df):
    fig = go.Figure(data=[go.Table(
        columnorder=['Country', 'Gold'],
        header=dict(values=list(df.columns),
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=[df.Country, df['Gold']],
                   fill_color='white',
                   align='left'))
    ])
    return fig


def top_ten_gold_data():
    """
        Get the data for the top 10 countries who have won the most medals since 1960
        :return: dataframe
        """
    cols = ['Country', 'Gold']
    df_gold = pd.read_csv(MEDALS_DATA_FILEPATH, usecols=cols)
    df_gold = df_gold.groupby(by='Country', as_index=False).sum()
    df_gold = df_gold.sort_values(by='Gold', ascending=False)
    df_gold_ten = df_gold[0:10]
    return df_gold_ten


def get_medals_table_data(location, year):
    """
    Given a specific paralympic location and year, get the data for the medal results.
    :return: data frane
    """
    df_medals = pd.read_csv(MEDALS_DATA_FILEPATH)
    df_medals_event = df_medals[(df_medals['Event'] == location) & (df_medals['Year'] == year)]
    return df_medals_event
