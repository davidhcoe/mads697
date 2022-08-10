import streamlit as st

from utilities import get_parameter, FIPS_PARAMETER, METRIC_PARAMETER
from county_details import show_county_details_page
from national import show_national_page

if __name__ == '__main__':
    #streamlit wants to add a side panel if we use the native pages, which we dont want

    metric = get_parameter(METRIC_PARAMETER,'')

    fips = get_parameter(FIPS_PARAMETER, '')

    if len(metric) > 0:
        show_national_page()
    elif len(fips) > 0 and fips.isnumeric():
        show_county_details_page()
    else:
        st.experimental_set_query_params(metric='population')
        show_national_page()
