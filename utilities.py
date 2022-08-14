import streamlit as st
import pandas as pd
import wikipedia
import requests
import json
import numpy as np
from typing import Any, Dict

WIKI_REQUEST = "http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles="

METRIC_PARAMETER = "metric"
FIPS_PARAMETER = "fips"

INTEGER_METRICS = [
    "population",
    "HPSA Score",
    "transit_trips_index",
    "transit_low_cost_index",
    "crime_rate",
    "juvenile_crime_rate",
    "avg_edu_prof_diff",
    "median_family_income",
    "income_20_percentile",
    "income_80_percentile",
    "median_family_income_white",
    "median_family_income_black",
    "median_family_income_indigenous",
    "median_family_income_asian",
    "median_family_income_hispanic",
]

PERCENT_METRICS = [
    "proportion_homeless",
    "low_birth_rate",
    "Not Hispanic or Latino_low_birth_rate",
    "Hispanic or Latino_low_birth_rate",
    "Black or African American_low_birth_rate",
    "White_low_birth_rate",
    "Asian_low_birth_rate",
    "proportion_voter",
    "proportion_high_poverty_neighborhood",
    "hispanic_or_latino_exposure",
    "white_exposure",
    "black_exposure",
    "native_american_exposure",
    "asian_exposure",
    "preschool_enroll",
    "preschool_enrollment_white",
    "preschool_enrollment_black",
    "preschool_enrollment_hispanic",
    "preschool_enrollment_indigenous",
    "preschool_enrollment_asian",
    "employed_25_54_population",
    "employed_16_64_population",
    "black_employed_16_64",
    "white_employed_16_64",
    "hispanic_or_latino_employed_16_64",
    "american_indian_employed_16_64",
    "asian_employed_16_64",
    "some_other_race_alone_employed_16_64",
    "two_or_more_race_employed_16_64",
]

HUMAN_READABLE_METRICS = {
    "population": "Population",
    "proportion_homeless": "Housing instability and homelessness in students",
    "HPSA Score": "Health Professional Shortage Area Score",
    "low_birth_rate": "Proportion of Births Classified as Low-Weight",
    "Not Hispanic or Latino_low_birth_rate": "Proportion of Births Classified as Low-Weight: Non Hispanic or Latino",
    "Hispanic or Latino_low_birth_rate": "Proportion of Births Classified as Low-Weight: Hispanic or Latino",
    "Unknown or Not Stated_low_birth_rate": "Unknown Or Not Stated Low Birth Rate",
    "Black or African American_low_birth_rate": "Proportion of Births Classified as Low-Weight: Black",
    "White_low_birth_rate": "Proportion of Births Classified as Low-Weight: White",
    "Asian_low_birth_rate": "Proportion of Births Classified as Low-Weight: Asian",
    "More than one race_low_birth_rate": "More Than One Race Low Birth Rate",
    "American Indian or Alaska Native_low_birth_rate": "American Indian Or Alaska Native Low Birth Rate",
    "Native Hawaiian or Other Pacific Islander_low_birth_rate": "Native Hawaiian Or Other Pacific Islander Low Birth Rate",
    "proportion_voter": "Voter Turnout",
    "proportion_high_poverty_neighborhood": "Residents Living in High Poverty Neighborhoods",
    "hispanic_or_latino_exposure": "Racial Exposure: Hispanic or Latino Population",
    "white_exposure": "Racial Exposure: White Population",
    "black_exposure": "Racial Exposure: Black Population",
    "native_american_exposure": "Racial Exposure: Native American Population",
    "asian_exposure": "Racial Exposure: Asian Population",
    "hawaiian_exposure": "Hawaiian Exposure",
    "some_other_race_alone_exposure": "Some Other Race Alone Exposure",
    "two_more_races_exposure": "Two More Races Exposure",
    "transit_trips_index": "Transit Trips Index",
    "transit_low_cost_index": "Transit Low Cost Index",
    "crime_rate": "Violent Crime Rate",
    "juvenile_crime_rate": "Juvenile Crime Rate",
    "avg_edu_prof_diff": "Average Change in English Language Arts Achievement",
    "preschool_enroll": "Preschool Enrollment Rate",
    "white_under_5": "White Under 5",
    "black_under_5": "Black Under 5",
    "indigenous_under_5": "Indigenous Under 5",
    "asian_under_5": "Asian Under 5",
    "hispanic_under_5": "Hispanic Under 5",
    "two_or_more_race_under_5": "Two Or More Race Under 5",
    "some_other_race_under_5": "Some Other Race Under 5",
    "preschool_enrollment_white": "Preschool Enrollment: White",
    "preschool_enrollment_black": "Preschool Enrollment: Black",
    "preschool_enrollment_hispanic": "Preschool Enrollment: Hispanic",
    "preschool_enrollment_indigenous": "Preschool Enrollment: Indigenous",
    "preschool_enrollment_asian": "Preschool Enrollment: Asian",
    "employed_25_54_population": "Employment-to-Population Ratio 25 - 54 y.o.",
    "employed_16_64_population": "Employment-to-Population Ratio 16 - 64 y.o.",
    "black_employed_16_64": "Employment-to-Population Ratio 16 - 64 y.o.: Black",
    "white_employed_16_64": "Employment-to-Population Ratio 16 - 64 y.o.: White",
    "hispanic_or_latino_employed_16_64": "Employment-to-Population Ratio 16 - 64 y.o.: Hispanic or Latino",
    "american_indian_employed_16_64": "Employment-to-Population Ratio 16 - 64 y.o.: American Indian",
    "asian_employed_16_64": "Employment-to-Population Ratio 16 - 64 y.o.: Asian",
    "some_other_race_alone_employed_16_64": "Employment-to-Population Ratio 16 - 64 y.o.: Some Other Race",
    "two_or_more_race_employed_16_64": "Employment-to-Population Ratio 16 - 64 y.o.: Two or More Other Race",
    "median_family_income": "Median Household Income",
    "income_20_percentile": "20th Percentile Household Income",
    "income_80_percentile": "80th Percentile Household Income",
    "median_family_income_white": "Median Household Income, Race: White",
    "median_family_income_black": "Median Household Income, Race: Black",
    "median_family_income_indigenous": "Median Household Income, Race: Indigenous",
    "median_family_income_asian": "Median Household Income, Race: Asian",
    "median_family_income_hispanic": "Median Household Income, Race: Hispanic",
}

PREFERRED_METRICS = {
    "Housing instability and homelessness in students": "proportion_homeless",
    "HPSA Score": "HPSA Score",
    "Proportion of Births Classified as Low-Weight": "low_birth_rate",
    "Voter Turnout": "proportion_voter",
    "Residents Living in High Poverty Neighborhoods": "proportion_high_poverty_neighborhood",
    "Racial Exposure: Hispanic or Latino Population": "hispanic_or_latino_exposure",
    "Racial Exposure: White Population": "white_exposure",
    "Racial Exposure: Black Population": "black_exposure",
    "Racial Exposure: Native American Population": "native_american_exposure",
    "Transit Trips Index": "transit_trips_index",
    "Transit Low Cost Index": "transit_low_cost_index",
    "Violent Crime Rate": "crime_rate",
    "Juvenile Crime Rate": "juvenile_crime_rate",
    "Average Change in English Language Arts Achievement": "avg_edu_prof_diff",
    "Preschool Enrollment Rate": "preschool_enroll",
    "Employment-to-Population Ratio 25 - 54 y.o.": "employed_25_54_population",
    "Median Household Income": "median_family_income",
    "20th Percentile Household Income": "income_20_percentile",
    "80th Percentile Household Income": "income_80_percentile",
}

IDEAL_SCORES = {
    "proportion_homeless": 0,
    "HPSA Score": 0,
    "low_birth_rate": 0,
    "proportion_voter": 1,
    "proportion_high_poverty_neighborhood": 0,
    "hispanic_or_latino_exposure": 0.5,
    "white_exposure": 0.5,
    "black_exposure": 0.5,
    "native_american_exposure": 0.5,
    "transit_trips_index": 100,
    "transit_low_cost_index": 100,
    "crime_rate": 0,
    "juvenile_crime_rate": 0,
    "avg_edu_prof_diff": 20,
    "preschool_enroll": 1,
    "employed_25_54_population": 1,
    "median_family_income": 300000,
    "income_20_percentile": 300000,
    "income_80_percentile": 300000,
}

# per https://stackoverflow.com/questions/30595918/is-there-any-api-to-get-image-from-wiki-page
def get_wiki_image(search_term):
    """
    get an image from wikipedia using a search term

    search_term: the term to search on Wikipedia
    """
    try:
        result = wikipedia.search(search_term, results=1)
        wikipedia.set_lang("en")
        wkpage = wikipedia.WikipediaPage(title=result[0])
        title = wkpage.title
        response = requests.get(WIKI_REQUEST + title)
        json_data = json.loads(response.text)
        img_link = list(json_data["query"]["pages"].values())[0]["original"]["source"]
        return img_link
    except:
        return 0


@st.cache(suppress_st_warning=True)
def get_dataframe():
    """
    gets the dataframe and averages used for the site
    """
    df = pd.read_csv("counties_merged.csv")

    averages = {}

    feature_names = [
        "population",
        "white_total",
        "black_total",
        "native_american_total",
        "asian_total",
        "hawaiian_total",
        "some_other_race_alone_total",
        "two_more_races_total",
        "hispanic_or_latino_total",
        "hispanic_or_latino_white_total",
        "hispanic_or_latino_black_total",
        "hispanic_or_latino_american_indian_total",
        "hispanic_or_latino_asian_total",
        "hispanic_or_latino_hawaiian_total",
        "hispanic_or_latino_some_other_race_total",
        "hispanic_or_latino_two_or_more_races_total",
        "not_hispanic_or_latino_total",
        "hispanic_or_latino",
        "white_employed_16_64",
        "black_employed_16_64",
        "american_indian_employed_16_64",
        "asian_employed_16_64",
        "some_other_race_alone_employed_16_64",
        "two_or_more_race_employed_16_64",
        "hispanic_or_latino_employed_16_64",
        "employed_25_54_population",
        "employed_16_64_population",
        "median_family_income",
        "income_20_percentile",
        "income_80_percentile",
        "median_family_income_white",
        "median_family_income_black",
        "median_family_income_indigenous",
        "median_family_income_asian",
        "median_family_income_hispanic",
        "all_in_poverty",
        "juvenile_crime_rate",
        "some_other_race_under_5",
        "two_or_more_race_under_5",
        "preschool_enrollment_white",
        "preschool_enrollment_black",
        "preschool_enrollment_hispanic",
        "preschool_enrollment_indigenous",
        "preschool_enrollment_asian",
        "year",
        "public_students_pre_12",
        "white_employed_16_64",
        "black_employed_16_64",
        "american_indian_employed_16_64",
        "asian_employed_16_64",
        "some_other_race_alone_employed_16_64",
        "two_or_more_race_employed_16_64",
        "hispanic_or_latino_employed_16_64",
        "employed_25_54_population",
        "employed_16_64_population",
        "preschool_enroll",
        "white_under_5",
        "black_under_5",
        "indigenous_under_5",
        "asian_under_5",
        "hispanic_under_5",
        "avg_edu_prof_diff",
        "low_birth_rate",
        "Not Hispanic or Latino_low_birth_rate",
        "Hispanic or Latino_low_birth_rate",
        "Unknown or Not Stated_low_birth_rate",
        "Black or African American_low_birth_rate",
        "White_low_birth_rate",
        "Asian_low_birth_rate",
        "More than one race_low_birth_rate",
        "American Indian or Alaska Native_low_birth_rate",
        "Native Hawaiian or Other Pacific Islander_low_birth_rate",
        "HPSA Score",
        "HOM_STUDENTS",
        "proportion_homeless",
        "proportion_voter",
        "proportion_high_poverty_neighborhood",
        "transit_trips_index",
        "transit_low_cost_index",
        "crime_rate",
    ]

    for f in feature_names:
        averages[f] = df[f].mean()

    return df, averages


def get_metric(
    name: str,
    col_name: str,
    county_df: pd.DataFrame,
    averages: Dict[str, Any],
    format_pattern: str = None,
    delta_color: str = "normal",
):
    """
    build a metric display based on the column details

    name: the display name of the metric
    col_name: the column name in the dataframe
    county_df: the dataframe to use
    averages: a dictionary of the national averages
    format_pattern: the pattern of the metric, if any
    delta_color: indicates if a metric should display green (normal), red (inverse), or none (off)
    """
    value = county_df[col_name].values[0]

    delta = None

    if value:
        value = float(value)
        delta = value - averages[col_name]

    if np.isnan(value):
        return st.metric(
            name, value="n/a", delta="No data available", delta_color="off"
        )

    if format_pattern is not None:
        value = format_pattern.format(value)

    if delta is not None:
        if col_name in PERCENT_METRICS:
            delta_str = f"{round(delta*100, 1)}% from national average"
        else:
            delta_str = f"{round(delta, 1)} from national average"
        return st.metric(name, value=value, delta=delta_str, delta_color=delta_color)
    else:
        return st.metric(name, value=value)


def get_parameter(name, default_value):
    """
    gets a parameter from the query string

    name: the parameter to get
    default_value: value if the parameter is not found
    """

    url_params = st.experimental_get_query_params()

    param_value = default_value

    if name in url_params and len(url_params[name][0]) > 0:
        param_value = url_params[name][0]

    return param_value


def get_county_details_url():
    """
    gets the URL used for linking to the details page
    """
    url = ""

    debug = get_parameter("debug", "false")

    if debug == "true":
        url = "http://localhost:8501/?fips="
    else:
        url = "https://davidhcoe-mads697-main-1sf12v.streamlitapp.com/?fips="

    return url
