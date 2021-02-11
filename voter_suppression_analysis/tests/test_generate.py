''' CODE TO TEST DASHBOARD GENERATING FUNCTIONALITY '''

import os

from pathlib import Path

import altair as alt

from voter_suppression_analysis.generate import \
    generate_map, generate_chart, generate_html

from voter_suppression_analysis.processing import \
    combine_age_data, combine_sexrace_data, \
    homogenize_age_data, homogenize_sexrace_data


# useful file locations
CWD = Path(__file__).parent
data_path = os.path.join('..', 'data')
figures_path = os.path.join('..', 'figures')

#OUTPUT_FILE_PATH = str(CWD / '../figures/test_dashboard.html')
OUTPUT_FILE_PATH = os.path.join(CWD, figures_path, 'test_dashboard.html')
#EXAMPLE_DIR_AGE = str(CWD / '../*data*/*samples*/*example_age_folder*/*')
EXAMPLE_DIR_AGE = os.path.join(CWD, data_path, 'samples', 'example_age_folder', '*.csv')
#EXAMPLE_DIR_SEX = str(CWD / '../*data*/*samples*/*example_sex_folder*/*')
EXAMPLE_DIR_SEX = os.path.join(CWD, data_path, 'samples', 'example_sex_folder', '*.csv')
#EXAMPLE_FILE_LAW = str(CWD / '../data/samples/law_01.csv')
EXAMPLE_FILE_LAW = os.path.join(CWD, data_path, 'samples', 'law_01.csv')

# anticipated object types of individual viz pieces
EXPECTED_MAP_TYPE = alt.vegalite.v4.api.Chart
EXPECTED_CHART_TYPE = alt.vegalite.v4.api.VConcatChart

# making test DataFrames
DF_AGE = combine_age_data(EXAMPLE_DIR_AGE, EXAMPLE_FILE_LAW)
DF_AGE = homogenize_age_data(DF_AGE)

DF_SEX = combine_sexrace_data(EXAMPLE_DIR_SEX, EXAMPLE_FILE_LAW)
DF_SEX = homogenize_sexrace_data(DF_SEX)


def test_generate_map():
    '''
    Test generate_map(). Note that attributes for all Altair objects were
    set manually, value-testing them is hence redundant and fruitless.
    '''

    # smoke test
    map_obj = generate_map(
        DF_AGE,
        map_type='Percent Voted',
        map_title='X'
    )

    # type check
    assert isinstance(map_obj, EXPECTED_MAP_TYPE)


def test_generate_chart():
    '''
    Test generate_chart(). Again, attribute value-tests are excluded.
    '''

    # smoke test
    chart = generate_chart(
        df_in=DF_SEX,
        x='Percent Registered:Q',
        y='Percent Voted:Q',
        x_lbl='% Registered',
        y_lbl='% Voted',
        title='Demographics',
        clr_setting='restrictive_id_laws:N',
        chart_type='sexrace'
    )

    # type check
    assert isinstance(chart, EXPECTED_CHART_TYPE)


def test_generate_html():
    '''
    Test generate_html(). Note this function does not return a value.
    '''

    # smoke test
    generate_html(DF_AGE, DF_SEX, OUTPUT_FILE_PATH)

    # check if file exists at expected location, is non empty
    file = Path(OUTPUT_FILE_PATH)
    assert file.is_file()
    assert file.stat().st_size != 0
