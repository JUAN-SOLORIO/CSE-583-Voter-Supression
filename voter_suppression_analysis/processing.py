''' CODE TO CLEAN AND STANDARDIZE ALL DATA '''

import glob
import os
import pandas as pd


# filepath expressions for data
data_path = 'data'
#PATH_ALL_AGE = 'data/clean/*_age.csv'
PATH_ALL_AGE = os.path.join(data_path, 'clean', '*_age.csv')
#PATH_ALL_SEX = 'data/clean/*_sexrace.csv'
PATH_ALL_SEX = os.path.join(data_path, 'clean', '*_sexrace.csv')
#PATH_LAWS = 'data/clean/suppression.csv'
PATH_LAWS = os.path.join(data_path, 'clean', 'suppression.csv')

# useful constants for renaming and removing columns
SEX_COLUMNS = [
    'STATE', 'Group', 'Population (18+)', 'Total Citizen', 'Percent Citizen',
    'CI Citizen', 'Total Registered', 'Percent Registered (18+)',
    'CI Registered', 'Total Voted', 'Percent Voted (18+)', 'CI Voted', 'Year'
]

AGE_COLUMNS = [
    'STATE', 'Age', 'Total', 'Total Registered', 'Percent registered (18+)',
    'CI Registered', 'Total Voted', 'Percent voted (18+)', 'CI Voted', 'Year'
]

ORIGINAL_SEX_GROUPS = [
    'Total', 'Male', 'Female', 'N-H White', 'N-H Black', 'API', 'Hispanic',
    'Non-Hispanic White', 'Non-Hispanic Black', 'Asian and Pacific Islander',
    'White non-Hispanic alone', 'Black alone', 'Asian alone',
    'Hispanic (of any race)'
]

NEW_SEX_GROUPS = [
    'Total', 'Male', 'Female', 'White', 'Black', 'Asian & Pacific Islander',
    'Hispanic', 'White', 'Black', 'Asian & Pacific Islander', 'White',
    'Black', 'Asian & Pacific Islander', 'Hispanic'
]

# useful constants for state names and IDs
STATE_NAMES = [
    'ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA',
    'COLORADO', 'CONNECTICUT', 'DELAWARE', 'DISTRICT OF COLUMBIA', 'FLORIDA',
    'GEORGIA', 'HAWAII', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS',
    'KENTUCKY', 'LOUISIANA', 'MAINE', 'MARYLAND', 'MASSACHUSETTS',
    'MICHIGAN', 'MINNESOTA', 'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA',
    'NEVADA', 'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK',
    'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA', 'OREGON',
    'PENNSYLVANIA', 'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA',
    'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT', 'VIRGINIA', 'WASHINGTON',
    'WEST VIRGINIA', 'WISCONSIN', 'WYOMING', 'NATIONAL'
]

# note these integers come from US Census Bureau ordering
STATE_NUMS = [
    1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23,
    24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
    42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56, 0
]

STATES_TABLE = list(zip(STATE_NAMES, STATE_NUMS))

# punctuation symbols to handle in data cleaning
COMMA_SYMBOL = ','
PERIOD_SYMBOL = '.'
EMPTY_STR = ''


def get_age_df(file_path):
    '''
    Load age data by file name into pd.DataFrame and
    return DataFrame object with select columns and cleaned
    values.

    Note: NaN values are kept for possible use in viz.

    Args:
        file_path: str, designating file to retrieve for a given year

    Returns:
        pd.DataFrame, processed age data for that year
    '''

    # load and subset data
    df_age = pd.read_csv(file_path, header=0, names=AGE_COLUMNS)

    # clean up format and unwanted punctuation
    df_age['STATE'] = df_age['STATE'].str.upper()
    df_age['Year'] = df_age['Year'].astype(str)
    df_age['Age'] = df_age['Age'].map(lambda x: x.lstrip(PERIOD_SYMBOL))

    df_age['Total'] = df_age['Total'].replace(
        COMMA_SYMBOL,
        EMPTY_STR,
        regex=True
    )

    df_age['Total Registered'] = df_age['Total Registered'].replace(
        COMMA_SYMBOL,
        EMPTY_STR,
        regex=True
    )

    df_age['Total Voted'] = df_age['Total Voted'].replace(
        COMMA_SYMBOL,
        EMPTY_STR,
        regex=True
    )

    # type cast numeric data
    df_age['Total'] = df_age['Total'].apply(
        pd.to_numeric,
        errors='coerce'
    )

    df_age['Total Registered'] = df_age['Total Registered'].apply(
        pd.to_numeric,
        errors='coerce'
    )

    df_age['Total Voted'] = df_age['Total Voted'].apply(
        pd.to_numeric,
        errors='coerce'
    )

    # finish
    return df_age


def get_sexrace_df(file_path):
    '''
    Load sexrace data by file name into pd.DataFrame
    and return DataFrame object with select columns and cleaned
    values.

    Note: NaN values are kept for possible use in viz.

    Args:
        file_path: str, file for which to retrieve sexrace data

    Returns:
        pd.DataFrame, processed sexrace data for that year
    '''

    # load and subset data
    df_sex = pd.read_csv(file_path, header=0, names=SEX_COLUMNS)

    # clean up format and unwanted punctuation
    df_sex['STATE'] = df_sex['STATE'].str.upper()
    df_sex['Year'] = df_sex['Year'].astype(str)
    df_sex['Group'] = df_sex['Group'].map(lambda x: x.lstrip(PERIOD_SYMBOL))

    df_sex['Total Citizen'] = df_sex['Total Citizen'].replace(
        COMMA_SYMBOL,
        EMPTY_STR,
        regex=True
    )

    df_sex['Total Registered'] = df_sex['Total Registered'].replace(
        COMMA_SYMBOL,
        EMPTY_STR,
        regex=True
    )

    df_sex['Total Voted'] = df_sex['Total Voted'].replace(
        COMMA_SYMBOL,
        EMPTY_STR,
        regex=True
    )

    # type cast numeric data
    df_sex['Total Citizen'] = df_sex['Total Citizen'].apply(
        pd.to_numeric,
        errors='coerce'
    )

    df_sex['Total Registered'] = df_sex['Total Registered'].apply(
        pd.to_numeric,
        errors='coerce'
    )

    df_sex['Total Voted'] = df_sex['Total Voted'].apply(
        pd.to_numeric,
        errors='coerce'
    )

    # finish
    return df_sex


def combine_age_data(file_expression=PATH_ALL_AGE, law_filepath=PATH_LAWS):
    '''
    Generate all age-related dataframes, combine into one,
    and attach legislative data columns.

    Args:
        file_expression: str, regex to capture desired age files
        law_filepath: str, filepath to legislation data

    Returns:
        pd.DataFrame, combined age data for all years
    '''

    # retrieve all relevant file paths
    age_file_paths = glob.glob(file_expression)
    df_list = []

    # generate a dataframe from each file and combine
    for age_file in age_file_paths:
        df_curr = get_age_df(age_file)
        df_list.append(df_curr)

    combined = pd.concat(df_list, axis=0, ignore_index=True)

    # load legislative data
    df_laws = pd.read_csv(law_filepath)
    df_laws['STATE'] = df_laws['STATE'].str.upper()

    # make nationwide labels consistent
    combined['STATE'].loc[combined['STATE'] == 'US'] = 'NATIONAL'
    combined['STATE'].loc[combined['STATE'] == 'UNITED STATES'] = 'NATIONAL'
    df_laws['STATE'].loc[df_laws['STATE'] == 'US'] = 'NATIONAL'

    # attach legislative rating to age data and finish
    df_result = combined.merge(
        df_laws,
        how='outer',
        left_on='STATE',
        right_on='STATE'
    )

    return df_result


def combine_sexrace_data(file_expression=PATH_ALL_SEX, law_filepath=PATH_LAWS):
    '''
    Retrieve all sexrace-related data files, combine into one
    pd.DataFrame object, and attach legislative data columns.

    Args:
        file_expression: str, regex to capture desired age files
        law_filepath: str, filepath to legislation data

    Returns:
        pd.DataFrame, combined sexrace data for all years
    '''

    # retrieve all relevant file paths
    sex_file_paths = glob.glob(file_expression)
    df_list = []

    # generate a dataframe from each file and combine
    for sex_file in sex_file_paths:
        df_curr = get_sexrace_df(sex_file)
        df_list.append(df_curr)

    combined = pd.concat(df_list, axis=0, ignore_index=True)

    # load legislative data
    df_laws = pd.read_csv(law_filepath)
    df_laws['STATE'] = df_laws['STATE'].str.upper()

    # make nationwide labels consistent
    combined['STATE'].loc[combined['STATE'] == 'US'] = 'NATIONAL'
    combined['STATE'].loc[combined['STATE'] == 'UNITED STATES'] = 'NATIONAL'
    df_laws['STATE'].loc[df_laws['STATE'] == 'US'] = 'NATIONAL'

    # attach legislative rating to sex/race data
    df_result = combined.merge(
        df_laws,
        how='outer',
        left_on='STATE',
        right_on='STATE'
    )

    return df_result


def homogenize_age_data(df_in):
    '''
    Structures the age data by creating the desired age groups
    of 'Total','18 to 44', '45 to 65', '65+' into a DataFrame.

    Args:
        df_in: pd.Dataframe created by function combine_age_data()

    Returns:
        pd.DataFrame, age bracket structured data for all years
    '''

    # set up a table for the states
    df_states = pd.DataFrame(STATES_TABLE, columns=['STATE', 'id'])
    df_states['STATE'] = df_states['STATE'].str.upper()

    # combine existing age brackets for uniformity
    df_65plus = df_in.loc[
        (df_in['Age'] == '65 to 74')
        | (df_in['Age'] == '75+')
        | (df_in['Age'] == '65 to 75')
        | (df_in['Age'] == '65+'),
    ]

    df_45_64 = df_in.loc[
        (df_in['Age'] == '45 to 64')
        | (df_in['Age'] == '45 to 55')
        | (df_in['Age'] == '55 to 65')
        | (df_in['Age'] == '45 to 65'),
    ]

    df_18_44 = df_in.loc[
        (df_in['Age'] == '18 to 24')
        | (df_in['Age'] == '18 to 25')
        | (df_in['Age'] == '25 to 44')
        | (df_in['Age'] == '25 to 35')
        | (df_in['Age'] == '35 to 45')
        | (df_in['Age'] == '25 to 45')
        | (df_in['Age'] == '25 to 34')
        | (df_in['Age'] == '35 to 44'),
    ]

    df_total = df_in.loc[df_in['Age'] == 'Total',]

    # iteratively group DFs by state and year
    df_list = [df_total, df_18_44, df_45_64, df_65plus]
    age_brackets = ['Total', '18 to 44', '45 to 65', '65+']
    combined = []

    for i, data in enumerate(df_list):
        data = data.groupby(['STATE', 'Year'], sort=False).sum().reset_index()
        data['Age'] = age_brackets[i]
        combined.append(data)

    # recombine all age bracket DFs
    result = pd.concat(combined, axis=0, ignore_index=True)
    result.sort_values(['Year', 'STATE'], inplace=True)

    # compute voter turnout metric
    result['Percent Registered'] = result['Total Registered'] / result['Total']
    result['Percent Voted'] = result['Total Voted'] / result['Total']

    # refomatting
    result['Year'] = result['Year'].astype(int)
    result['STATE'] = result['STATE'].str.upper()
    result = result.rename(columns={'Age':'Group'})

    # attach our state labels/IDs and finish
    result = df_states.merge(
        result,
        how='outer',
        left_on='STATE',
        right_on='STATE'
    )

    return result

def homogenize_sexrace_data(df_in):
    '''
    Structures the age data by creating the desired demographic groups
    of 'Total','Male', 'Female', 'White', 'Black', 'Asian & Pacific Islander',
    'Hispanic' into a DataFrame.

    Args:
        df_in: pd.Dataframe created by function combine_age_data()

    Returns:
        pd.DataFrame, age bracket structured data for all years
    '''

    # set up a table for the states
    df_states = pd.DataFrame(STATES_TABLE, columns=['STATE', 'id'])
    df_states.STATE = df_states.STATE.str.upper()

    # all relevant totals
    total_columns = ['Total Citizen', 'Total Registered', 'Total Voted']

    # iteratively renaming demographic groups
    copy = df_in.copy()

    for (orig, new) in zip(ORIGINAL_SEX_GROUPS, NEW_SEX_GROUPS):
        copy.Group.loc[copy.Group == orig] = new

    # keeping relevant groups and setting years as str
    df_kept = copy.loc[copy.Group.isin(NEW_SEX_GROUPS)]
    df_kept.Year = df_kept.Year.astype(float).astype(int).astype(str)

    # iteratively validating the totals values
    for col in total_columns:

        idx = [
            'STATE',
            'Year',
            'restrictive_id_laws',
            'felony_disenfranchisement'
        ]

        merge_key = [
            'STATE',
            'Year',
            'Group',
            'restrictive_id_laws',
            'felony_disenfranchisement'
        ]

        # perform pivot and compute gender-wide totals
        df_tmp = df_kept.pivot_table(index=idx, columns='Group', values=col)
        df_tmp = df_tmp.reset_index()

        if ('Male' in df_tmp.columns) & ('Female' in df_tmp.columns):
            df_tmp.Total = df_tmp[['Male', 'Female']].sum(axis=1)

        # un-pivot
        df_tmp_unpivot = df_tmp.melt(id_vars=idx, value_name=col)

        # make a copy of un-pivoted table on first iteration
        if col == 'Total Citizen':
            df_merge = df_tmp_unpivot.copy()

        # continuously merge using merge key
        df_merge = pd.merge(
            df_merge,
            df_tmp_unpivot,
            how='left',
            left_on=merge_key,
            right_on=merge_key
        )


    # reformating values, types, and column names
    result = df_merge.drop('Total Citizen_y', axis=1)
    result.STATE = result.STATE.str.upper()
    result = result.rename(columns={'Total Citizen_x':'Total'})
    result = result.sort_values(by=['Year', 'STATE']).round()
    result.Year = result.Year.astype(int)

    # calculating the percentage of voter turnout totals
    result['Percent Registered'] = result['Total Registered'] / result['Total']
    result['Percent Voted'] = result['Total Voted'] / result['Total']

    # attach our state labels/IDs and finish
    result = pd.merge(
        result,
        df_states,
        left_on='STATE',
        right_on='STATE'
    )

    return result
