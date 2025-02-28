import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

load_dotenv()
db_url = os.getenv('DB_URL')
if not db_url:
    raise ValueError('Missing environment variable: DB_URL')

engine = create_engine(db_url, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class CensusDataNotFound(Exception):
    pass


class InvalidDataFilter(Exception):
    pass


class EconomicCensusData(Base):
    __tablename__ = 'economic_census'

    id = Column(Integer, primary_key=True, autoincrement=True)

    state = Column(Integer)
    state_label = Column(String(15))
    county = Column(Integer)
    county_label = Column(String(50))
    naics = Column(Integer)
    naics_label = Column(String(200))

    sector = Column(String(200))
    industry_level = Column(Integer)
    industry_level_label = Column(String(200))
    employees = Column(Integer)
    establishments = Column(Integer)
    firms = Column(Integer)

    total_receipts = Column(Float)
    annual_payroll = Column(Float)
    operating_expenses = Column(Float)


class AnnualBusinessSurveyData(Base):
    __tablename__ = 'annual_business_servey'

    id = Column(Integer, primary_key=True, autoincrement=True)

    state = Column(Integer)
    state_label = Column(String(15))
    county = Column(Integer)
    county_label = Column(String(50))
    naics = Column(Integer)
    naics_label = Column(String(200))

    # demographics
    ethnicity = Column(Integer)
    ethnicity_label = Column(String(20))
    race = Column(Integer)
    race_label = Column(String(10))
    sex = Column(Integer)
    sex_label = Column(String(10))
    veteran = Column(Integer)
    veteran_label = Column(String(10))
    urban_rural_classification = Column(Integer)
    urban_rural_classification_label = Column(String(15))

    # Business
    sector = Column(String(200))
    industry_group = Column(Integer)
    industry_group_label = Column(String(200))
    industry_level = Column(Integer)
    industry_level_label = Column(String(200))

    employees = Column(Integer)
    establishments = Column(Integer)
    firms = Column(Integer)

    revenue = Column(Integer)
    revenue_category = Column(String(200))
    years_in_business = Column(Integer)


def create_data(session, data):
    session.add(data)
    session.commit()


def retrieve_data_by_id(session, model_class, data_id: int):
    data = session.query(model_class).filter(model_class.id == data_id).first()
    if not data:
        raise CensusDataNotFound(f'No data found with ID = {data_id}')
    return data


def retrieve_data_by_filters(session, model_class, state: str = None, county: str = None,
                             naics: str = None):
    query = session.query(model_class)
    has_filters = False

    if state:
        query = query.filter(model_class.state == state)
        has_filters = True
    if county:
        query = query.filter(model_class.county == county)
        has_filters = True
    if naics:
        query = query.filter(model_class.naics == naics)
        has_filters = True

    if not has_filters:
        raise InvalidDataFilter(f'At least one filter must be provided (state, county, or naics)')

    data = query.first()

    if not data:
        raise CensusDataNotFound(f'No data found filters = state:{state}, county: {county}, naics:{naics}')
    return data
