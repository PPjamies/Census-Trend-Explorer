import os

from api.http import http_get
from etl_docker.census.constants.census_constants import ECONOMIC_CENSUS_API_VARIABLES, \
    ANNUAL_BUSINESS_SURVEY_API_VARIABLES
from utils.utils import remove_none_values

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


def __add_naics_variables_to_params(year: str, naics_param: int, params):
    naics_variable = f'NAICS{year}'
    params[naics_variable] = naics_param
    params['get'] += f',{naics_variable}'
    params['get'] += f',{naics_variable}_LABEL'
    return params


def fetch_economic_census(year: str, for_param: str = None, in_param: str = None, naics_param: int = None):
    url = f'{domain}/{year}/ecnbasic'
    params = {
        'get': ','.join(ECONOMIC_CENSUS_API_VARIABLES),
        'for': for_param if for_param else None,
        'in': in_param if in_param else None,
        'key': api_key
    }

    if naics_param:
        params = __add_naics_variables_to_params(year, naics_param, params)

    params = remove_none_values(params)
    return http_get(url=url, headers=headers, params=params, body={})


def fetch_annual_business_survey(year: str, for_param: str = None, in_param: str = None, naics_param: int = None,
                                 pagination: [] = None):
    url = f'{domain}/{year}/abscs'
    params = {
        'get': ','.join(ANNUAL_BUSINESS_SURVEY_API_VARIABLES),
        'for': for_param if for_param else None,
        'in': in_param if in_param else None,
        'offset': str(pagination[0]) if pagination and len(pagination) > 1 else None,
        'limit': str(pagination[1]) if pagination and len(pagination) > 2 else None,
        'key': api_key
    }

    if naics_param:
        params = __add_naics_variables_to_params(year, naics_param, params)

    params = remove_none_values(params)
    return http_get(url=url, headers=headers, params=params, body={})
