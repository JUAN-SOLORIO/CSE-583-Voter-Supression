''' CODE TO GENERATE VISUALIZATIONS '''

import os
import sys

import pandas as pd
import altair as alt
from vega_datasets import data

sys.path.insert(0, os.path.abspath('..'))
from voter_suppression_analysis import processing


# data and visualization locations
data_path = 'data'
#DATA_PATH_SEX = 'data/clean/*_sexrace.csv'
DATA_PATH_SEX = os.path.join(data_path, 'clean', '*_sexrace.csv')
#DATA_PATH_AGE = 'data/clean/*_age.csv'
DATA_PATH_AGE = os.path.join(data_path, 'clean', '*_age.csv')
#DATA_PATH_LAW = 'data/clean/suppression.csv'
DATA_PATH_LAW = os.path.join(data_path, 'clean', 'suppression.csv')
#OUTPUT_FILE_PATH = 'figures/dashboard.html'
OUTPUT_FILE_PATH = os.path.join('figures', 'dashboard.html')

# fixed lists of interactive feature labels
CATEGORIES_AGE = [
    'Total', '18 to 44', '45 to 65', '65+'
]

CATEGORIES_SEX = [
    'Total', 'Male', 'Female', 'White', 'Black',
    'Asian & Pacific Islander', 'Hispanic'
]

# useful constants for mapping
GEOJSON_STATES_URL = ('https://raw.githubusercontent.com/'
                      'vega/vega/master/docs/data/us-10m.json')

MAP_PROJECTION = 'albersUsa'
COLOR_SCHEME = 'yellowgreenblue'

# range for year slider
START_YEAR = 2000
END_YEAR = 2018

# fixed dropdown objects and selection options
DROPDOWN_OBJ_AGE = alt.binding_select(options=CATEGORIES_AGE)
DROPDOWN_OBJ_SEX = alt.binding_select(options=CATEGORIES_SEX)

# accompanying selection options
SELECT_OBJ_AGE = alt.selection_single(
    fields=['Group'],
    bind=DROPDOWN_OBJ_AGE,
    name='Age',
    init={'Group':'Total'}
)

SELECT_OBJ_SEX = alt.selection_single(
    fields=['Group'],
    bind=DROPDOWN_OBJ_SEX,
    name='Demographics',
    init={'Group':'Total'}
)

# slider for year and accompanying selection options
SLIDER = alt.binding_range(
    min=START_YEAR,
    max=END_YEAR,
    step=2,
    name='Election Year'
)

SELECT_OBJ_YR = alt.selection_single(
    name='SelectorName',
    fields=['Year'],
    bind=SLIDER,
    init={'Year':START_YEAR}
)


def generate_map(df_in, map_title, map_type):
    '''
    Generate US map for given voting or registration data.

    Args:
        - df_in: pd.DataFrame, data to be mappd
        - map_type: str, name of column in df_in to map (vote/reg)
        - map_title: str

    Returns:
        - altair.vegalite.v4.api.Chart: complete map visualization
    '''
    df_copy = df_in.copy()

    # establish relevant columns from data
    pivot_columns = ['STATE', 'id', 'Group', 'Year']
    kept_columns = pivot_columns + [map_type]
    year_columns = [str(yr) for yr in range(START_YEAR, END_YEAR+1, 2)]

    # perform pivot
    df_pivot = df_copy[kept_columns].pivot_table(
        index=['id', 'STATE', 'Group'],
        columns='Year',
        values=map_type
    )

    # create map viz-ready DataFrame
    df_map = df_pivot.reset_index()
    df_map.columns = df_map.columns.astype(str)

    # Altair settings for US map
    states = alt.topo_feature(data.us_10m.url, 'states')
    states['url'] = GEOJSON_STATES_URL

    # create and return final map chart object
    map_chart = alt.Chart(states).mark_geoshape(
        stroke='black',
        strokeWidth=0.05
    )

    # map-logistics args
    projection = map_chart.project(type=MAP_PROJECTION)
    scale = alt.Scale(domain=[0.2, .9], scheme=COLOR_SCHEME, type='linear')
    lookup_idxs = df_map.loc[df_map.Group == 'Total']
    lookup_data = alt.LookupData(lookup_idxs, 'id', ['STATE']+year_columns)

    # start manipulating map aesthetic
    transform = projection.transform_lookup(
        lookup='id',
        from_=lookup_data
    )

    transform = transform.transform_fold(
        year_columns,
        as_=['Year', 'Percent']
    )

    transform = transform.transform_calculate(
        Year='parseInt(datum.Year)',
        Percent='isValid(datum.Percent) ? datum.Percent : -1'
    )

    # color and interactivity args
    clr = alt.condition(
        'datum.Percent > 0',
        alt.Color('Percent:Q', scale=scale),
        alt.value('#dbe9f6')
    )

    tool = ['STATE:N', alt.Tooltip('Percent:Q', format='.0%')]

    # final customizations and finish
    encoding = transform.encode(tooltip=tool, color=clr)
    encoding = encoding.add_selection(SELECT_OBJ_YR)
    encoding = encoding.properties(title=map_title, width=415, height=200)
    filtered = encoding.transform_filter(SELECT_OBJ_YR)
    return filtered


def generate_chart(df_in, x, y, x_lbl, y_lbl, title, clr_setting, chart_type):
    '''
    Generates chart visualization of given voting or registration data,
    against legislation data from the same source. Note that specially
    formatted strings follow patterns described in the Altair documentation.

    Args:
        - df_in: pd.DataFrame to be charted
        - x: str, specially formatted name of df_in column for x axis
        - y: str, specially formatted name of df_in column for y axis
        - x_lbl: str, name of x axis
        - y_lbl: str, name of y axis
        - title: str, chart title
        - clr_setting: str, formatted name of df_in column used to color-label
        - chart_type: str, name of df_in column to chart (voting/reg)

    Returns:
        - altair.vegalite.v4.api.VConcatChart: complete chart visualization
    '''

    # set dropdown option based on type of chart to be plotted
    if chart_type == 'age':
        dropdown_box = SELECT_OBJ_AGE
    elif chart_type == 'sexrace':
        dropdown_box = SELECT_OBJ_SEX
    else:
        raise ValueError('Type %s must be age/sexrace.' % chart_type)

    # interval highlighting on charts
    highlight = alt.selection_interval(encodings=['x'])
    color = alt.Color(clr_setting)
    click = alt.selection_multi(encodings=['color'])

    # remove national numbers
    copy = df_in.copy(deep=True)
    copy = copy.loc[copy.STATE != 'NATIONAL']

    # scatter portion
    scatter = alt.Chart().mark_point()

    # scatter portion args
    axis = alt.Axis(format='%')
    scale = alt.Scale(domain=[0.05, 0.96])
    gray_val = alt.value('lightgray')

    x_var = alt.X(x, title=x_lbl, scale=scale, axis=axis)
    y_var = alt.Y(y, title=y_lbl, scale=scale, axis=axis)
    size = alt.Size('Total:Q', title='Total Eligible Voters')
    clr = alt.condition(highlight, clr_setting, gray_val, legend=None)

    tools = [
        alt.Tooltip('STATE:N', title='State'),
        alt.Tooltip('Total:Q', title='Total Eligible Voters'),
        alt.Tooltip('Total Registered:Q', title='# Registered Voters'),
        alt.Tooltip('Total Voted:Q', title='# Voted')
    ]

    # scatter portion interactivity and labels
    scatter = scatter.encode(
        x=x_var,
        y=y_var,
        size=size,
        color=clr,
        tooltip=tools
    )

    scatter = scatter.add_selection(SELECT_OBJ_YR)
    scatter = scatter.transform_filter(SELECT_OBJ_YR)
    scatter = scatter.add_selection(dropdown_box)
    scatter = scatter.transform_filter(dropdown_box)
    scatter = scatter.add_selection(highlight)
    scatter = scatter.transform_filter(click)
    scatter = scatter.properties(title=title, width=400, height=275)

    # bar portion
    bars = alt.Chart().mark_bar()

    # bar portion args
    x_var = alt.X('count()', title='# States with Restrictive Laws')
    y_var = alt.Y(clr_setting, title='Restrictive Laws')
    clr = alt.condition(click, color, alt.value('lightgray'), legend=None)

    # bar portion interactivity and labels
    bars = alt.Chart().mark_bar()
    bars = bars.encode(x=x_var, y=y_var, color=clr)
    bars = bars.transform_filter(highlight)
    bars = bars.transform_filter(SELECT_OBJ_YR)
    bars = bars.transform_filter(dropdown_box)
    bars = bars.properties(width=400, height=80)
    bars = bars.add_selection(click)

    # combine features and finish
    chart = alt.vconcat(scatter, bars, data=copy)
    return chart


def generate_html(df_age, df_sex, output_file_path):
    '''
    Generates HTML file containing dynamic compilation of all required
    figures, given compiled age and sexrace data and a destination.

    Args:
        - df_age: pd.DataFrame, all years of age data (cleaned)
        - df_sex: pd.DataFrame, all years of sexrace data (cleaned)
        - output_file_path: str, location at which to store HTML file

    No return value. HTML file is stored in provided path.
    '''

    # generate maps for voting and registered populations
    map_voted = generate_map(
        df_age,
        map_type='Percent Voted',
        map_title='% Voted'
    )

    map_regis = generate_map(
        df_age,
        map_type='Percent Registered',
        map_title='% Registered'
    )

    # generate scatter-bar chart of turnout + laws data for age, sexrace
    chart_age = generate_chart(
        df_in=df_age,
        x='Percent Registered:Q',
        y='Percent Voted:Q',
        x_lbl='% Registered',
        y_lbl='% Voted',
        title='Age Groups',
        clr_setting='restrictive_id_laws:N',
        chart_type='age'
    )

    chart_sexrace = generate_chart(
        df_in=df_sex,
        x='Percent Registered:Q',
        y='Percent Voted:Q',
        x_lbl='% Registered',
        y_lbl='% Voted',
        title='Demographics',
        clr_setting='restrictive_id_laws:N',
        chart_type='sexrace'
    )

    # combine and write to file, finish
    dashboard = (chart_age | chart_sexrace) | (map_voted & map_regis)
    dashboard.save(output_file_path)
    print('Dashboard generated, location: /%s.' % output_file_path)


if __name__ == '__main__':
    # temporarily suppress warning for deprecated pandas slice function
    pd.options.mode.chained_assignment = None

    # retrieve and process data
    age_data = processing.combine_age_data(DATA_PATH_AGE, DATA_PATH_LAW)
    sex_data = processing.combine_sexrace_data(DATA_PATH_SEX, DATA_PATH_LAW)

    df_age_cleaned = processing.homogenize_age_data(age_data)
    df_sex_cleaned = processing.homogenize_sexrace_data(sex_data)

    # generate output file and finish
    generate_html(df_age_cleaned, df_sex_cleaned, OUTPUT_FILE_PATH)
