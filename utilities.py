import streamlit as st
import pandas as pd
import wikipedia
import requests
import json
import numpy as np
from typing import Any, Dict

WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

METRIC_PARAMETER = 'metric'
FIPS_PARAMETER = 'fips'

INTEGER_METRICS = ['population', 'HPSA Score', 'transit_trips_index', 'transit_low_cost_index', 
                  'crime_rate', 'juvenile_crime_rate', 'avg_edu_prof_diff', 'median_family_income',
                  'income_20_percentile', 'income_80_percentile', 'median_family_income_white',
                  'median_family_income_black', 'median_family_income_indigenous',
                  'median_family_income_asian', 'median_family_income_hispanic']

PERCENT_METRICS = ['proportion_homeless', 'low_birth_rate', 'Not Hispanic or Latino_low_birth_rate',
                    'Hispanic or Latino_low_birth_rate', 'Black or African American_low_birth_rate',
                    'White_low_birth_rate', 'Asian_low_birth_rate', 'proportion_voter', 
                    'proportion_high_poverty_neighborhood', 'hispanic_or_latino_exposure', 'white_exposure',
                    'black_exposure','native_american_exposure', 'asian_exposure', 'preschool_enroll',
                    'preschool_enrollment_white', 'preschool_enrollment_black','preschool_enrollment_hispanic',
                    'preschool_enrollment_indigenous', 'preschool_enrollment_asian', 'employed_25_54_population',
                    'employed_16_64_population', 'black_employed_16_64', 'white_employed_16_64',
                    'hispanic_or_latino_employed_16_64', 'american_indian_employed_16_64', 'asian_employed_16_64',
                    'some_other_race_alone_employed_16_64', 'two_or_more_race_employed_16_64']

# per https://stackoverflow.com/questions/30595918/is-there-any-api-to-get-image-from-wiki-page
def get_wiki_image(search_term):
    '''
    get an image from wikipedia using a search term
    '''
    try:
        result = wikipedia.search(search_term, results = 1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
        response  = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link        
    except:
        return 0

@st.cache(suppress_st_warning=True)
def get_dataframe():
    '''
    gets the dataframe used for the site
    '''
    df = pd.read_csv('counties_merged.csv')

    averages = {}

    feature_names = ['population','white','black','native_american','asian','hawaiian','some_other_race_alone','two_more_races','hispanic_or_latino',
                 'white_employed_16_64', 'black_employed_16_64',  'american_indian_employed_16_64', 'asian_employed_16_64', 'some_other_race_alone_employed_16_64',
                 'two_or_more_race_employed_16_64', 'hispanic_or_latino_employed_16_64', 'employed_25_54_population', 'employed_16_64_population',
                 'median_family_income','income_20_percentile','income_80_percentile','median_family_income_white','median_family_income_black',
                 'median_family_income_indigenous','median_family_income_asian','median_family_income_hispanic', 'all_in_poverty','juvenile_crime_rate',
                 'some_other_race_under_5','two_or_more_race_under_5', 'preschool_enrollment_white','preschool_enrollment_black','preschool_enrollment_hispanic','preschool_enrollment_indigenous','preschool_enrollment_asian','year','public_students_pre_12','white_employed_16_64','black_employed_16_64','american_indian_employed_16_64','asian_employed_16_64','some_other_race_alone_employed_16_64','two_or_more_race_employed_16_64','hispanic_or_latino_employed_16_64','employed_25_54_population','employed_16_64_population','preschool_enroll','white_under_5','black_under_5','indigenous_under_5','asian_under_5','hispanic_under_5','avg_edu_prof_diff','low_birth_rate','Not Hispanic or Latino_low_birth_rate','Hispanic or Latino_low_birth_rate','Unknown or Not Stated_low_birth_rate','Black or African American_low_birth_rate','White_low_birth_rate','Asian_low_birth_rate','More than one race_low_birth_rate','American Indian or Alaska Native_low_birth_rate','Native Hawaiian or Other Pacific Islander_low_birth_rate','HPSA Score','HOM_STUDENTS','proportion_homeless','proportion_voter','proportion_high_poverty_neighborhood','transit_trips_index','transit_low_cost_index','crime_rate']

    for f in feature_names:
        averages[f] = df[f].mean()

    return df, averages

def get_metric(name: str, col_name: str,county_df: pd.DataFrame, averages:Dict[str,Any], format_pattern:str=None, delta_color='normal'):
    '''
    build a metric display based on the column details
    '''
    value = county_df[col_name].values[0]

    delta = None

    if value:
        value = float(value)
        delta = round(value/averages[col_name], 1)
    
    if np.isnan(value):
        return st.metric(name,
            value = 'n/a',
            delta='No data available',
            delta_color='off' 
        )

    if format_pattern is not None:
        value = format_pattern.format(value)
    
    if delta is not None:
        delta_str = f'{delta}% from national average'

        return st.metric(name,
            value = value, 
            delta=delta_str, 
            delta_color=delta_color
        )
    else:
        return st.metric(name,
            value = value
        )

def get_parameter(name, default_value):
    '''
    gets a parameter from the query string

    name: the parameter to get
    default_value: value if the parameter is not found
    '''

    url_params = st.experimental_get_query_params()

    param_value = default_value

    if name in url_params and len(url_params[name][0])>0:
        param_value = url_params[name][0]

    return param_value
