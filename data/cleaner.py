import pandas as pd


def clean_and_validate_census_data(data_json):
    df = pd.DataFrame(data_json[1:], columns=data_json[0])

    # remove unnecessary columns
    df.drop(columns=['NAICS2022', 'state', 'county'], errors='ignore', inplace=True)

    # convert specific columns to numbers
    number_columns = ['EMP', 'EMP_S', 'FIRMPDEMP', 'FIRMPDEMP_S', "INDGROUP", 'INDLEVEL', 'PAYANN', 'PAYANN_S',
                      'SECTOR']
    df[number_columns] = df[number_columns].apply(pd.to_numeric, errors='coerce')

    # remove rows where values in number_columns are negative
    df = df[(df[number_columns] >= 0).all(axis=1)]

    # number columns must remain as strings but also be valid numbers
    number_code_columns = ['ETH_GROUP', "RACE_GROUP", "RCPSZFI", "SEX", "URSZFI", "YIBSZFI"]

    # create boolean mask to check if values are numeric and non-negative
    valid_number_code_rows = df[number_code_columns].applymap(
        lambda x: x.strip().isdigit() if isinstance(x, str) else False
    )

    # keep rows where all number_code_columns have valid numeric strings
    df = df[valid_number_code_rows.all(axis=1)]

    # drop columns if all values are NaN/None/NaT
    df.dropna(axis=1, how='all', inplace=True)

    # turn all pandas NaN/None/NaT values into Unknown
    df.fillna('Unknown', inplace=True)

    # replace 'empty' strings with Unknown
    empty_strings = ['', ' ', '\t', '\n', '\r', '\xa0', '\u200b', 'N/A', 'NA', 'na', 'null', 'Null', 'NULL', 'None',
                     'Missing']
    df.replace(empty_strings, 'Unknown', inplace=True)

    # todo: remove outliers - zscore, IQR, Box Plot, Modified Z score

    return df
