import os
import unittest
from unittest.mock import patch

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('CENSUS_API_KEY')
if not api_key:
    raise ValueError('Missing environment variable: CENSUS_API_KEY')

domain = os.getenv('CENSUS_DOMAIN')
if not domain:
    raise ValueError('Missing environment variable: CENSUS_DOMAIN')


def fetch_economic_census(year: str, state: str, county: str = None, industry_code: str = None):
    response = requests.get(
        f'{domain}/{year}/ecnbasic?get=NAME,EMP,ESTAB,FIRM,INDLEVEL,OPEX,PAYANN,RCPTOT,SECTOR,NAICS2022_LABEL&for=county:{county}&in=state:{state}&NAICS2022={industry_code}&key={api_key}')
    if response.status_code == 200:
        return response.json()
    else:
        return []


def fetch_annual_business_survey(year: str, state: str, county: str = None, industry_code: str = None,
                                 offset: int = None, limit: int = None):
    response = requests.get(
        f'{domain}/{year}/abscs?get=NAME,EMP,EMP_S,ETH_GROUP,FIRMPDEMP,FIRMPDEMP_S,INDGROUP,INDLEVEL,PAYANN,PAYANN_S,RACE_GROUP,RCPSZFI,SECTOR,SEX,URSZFI,YIBSZFI,NAICS2022_LABEL&for=county:{county}&in=state:{state}&NAICS2022={industry_code}&key={api_key}&offset={offset}&limit={limit}')
    if response.status_code == 200:
        return response.json()
    else:
        return []


class TestService(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_economic_census(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            ["NAME", "EMP", "ESTAB", "FIRM", "INDLEVEL", "OPEX", "PAYANN", "RCPTOT", "SECTOR", "NAICS2022_LABEL",
             "NAICS2022", "state", "county"],
            ["King County, Washington", "178901", "11185", "10643", "2", "0", "19155041", "46434744", "54",
             "Professional, scientific, and technical services", "54", "53", "033"]]
        mock_get.return_value = mock_response

        economic_census = fetch_economic_census(year='2022', state='53', county='033', industry_code='54')
        assert economic_census
        assert len(economic_census) == 2

        # validate first column contain the expected fields
        actual_columns = economic_census[0]
        assert actual_columns

        expected_columns = ["NAME", "EMP", "ESTAB", "FIRM", "INDLEVEL", "OPEX", "PAYANN", "RCPTOT", "SECTOR",
                            "NAICS2022_LABEL", "NAICS2022", "state", "county"]
        assert actual_columns == expected_columns

    @patch('requests.get')
    def test_fetch_annual_business_survey(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            ["NAME", "EMP", "EMP_S", "ETH_GROUP", "FIRMPDEMP", "FIRMPDEMP_S", "INDGROUP", "INDLEVEL", "PAYANN",
             "PAYANN_S", "RACE_GROUP", "RCPSZFI", "SECTOR", "SEX", "URSZFI", "YIBSZFI", "NAICS2022_LABEL", "NAICS2022",
             "state", "county"],
            ["King County, Washington", "165429", "3.3", "001", "10443", "2.8", None, "2", "17828290", "3.2", "00",
             "001", "54", "001", "001", "001", "Professional, scientific, and technical services", "54", "53", "033"],
            ["King County, Washington", "15017", "14.6", "001", "3035", "9.7", None, "2", "1329981", "14.7", "00",
             "001", "54", "002", "001", "001", "Professional, scientific, and technical services", "54", "53", "033"],
            ["King County, Washington", "56261", "10.5", "001", "5757", "7.4", None, "2", "6090012", "10.5", "00",
             "001", "54", "003", "001", "001", "Professional, scientific, and technical services", "54", "53", "033"],
            ["King County, Washington", "6072", "24.4", "001", "1010", "19.9", None, "2", "538043", "22.4", "00", "001",
             "54", "004", "001", "001", "Professional, scientific, and technical services", "54", "53", "033"]]
        mock_get.return_value = mock_response

        surveys = fetch_annual_business_survey(year='2022', state='53', county='033', industry_code='54', offset=0,
                                               limit=5)
        assert surveys
        assert len(surveys) == 5

        # validate first column contain the expected fields
        actual_columns = surveys[0]
        assert actual_columns

        expected_columns = ["NAME", "EMP", "EMP_S", "ETH_GROUP", "FIRMPDEMP", "FIRMPDEMP_S", "INDGROUP", "INDLEVEL",
                            "PAYANN", "PAYANN_S", "RACE_GROUP", "RCPSZFI", "SECTOR", "SEX", "URSZFI", "YIBSZFI",
                            "NAICS2022_LABEL", "NAICS2022", "state", "county"]
        assert actual_columns == expected_columns
