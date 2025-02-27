import pandas as pd

# todo: remove NaN, Nones, Null, and Empty strings
def remove_none_values():
    return None


# todo: remove duplicate entries
def remove_duplicates():
    return None


def remove_outliers():
    return None


# todo: consolidate fields that are basically the same (ex. sex/gender)
def consolidate_fields():
    return None


# todo: check if numerical values make any sense given the field (age - no negatives allowed)
def validate_field_types():
    return None


def clean_census_data(data_json):
    df = pd.DataFrame(data_json[1:], columns=data_json[0])
    print(df.head())

    # determine threshold to drop na or replace na
    nat_threshold =

    # replace NaN, NaT, and None with "Unknown"
    df.fillna("Unknown", inplace=True)


    return None
