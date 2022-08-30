import streamlit as st
from utilities import (
    get_parameter,
    FIPS_PARAMETER,
    METRIC_PARAMETER,
    FIPS1_PARAMETER,
    FIPS2_PARAMETER,
)
from county_details import show_county_details_page
from county_comparer import show_county_comparer_page
from national import show_national_page
from county_picker import show_county_picker_page

if __name__ == "__main__":
    # streamlit wants to add a side panel if we use the native pages, which we dont want

    metric = get_parameter(METRIC_PARAMETER, "")

    fips = get_parameter(FIPS_PARAMETER, "")
    fips1 = get_parameter(FIPS1_PARAMETER, "")
    fips2 = get_parameter(FIPS2_PARAMETER, "")

    page = get_parameter("page", "")

    if len(metric) > 0:
        show_national_page()
    elif len(fips) > 0 and fips.isnumeric():
        show_county_details_page()
    elif len(fips1) > 0 and fips1.isnumeric() and len(fips2) > 0 and fips2.isnumeric():
        show_county_comparer_page(fips1, fips2)
    elif page.lower() == "picker":
        show_county_picker_page()
    else:
        st.experimental_set_query_params(metric="population")
        show_national_page()
