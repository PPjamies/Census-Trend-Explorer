import os

from api.http import http_get

api_key = os.getenv('CENSUS_API_KEY')
if not api_key:
    raise ValueError("Missing environment variable: CENSUS_API_KEY")

domain = 'https://api.census.gov/data'
headers = {
    'user-agent': 'MyCensusAPIClient/1.0',
    'accept': 'application/json'
}


# years: 2022, 2017, 2012, 2007, 2002
def get_economic_census(year: str, state: str, county: str = None, industry_code: str = None):
    url = f'{domain}/{year}/ecnbasic'
    params = {
        'get': 'EMP,ESTAB',
        'for': f'state:{state}',
        'in': f'county:{county}' if county else None,
        'NAICS': industry_code if industry_code else None,
        'key': api_key
    }

    params = {k: v for k, v in params.items() if v is not None}

    return http_get(url=url, headers={}, params=params, body={})


# years: 2023, 2022, 2021, 2020, 2019, 2018
def get_annual_business_survey(year: str, state: str, county: str = None, industry_code: str = None):
    url = f'{domain}/{year}/abs'
    params = {
        'get': ','.join([
            'EMP',  # Total number of employees
            'PAYANN',  # Annual payroll
            'RCPTOT',  # Total revenue
            'RACE_GROUP',  # Race of business owner
            'SEX',  # Gender of business owner
            'FIRMPDEMP',  # Number of employees
            'FIRMCHAR',  # Business age and survival rate
            'TECHUSE'  # Technology adoption
        ]),
        'for': f'state:{state}',
        'in': f'county:{county}' if county else None,
        'NAICS': industry_code if industry_code else None,
        'key': api_key
    }

    params = {k: v for k, v in params.items() if v is not None}

    return http_get(url=url, headers={}, params=params, body={})
