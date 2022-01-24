import json

from dash import Output, Input

import paralympics_app.paralympic_dash_app.create_charts as cc


def register_callbacks(dash_app):
    """ Create the callbacks for a Plotly Dash dash_app. """

    @dash_app.callback(
        Output(component_id='line-chart-time', component_property='figure'),
        Input(component_id='type-dropdown', component_property='value')
    )
    def update_output_div(event_variable):
        """
        Call back for updating the line chart when the type of data to display is changed.

        :param event_variable: one of the following which are columns in the paralympics dataset ['EVENTS', 'SPORTS',
        'COUNTRIES', 'PARTICIPANTS']
        :return: plotly.px.Figure The line chart representing the chosen variable
        """
        fig_line_time = cc.line_chart_over_time(event_variable)
        return fig_line_time

    @dash_app.callback(
        [Output("stacked-bar-gender-win", "style"),
         Output("stacked-bar-gender-sum", "style")],
        Input("mf-ratio-checklist", "value"),
    )
    def show_hide_ratio_charts(selected_types):
        """
        Callback to display or hide the winter and summer male:female ratio bar charts depending on the checkbox values.

        :param selected_types: List of checkbox values for the event type(s) (Winter and/or Summer)
        :return: a list of values, the first sets visibility for the Winter chart, the second for the Summer
        """
        # Default to hiding both
        win_show = {'display': 'none'}
        sum_show = {'display': 'none'}
        if 'Winter' in selected_types:
            win_show = {'display': 'block'}
        if 'Summer' in selected_types:
            sum_show = {'display': 'block'}
        return [win_show, sum_show]

    @dash_app.callback(
        Output('highlight-text', 'children'),
        Input('scatter-mapbox-osm', 'hoverData'))
    def display_hover_data(hoverData):
        """
        Callback to find the highlight text for a given paralympic event when it is hovered over on the map.

        :param hoverData: he `hoverData` from the Input
        :return: text for the paragraph with id='highlight-text'
        """
        location = json.dumps(hoverData['points'][0]['customdata'][2], indent=2)
        location = location.strip('"')
        year = json.dumps(hoverData['points'][0]['customdata'][3], indent=2)
        year = int(year)
        highlight_text = cc.get_event_highlights(location, year)
        return highlight_text
