import os

from api.http import http_get

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


def fetch_economic_census(year: str, state: str, county: str = None, industry_code: str = None):
    url = f'{domain}/{year}/ecnbasic'
    params = {
        'get': ','.join([
            'NAME',  # Geographic
            'EMP',  # Number of employees
            'ESTAB',  # Number of establishments
            'FIRM',  # Number of firms
            'INDLEVEL',  # Industry level
            'OPEX',  # Operating expenses
            'PAYANN',  # Annual payroll
            'RCPTOT',  # Sales, value of shipments, or revenue ($1000)
            'SECTOR'  # NAICS economic sector
        ]),
        'for': f'county:{county}' if county else f'state:{state}',
        'in': f'state:{state}' if county else None,
        'key': api_key
    }

    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    # Update NAICS codes (based on year)
    valid_years = {'2022', '2017', '2012', '2007', '2002'}
    if industry_code and year in valid_years:
        naics_field = f'NAICS{year}'
        params[naics_field] = industry_code
        params['get'] += f',{naics_field}_LABEL'

    return http_get(url=url, headers=headers, params=params, body={})


def fetch_annual_business_survey(year: str, state: str, county: str = None, industry_code: str = None,
                                 offset: int = None, limit: int = None):
    url = f'{domain}/{year}/abscs'
    params = {
        'get': ','.join([
            'NAME', # Geographic
            'EMP',  # Number of Employees,
            'EMP_S',  # Relative standard error of number of employees (%)
            'ETH_GROUP',  # Ethnicity code
            'FIRMPDEMP',  # Number of employer firms
            'FIRMPDEMP_S',  # Standard error of employer firms (%)
            'INDGROUP',  # Industry group
            'INDLEVEL',  # Industry level
            'PAYANN',  # Annual payroll
            'PAYANN_S',  # Relative standard error of annual payroll (%)
            'RACE_GROUP',  # Race of business owner
            'RCPSZFI',  # Sales, value of shipments, or revenue size of firms code
            'SECTOR',  # NAICS economic sector
            'SEX',  # Gender of business owner
            'URSZFI',  # Urban and rural classification of firms code
            'YIBSZFI'  # Years in business code
        ]),
        'for': f'county:{county}' if county else f'state:{state}',
        'in': f'state:{state}' if county else None,
        'key': api_key,
        'offset': str(offset) if offset else None,
        'limit': str(limit) if limit else None
    }

    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}

    # Update NAICS codes (based on year)
    valid_years = {'2023', '2022', '2021', '2020', '2019', '2018'}
    if industry_code and year in valid_years:
        naics_field = f'NAICS{year}'
        params[naics_field] = industry_code
        params['get'] += f',{naics_field}_LABEL'

    return http_get(url=url, headers=headers, params=params, body={})
