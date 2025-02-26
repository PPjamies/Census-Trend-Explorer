# Census-Trend-Explorer
Explore and visualize trends, correlations, and KPIs from a real-world dataset. This project focuses on Exploratory Data Analysis (EDA) to uncover valuable insights and make data-driven decisions.

- request API Key from census.gov https://www.census.gov/data/developers.html
- browse public data sets https://www.census.gov/data/developers/data-sets.html
- state and countries FIPS codes: https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt

Goal - I want to know:

- which industries are in need of tech adoption (which ones have had major adoption vs low adoption)
- I want to know about these industries revenue growth, customer growth, employee growth, expenditures
- I want to be able to filter the geographical location down to the county level (if not possible then it needs to at least filter by state)

For a separate report I want to:
- know about computer related industries such as (IT consultant, software developer, software engineer, etc) such as there revenues, expenditures, growth prospects
- I also want to know about business owner demographics of these companies (ethnicity, sex, etc)
- I want to be able to filter by county or at the very least state.


Economic Census

Professional, Scientific, and Technical Services: Summary Statistics for the U.S., States, and Selected Geographies: 2022

* EMP - EMP_F - Number of employees
* ESTAB - ESTAB_F - Number of establishments
* FIRM - FIRM_F - Number of firms
* INDLEVEL - Industry level
* NAICS2022 - NAICS2022_LABEL - 2022 NAICS code
* OPEX - OPEX_F - Operating expenses ($1000)
* PAYANN - PAYANN_F - Annual payroll ($1000)
* RCPTOT - RCPTOT_F - Sales, value of shipments, or revenue ($1,000)
* SECTOR - NAICS economic sector


Annual Business Survey
* EMP - EMP_F - Number of employees
* EMP_S - EMP_S_F - Relative standard error of number of employees (%)
* ETH_GROUP - ETH_GROUP_LABEL - Ethnicity code
* FIRMPDEMP - FIRMDEMP_F - Number of employer firms
* FIRMPDEMP_S - FIRMPDEMP_S_F - Relative SE of employer firms (%)
* INDGROUP - Industry group
* INDLEVEL - Industry level
* NAICS2022 - NAICS2022_LABEL - 2022 NAICS code
* PAYANN - PAYANN_F - Annual payroll ($1000)
* PAYANN_S - PAYANN_S_F - Relative SE of annual payroll
* RACE_GROUP - RACE_GROUP_LABEL - Race code
* RCPSZFI - RCPSZFI_LABEL - Sales, value of shipments, or revenue size of firms code
* SECTOR - NAICS economic sector
* SEX - SEX_LABEL - Sex code
* URSZFI - URSZFI_LABEL - Urban and rural classification of firms code
* YIBSZFI - YIBSZFI_LABEL - Years in business code


## Approach
1. get data from census
2. clean data:
   - NaN, None
   - duplicates
   - outliers
   - inconsistent data column names that result in duplicate values
   - inconsistent numerical values (negatives)
   - standardizing formats
   - inconsistent categorical data