import os

from api.http import http_get
from census_constants import ECONOMIC_CENSUS_API_VARIABLES, ANNUAL_BUSINESS_SURVEY_API_VARIABLES
from utils import remove_none_values

api_key = os.getenv('CENSUS_API_KEY')
if not api_key:
    raise ValueError('Missing environment variable: CENSUS_API_KEY')

domain = os.getenv('CENSUS_DOMAIN')
if not domain:
    raise ValueError('Missing environment variable: CENSUS_DOMAIN')

headers = {
    'user-agent': 'MyCensusAPIClient/1.0',
    'accept': 'application/json'
}


# if industry_code and year in valid_years:
#     naics_field = f'NAICS{year}'
#     params[naics_field] = industry_code
#     params['get'] += f',{naics_field}_LABEL'

# if industry_code and year in valid_years:
#     naics_field = f'NAICS{year}'
#     params[naics_field] = industry_code
#     params['get'] += f',{naics_field}_LABEL'

def fetch_economic_census(year: str, get_param: [] = None, for_param: str = None, in_param: str = None):
    url = f'{domain}/{year}/ecnbasic'
    params = {
        'get': ','.join(ECONOMIC_CENSUS_API_VARIABLES + get_param),
        'for': for_param if for_param else None,
        'in': in_param if in_param else None,
        'key': api_key
    }
    params = remove_none_values(params)
    return http_get(url=url, headers=headers, params=params, body={})


def fetch_annual_business_survey(year: str, get_param: [] = None, for_param: str = None, in_param: str = None,
                                 pagination: [] = None):
    url = f'{domain}/{year}/abscs'
    params = {
        'get': ','.join(ANNUAL_BUSINESS_SURVEY_API_VARIABLES + get_param),
        'for': for_param if for_param else None,
        'in': in_param if in_param else None,
        'offset': str(pagination[0]) if pagination and len(pagination) > 1 else None,
        'limit': str(pagination[1]) if pagination and len(pagination) > 2 else None,
        'key': api_key
    }
    params = remove_none_values(params)
    return http_get(url=url, headers=headers, params=params, body={})
