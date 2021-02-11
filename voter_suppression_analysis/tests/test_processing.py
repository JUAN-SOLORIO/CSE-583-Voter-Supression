''' CODE TO TEST DATA PROCESSING FUNCTIONALITY '''

import random
import os
import sys
from pathlib import Path

#sys.path.insert(0, os.path.abspath('..'))
from voter_suppression_analysis.processing import \
    get_age_df, get_sexrace_df, \
    combine_age_data, combine_sexrace_data, \
    homogenize_age_data, homogenize_sexrace_data


# useful constants for file locations
CWD = Path(__file__).parent
data_folder = os.path.join('..', 'data')

#EXAMPLE_PATH_AGE = CWD / '../data/samples/age_01.csv'
EXAMPLE_PATH_AGE = os.path.join(CWD, data_folder, 'samples', 'age_01.csv')
#EXAMPLE_PATH_SEX = CWD / '../data/samples/sex_01.csv'
EXAMPLE_PATH_SEX = os.path.join(CWD, data_folder, 'samples', 'sex_01.csv')
#EXAMPLE_PATH_LAW = CWD / '../data/samples/law_01.csv'
EXAMPLE_PATH_LAW = os.path.join(CWD, data_folder, 'samples', 'law_01.csv')

#EXAMPLE_DIR_AGE = str(CWD / '../*data*/*samples*/*example_age_folder*/*')
EXAMPLE_DIR_AGE = os.path.join(CWD, data_folder, 'samples', 'example_age_folder', '*.csv')
#EXAMPLE_DIR_SEX = str(CWD / '../*data*/*samples*/*example_sex_folder*/*')
EXAMPLE_DIR_SEX = os.path.join(CWD, data_folder, 'samples', 'example_sex_folder', '*.csv')

GARBAGE_PATH = str(random.randint(0, 9))

# useful constants for expected column names
EXPECTED_AGE_COLUMNS = [
    'STATE', 'Age', 'Total', 'Total Registered', 'Percent registered (18+)',
    'CI Registered', 'Total Voted', 'Percent voted (18+)', 'CI Voted', 'Year'
]

EXPECTED_SEX_COLUMNS = [
    'STATE', 'Group', 'Population (18+)', 'Total Citizen', 'Percent Citizen',
    'CI Citizen', 'Total Registered', 'Percent Registered (18+)',
    'CI Registered', 'Total Voted', 'Percent Voted (18+)', 'CI Voted', 'Year'
]

# useful constants for expected shapes
FINISHED_LENGTH_AGE = 55

# useful constants for state labels and IDs
STATE_NUMS = [
    1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21,
    22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
    40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56, 0
]

STATE_NAMES = [
    'ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA', 'COLORADO',
    'CONNECTICUT', 'DELAWARE', 'DISTRICT OF COLUMBIA', 'FLORIDA', 'GEORGIA',
    'HAWAII', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS', 'KENTUCKY',
    'LOUISIANA', 'MAINE', 'MARYLAND', 'MASSACHUSETTS', 'MICHIGAN',
    'MINNESOTA', 'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA', 'NEVADA',
    'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK',
    'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA', 'OREGON',
    'PENNSYLVANIA', 'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA',
    'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT', 'VIRGINIA', 'WASHINGTON',
    'WEST VIRGINIA', 'WISCONSIN', 'WYOMING', 'NATIONAL'
]


def test_get_age_df():
    '''
        Test the following conditions for get_age_df():
            - function breaks with invalid filepath
            - resulting dataframe has the right columns
            - resulting df is non empty
            - random punctuation marks have been removed
    '''

    # smoke test
    df_age = get_age_df(EXAMPLE_PATH_AGE)

    # check if invalid file paths break function
    invalid_file_caught = False

    try:
        df_age = get_age_df(GARBAGE_PATH)
    except FileNotFoundError:
        invalid_file_caught = True

    assert invalid_file_caught

    # check resulting df has data
    assert len(df_age) > 0

    # check resulting df has correct columns
    assert all(df_age.columns == EXPECTED_AGE_COLUMNS)

    # check leading punctuation marks have been removed
    assert df_age["Age"][0] == "Total"


def test_get_sexrace_df():
    '''
        Test the following conditions for get_sexrace_df():
            - function breaks with invalid filepath
            - resulting dataframe has right columns
            - resulting df has data
            - random punctuation marks have been removed
    '''

    # smoke test
    df_sex = get_sexrace_df(EXAMPLE_PATH_SEX)

    # check if invalid file paths break function
    invalid_file_caught = False

    try:
        df_sex = get_sexrace_df(GARBAGE_PATH)
    except FileNotFoundError:
        invalid_file_caught = True

    assert invalid_file_caught

    # check resulting df has data
    assert len(df_sex) > 0

    # check resulting df has correct columns
    assert all(df_sex.columns == EXPECTED_SEX_COLUMNS)

    # check punctuation has been removed
    assert df_sex["Group"][0] == "Total"


def test_combine_age_data():
    '''
        Test following conditions for combine_age_data():
            - resulting dataframe has all the data
            - invalid filepath doesn't work
            - legislative data is present
            - NATIONAL label has been substituted for US
    '''

    # smoke test
    df_combined = combine_age_data(EXAMPLE_DIR_AGE, EXAMPLE_PATH_LAW)

    # test dataframe has enough data
    assert len(df_combined) > 0

    # combine_age_data should throw ValueError if no files found to join
    invalid_file_caught = False

    try:
        df_combined = combine_age_data(GARBAGE_PATH)
    except ValueError:
        invalid_file_caught = True

    assert invalid_file_caught

    # check NATIONAL label is in place
    assert df_combined['STATE'][0] == 'NATIONAL'


def test_combine_sexrace_data():
    '''
        Test following conditions for combine_sexrace_data():
            - resulting dataframe has all the data
            - invalid filepath doesn't work
            - legislative data is present
            - NATIONAL label has been substituted for US
    '''

    # smoke test
    df_combined = combine_sexrace_data(EXAMPLE_DIR_SEX, EXAMPLE_PATH_LAW)

    # test dataframe has enough data
    assert len(df_combined) > 0

    # function will throw ValueError if no files found to combine
    invalid_file_caught = False

    try:
        df_combined = combine_age_data(GARBAGE_PATH)
    except ValueError:
        invalid_file_caught = True

    assert invalid_file_caught

    # check NATIONAL label is in place
    assert df_combined['STATE'][0] == 'NATIONAL'


def test_homogenize_age_data():
    '''
        Test conditions for homogenize_age_data():
            - the correct age brackets are present
            - data is in the correct shape
            - state ID's are present
            - state labels are present
    '''

    # smoke test
    df_combined = combine_age_data(EXAMPLE_DIR_AGE, EXAMPLE_PATH_LAW)
    df_standardized = homogenize_age_data(df_combined)

    # test data is in correct shape
    assert len(df_standardized) == FINISHED_LENGTH_AGE

    # test the state IDs and labels are present
    assert any(df_standardized['id'].unique() == STATE_NUMS)
    assert any(df_standardized['STATE'].unique() == STATE_NAMES)


def test_homogenize_sexrace_data():
    '''
        Test conditions for homogenize_age_data():
            - the correct age brackets are present
            - data is in the correct shape
            - state ID's are present
            - state labels are present
    '''

    # smoke test
    df_combined = combine_sexrace_data(EXAMPLE_DIR_SEX, EXAMPLE_PATH_LAW)
    df_standardized = homogenize_sexrace_data(df_combined)

    # test the state IDs and labels are present
    assert any(df_standardized['id'].unique() == STATE_NUMS)
    assert any(df_standardized['STATE'].unique() == STATE_NAMES)
