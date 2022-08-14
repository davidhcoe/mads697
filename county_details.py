import numpy as np
from typing import Any, Dict
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

from utilities import (
    get_dataframe,
    get_metric,
    get_parameter,
    get_wiki_image,
    FIPS_PARAMETER,
)


def show_county_details_page():
    """
    executes the code needed for the county_details page to display
    """

    fips_code = get_parameter(FIPS_PARAMETER, "")

    if len(fips_code) == 0 or fips_code.isnumeric() == False:
        st.title(f"Cant find any data for {fips_code}")
    else:
        # build the main content for the report on the page

        df, averages = get_dataframe()

        county_only_df = df[df["FIPS"] == int(fips_code)]

        if len(county_only_df) == 1:
            name = county_only_df.NAME.values[0]

            wiki_image = get_wiki_image(name)

            if wiki_image != 0:
                st.markdown(
                    "<style>.container {        display: flex;        align-items: center;        justify-content: center}      img {        max-width: 100%}      .image {        flex-basis: 40%}      .text {        font-size: 14px;        padding-left: 20px;}</style>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="container"><div class="image"><img src="{wiki_image}" alt="Wikipedia image of {name}"/></div><div class="text"><h1>{name}</h1><a href="#population">Population</a> | <a href="#strong-and-healthy-families">Strong and Healthy Families</a> | <a href="#supportive-communities">Supportive Communities</a> | <a href="#opportunities-to-learn-and-earn">Opportunities to Learn and Earn</a></div>',
                    unsafe_allow_html=True,
                )
                # st.markdown(f'<img src="" width="300" height="225" alt="Wikipedia image of {name}"/>', unsafe_allow_html=True)
            else:
                st.title(f"{name}")
                st.markdown(
                    '<a href="#population">Population</a> | <a href="#strong-and-healthy-families">Strong and Healthy Families</a> | <a href="#supportive-communities">Supportive Communities</a> | <a href="#opportunities-to-learn-and-earn">Opportunities to Learn and Earn</a>',
                    unsafe_allow_html=True,
                )

            #############################
            # Population
            #############################

            col1, col2 = st.columns([1, 3])

            with col1:
                st.markdown("<br><br><h2>Population</h2>", unsafe_allow_html=True)
                st.metric(
                    "2019 Population",
                    value="{:,}".format(int(county_only_df["population"].values[0])),
                )

            with col2:

                values = []

                white_hispanic = county_only_df.iloc[0][
                    "hispanic_or_latino_white_total"
                ]
                white = county_only_df.iloc[0]["white_total"] - white_hispanic
                values.append(white)
                values.append(white_hispanic)

                black_hispanic = county_only_df.iloc[0][
                    "hispanic_or_latino_black_total"
                ]
                black = county_only_df.iloc[0]["black_total"] - black_hispanic
                values.append(black)
                values.append(black_hispanic)

                native_hispanic = county_only_df.iloc[0][
                    "hispanic_or_latino_american_indian_total"
                ]
                native = (
                    county_only_df.iloc[0]["native_american_total"] - native_hispanic
                )
                values.append(native)
                values.append(native_hispanic)

                asian_hispanic = county_only_df.iloc[0][
                    "hispanic_or_latino_asian_total"
                ]
                asian = county_only_df.iloc[0]["asian_total"] - asian_hispanic
                values.append(asian)
                values.append(asian_hispanic)

                hawaiian_hispanic = county_only_df.iloc[0][
                    "hispanic_or_latino_hawaiian_total"
                ]
                hawaiian = county_only_df.iloc[0]["hawaiian_total"] - hawaiian_hispanic
                values.append(hawaiian)
                values.append(hawaiian_hispanic)

                other_hispanic = county_only_df.iloc[0][
                    "hispanic_or_latino_some_other_race_total"
                ]
                other = (
                    county_only_df.iloc[0]["some_other_race_alone_total"]
                    - other_hispanic
                )
                values.append(other)
                values.append(other_hispanic)

                two_or_more_hispanic = county_only_df.iloc[0][
                    "hispanic_or_latino_two_or_more_races_total"
                ]
                two_or_more = (
                    county_only_df.iloc[0]["two_more_races_total"]
                    - two_or_more_hispanic
                )
                values.append(two_or_more)
                values.append(two_or_more_hispanic)

                data_dict = {
                    "Race": [
                        "White",
                        "White",
                        "Black",
                        "Black",
                        "Native American",
                        "Native American",
                        "Asian",
                        "Asian",
                        "Hawaiian",
                        "Hawaiian",
                        "Other",
                        "Other",
                        "Two or More",
                        "Two or More",
                    ],
                    "Ethnicity": [
                        # white
                        "Non Hispanic/Latino",
                        "Hispanic/Latino",
                        # black
                        "Non Hispanic/Latino",
                        "Hispanic/Latino",
                        # native
                        "Non Hispanic/Latino",
                        "Hispanic/Latino",
                        # asian
                        "Non Hispanic/Latino",
                        "Hispanic/Latino",
                        # hawaiian
                        "Non Hispanic/Latino",
                        "Hispanic/Latino",
                        # other
                        "Non Hispanic/Latino",
                        "Hispanic/Latino",
                        # two or more
                        "Non Hispanic/Latino",
                        "Hispanic/Latino",
                    ],
                    "Population": values,
                }

                viz_df = pd.DataFrame(data_dict)

                fig = px.sunburst(
                    viz_df,
                    path=["Race", "Ethnicity"],
                    values="Population",
                    color="Race",
                    color_discrete_sequence=px.colors.sequential.Blues_r,
                )

                st.plotly_chart(fig, use_container_width=False)

            #############################
            # Strong and Healthy Families
            #############################

            st.header("Strong and Healthy Families")

            fin_being, housing, health = st.tabs(
                ["Financial Wellbeing", "Housing", "Health"]
            )

            with fin_being:

                col1, col2 = st.columns([1.5, 2.5])

                with col1:

                    st.markdown("##### Income")

                    get_metric(
                        "Income 20%",
                        "income_20_percentile",
                        county_only_df,
                        averages,
                        "${0:,.0f}",
                    )
                    get_metric(
                        "Median Family Income",
                        "median_family_income",
                        county_only_df,
                        averages,
                        "${0:,.0f}",
                    )
                    get_metric(
                        "Income 80%",
                        "income_80_percentile",
                        county_only_df,
                        averages,
                        "${0:,.0f}",
                    )

                with col2:

                    categories = [
                        "median_family_income_white",
                        "median_family_income_black",
                        "median_family_income_indigenous",
                        "median_family_income_asian",
                        "median_family_income_hispanic",
                    ]

                    category_names = {
                        "median_family_income_white": "White",
                        "median_family_income_black": "Black",
                        "median_family_income_indigenous": "Native American",
                        "median_family_income_asian": "Asian",
                        "median_family_income_hispanic": "Hispanic/Latino",
                    }

                    labels = []
                    values = []

                    for c in categories:
                        value = county_only_df[c].values[0]

                        if value > 0:
                            labels.append(category_names[c])
                            values.append(value)

                    chart_df = pd.DataFrame({"race": labels, "value": values})

                    fig = px.bar(
                        chart_df,
                        x="race",
                        y="value",
                        title="Median Income by Race/Ethnicity",
                        color_discrete_sequence=px.colors.sequential.Blues_r,
                        labels=dict(race="", value=""),
                    )

                    st.plotly_chart(fig, use_container_width=False)

                with st.expander("Source details"):
                    st.markdown(
                        "Description: Household income at 20th, 50th, and 80th percentiles<br>"
                        "Source: ACS 5-year data, 2019",
                        unsafe_allow_html=True,
                    )

            with housing:

                st.subheader("Housing instability and homelessness")

                get_metric(
                    "Proportion Homeless Students",
                    "proportion_homeless",
                    county_only_df,
                    averages,
                    "{:.0%}",
                    "inverse",
                )

                with st.expander("Source details"):
                    st.markdown(
                        "Description: Portion of public-school children who had ever experienced housing instability in the 2018-2019 school year<br>"
                        'Source: <a href="https://www2.ed.gov/about/inits/ed/edfacts/data-files/school-status-data.html">US Department of Education</a>',
                        unsafe_allow_html=True,
                    )

            with health:

                col1, col2 = st.columns([1.5, 2.5])

                with col1:
                    st.markdown("##### Access to and utilization of health services")
                    get_metric(
                        "HPSA Score",
                        "HPSA Score",
                        county_only_df,
                        averages,
                        "{:.2f}",
                        delta_color="inverse",
                    )

                    st.markdown("##### Neonatal Health")
                    get_metric(
                        "Low Birth Rate",
                        "low_birth_rate",
                        county_only_df,
                        averages,
                        "{:.0%}",
                        delta_color="inverse",
                    )

                with col2:
                    categories = [
                        "Not Hispanic or Latino_low_birth_rate",
                        "Hispanic or Latino_low_birth_rate",
                        "Unknown or Not Stated_low_birth_rate",
                        "Black or African American_low_birth_rate",
                        "White_low_birth_rate",
                        "Asian_low_birth_rate",
                        "More than one race_low_birth_rate",
                        "American Indian or Alaska Native_low_birth_rate",
                        "Native Hawaiian or Other Pacific Islander_low_birth_rate",
                    ]

                    category_names = {
                        "White_low_birth_rate": "White",
                        "Black or African American_low_birth_rate": "Black",
                        "American Indian or Alaska Native_low_birth_rate": "Indiginous",
                        "Asian_low_birth_rate": "Asian",
                        "Hispanic or Latino_low_birth_rate": "Hispanic/Latino",
                        "Not Hispanic or Latino_low_birth_rate": "Non Hispanic/Latino",
                        "Unknown or Not Stated_low_birth_rate": "Unknown/Not stated",
                        "More than one race_low_birth_rate": "More than 1 race",
                        "Native Hawaiian or Other Pacific Islander_low_birth_rate": "Hawaiian/Islander",
                    }

                    labels = []
                    values = []

                    for c in categories:
                        value = county_only_df[c].values[0]

                        if value > 0:
                            labels.append(category_names[c])
                            values.append(value)

                    # not all counties have data
                    if len(values) > 0:
                        chart_df = pd.DataFrame({"race": labels, "value": values})

                        fig = px.bar(
                            chart_df,
                            x="race",
                            y="value",
                            color_discrete_sequence=px.colors.sequential.Blues_r,
                            title="Low Birth Rate by Race/Ethnicity",
                            labels=dict(race="", value=""),
                        )

                        st.plotly_chart(fig, use_container_width=False)

                with st.expander("Source details"):
                    st.markdown(
                        "*Health Professional Shortage Area ranking for primary care providers*<br>"
                        'Source: <a href="https://data.hrsa.gov/data/download">Health Resources & Services Administration</a>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        "*Share of low-weight births*<br>"
                        'Source: <a href="https://wonder.cdc.gov/natality-expanded-current.html">Center for Disease Control </a>',
                        unsafe_allow_html=True,
                    )

            #############################
            # Supportive Communities
            #############################

            st.header("Supportive Communities")

            local_gov, neighborhoods, safety = st.tabs(
                ["Local Governance", "Neighborhoods", "Safety"]
            )

            with local_gov:

                st.markdown("##### Political participation")

                get_metric(
                    "Eligible population who turn out to vote",
                    "proportion_voter",
                    county_only_df,
                    averages,
                    "{:.0%}",
                )

                with st.expander("Source details"):
                    st.markdown(
                        "Description: Share of the voting eligible population who turn out to vote<br>"
                        'Source: MIT Election Data and Science Lab for 2020 Election pulled from the <a href="https://dataverse.harvard.edu/file.xhtml?fileId=6100388&version=1.1">Harvard Dataverse</a> aand American Community Survey 2020 5-year data<br>'
                        "Notes: This measures the share of the voting-eligible population who voted in the most recent presidential election.",
                        unsafe_allow_html=True,
                    )

            with neighborhoods:

                col1, col2 = st.columns([1.5, 2.5])

                with col1:

                    st.markdown("##### Economic inclusion")

                    st.metric(
                        "People in Poverty",
                        value="{:,}".format(
                            int(county_only_df["all_in_poverty"].values[0])
                        ),
                        delta_color="inverse",
                    )

                    get_metric(
                        "Proportion high poverty neighborhood",
                        "proportion_high_poverty_neighborhood",
                        county_only_df,
                        averages,
                        "{0:.0%}",
                        delta_color="inverse",
                    )

                    st.markdown("##### Transportation Access")

                    get_metric(
                        "Transit Trips Index",
                        "transit_trips_index",
                        county_only_df,
                        averages,
                        "{0:.2f}",
                    )
                    get_metric(
                        "Transit Trips Cost",
                        "transit_low_cost_index",
                        county_only_df,
                        averages,
                        "{0:.2f}",
                    )

                with col2:

                    categories = [
                        "hispanic_or_latino_exposure",
                        "white_exposure",
                        "black_exposure",
                        "native_american_exposure",
                        "asian_exposure",
                        "hawaiian_exposure",
                        "some_other_race_alone_exposure",
                        "two_more_races_exposure",
                    ]

                    category_names = {
                        "white_exposure": "White",
                        "black_exposure": "Black",
                        "native_american_exposure": "Native American",
                        "asian_exposure": "Asian",
                        "hispanic_or_latino_exposure": "Hispanic/Latino",
                        "hawaiian_exposure": "Hawaiian",
                        "some_other_race_alone_exposure": "Other race",
                        "two_more_races_exposure": "Two or more races",
                    }

                    labels = []
                    values = []

                    for c in categories:
                        value = county_only_df[c].values[0]

                        if value > 0:
                            labels.append(category_names[c])
                            values.append(value)

                    chart_df = pd.DataFrame({"race": labels, "value": values})

                    fig = px.bar(
                        chart_df,
                        x="race",
                        y="value",
                        title="Racial Exposure Index",
                        color_discrete_sequence=px.colors.sequential.Blues_r,
                        labels=dict(race="", value=""),
                    )

                    st.plotly_chart(fig, use_container_width=False)

                with st.expander("Source details"):
                    st.markdown(
                        "*People in Poverty*<br>"
                        "Description:  Share of county residents experiencing poverty that live in high-poverty neighborhoods (a neighborhood is defined as a census tract).  A high-poverty neighborhood is one in which over 40 percent of the residents are experiencing poverty.<br>"
                        "Source: American Community Survey (ACS) 5-year data, 2019",
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        "*Racial Diversity*<br>"
                        "Description: Neighborhood exposure index, or share of a person’s neighbors who are people of other races and ethnicities<br>"
                        "Source: ACS 5-year data, 2019<br>"
                        "Notes: This is a set of metrics constructed separately for each racial/ethnic group and reports the average share of that group's neighbors who are members of other racial/ethnic groups. This is a type of exposure index. For example, an exposure index of 80% in “Hispanic or Latino“' means that the average Hispanic or Latino resident has 80% of their neighbors within a census tract who have a different ethnicity than them. The higher the value, the more exposed to people of different races/ethnicities.",
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        "*Transportation access*<br>"
                        "Description: Transit Index<br>"
                        'Source: Department of Housing and Urban Development Accessed via <a href="https://hudgis-hud.opendata.arcgis.com/datasets/location-affordability-index-v-3/api">API</a><br>'
                        "Notes: Converted the transit trips index (hh6_transit_trips_renters) given to percentile ranked nationally "
                        "and inverted the transity cost index (hh6_t_renters) then converted to a percentile ranked nationally.<br>"
                        "Interpretation: Higher scores reflect better access to public transportation.",
                        unsafe_allow_html=True,
                    )

            with safety:

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("##### Exposure to crime")
                    get_metric(
                        "Violent crime",
                        "crime_rate",
                        county_only_df,
                        averages,
                        "{0:.2f}",
                        delta_color="inverse",
                    )
                    st.markdown("*per 100k residents*")

                with col2:
                    st.markdown("##### Overly punitive policing")
                    get_metric(
                        "Juvenile Crime Rate",
                        "juvenile_crime_rate",
                        county_only_df,
                        averages,
                        "{0:.2f}",
                        delta_color="inverse",
                    )
                    st.markdown("*per 100k residents*")

                with st.expander("Source details"):
                    st.markdown(
                        "*Exposure to crime*<br>"
                        "Description: Rates of reported violent crime<br>"
                        "Source: Federal Bureau of Investigations (FBI) Uniform Crime Statistic (UCR) Crime in the United States, 2019, accessed via <a href='http://api.usa.gov/'>api.usa.gov</a>; American Community Survey 5-year data, 2019<br>"
                        "Notes:  Violent crime is composed of four offenses: murder and nonnegligent manslaughter, rape, robbery, and aggravated assault. Rates are calculated as the number of reported crimes per 100,000 people. The FBI cautions using UCR data to rank or compare locales because this can create, ‘misleading perceptions which adversely affect geographic entities and their residents.’",
                        unsafe_allow_html=True,
                    )

            #############################
            # Opportunities to Learn and Earn
            #############################

            st.header("Opportunities to Learn and Earn")

            education, work = st.tabs(["Education", "Work"])

            with education:

                col1, col2 = st.columns([1.5, 2.5])

                with col1:
                    st.markdown("##### Access to preschool")
                    get_metric(
                        "Preschool enrollment",
                        "preschool_enroll",
                        county_only_df,
                        averages,
                        "{:.0%}",
                    )
                    st.metric(
                        "PreK-12 enrollment",
                        value="{:,}".format(
                            int(county_only_df["public_students_pre_12"].values[0])
                        ),
                    )
                    st.markdown("##### Effective Education")
                    get_metric(
                        "Avg change in English LA Proficiency in 3-8",
                        "avg_edu_prof_diff",
                        county_only_df,
                        averages,
                        "{0:,.1f}",
                    )

                with col2:
                    categories = [
                        "preschool_enrollment_white",
                        "preschool_enrollment_black",
                        "preschool_enrollment_hispanic",
                        "preschool_enrollment_indigenous",
                        "preschool_enrollment_asian",
                    ]

                    category_names = {
                        "preschool_enrollment_white": "White",
                        "preschool_enrollment_black": "Black",
                        "preschool_enrollment_indigenous": "Indigenous",
                        "preschool_enrollment_asian": "Asian",
                        "preschool_enrollment_hispanic": "Hispanic/Latino",
                    }

                    labels = []
                    values = []

                    for c in categories:
                        value = county_only_df[c].values[0]

                        if value > 0:
                            labels.append(category_names[c])
                            values.append(value)

                    chart_df = pd.DataFrame({"race": labels, "value": values})

                    fig = px.bar(
                        chart_df,
                        x="race",
                        y="value",
                        title="Proportion of PreK Students who Identify as a Given Race/Ethnicity",
                        color_discrete_sequence=px.colors.sequential.Blues_r,
                        labels=dict(race="", value=""),
                    )

                    st.plotly_chart(fig, use_container_width=False)

                with st.expander("Source details"):

                    st.markdown(
                        "*Access to preschool*<br>"
                        "Description: Share of children enrolled in nursery school or preschool<br>"
                        "Source: ACS 5-year data, 2019<br><br>"
                        """ *Effective Education*<br>Description: Average per-grade change in English Language Arts Achievement, between third and eighth grades<br>
                        Source: <a href="https://www2.ed.gov/about/inits/ed/edfacts/data-files/index.html">US Department of Education</a>, 2018-2019 school year<br>
                        Notes: Calculated using weighted average for differences within the same county. <br><br>
                        """,
                        unsafe_allow_html=True,
                    )

            with work:

                col1, col2 = st.columns([1.5, 2.5])

                with col1:

                    st.markdown("##### Employment")

                    get_metric(
                        "Ages 16-64",
                        "employed_16_64_population",
                        county_only_df,
                        averages,
                        "{:.0%}",
                    )
                    get_metric(
                        "Ages 25-54",
                        "employed_25_54_population",
                        county_only_df,
                        averages,
                        "{:.0%}",
                    )

                with col2:

                    categories = [
                        "white_employed_16_64",
                        "black_employed_16_64",
                        "american_indian_employed_16_64",
                        "asian_employed_16_64",
                        "some_other_race_alone_employed_16_64",
                        "two_or_more_race_employed_16_64",
                        "hispanic_or_latino_employed_16_64",
                    ]

                    category_names = {
                        "white_employed_16_64": "White",
                        "black_employed_16_64": "Black",
                        "american_indian_employed_16_64": "Native American",
                        "asian_employed_16_64": "Asian",
                        "hispanic_or_latino_employed_16_64": "Hispanic/Latino",
                        "some_other_race_alone_employed_16_64": "Other race",
                        "two_or_more_race_employed_16_64": "Two or more races",
                    }

                    labels = []
                    values = []

                    for c in categories:
                        value = county_only_df[c].values[0]

                        if value > 0:
                            labels.append(category_names[c])
                            values.append(value)

                    chart_df = pd.DataFrame({"race": labels, "value": values})

                    fig = px.bar(
                        chart_df,
                        x="race",
                        y="value",
                        title="Employment by Race, Age 16-64",
                        color_discrete_sequence=px.colors.sequential.Blues_r,
                        labels=dict(race="", value=""),
                    )

                    st.plotly_chart(fig, use_container_width=False)

                with st.expander("Source details"):
                    st.markdown(
                        """*Employment*<br>
                            Description: Employment-to-population ratio for adults<br>
                            Source: ACS 5-year data, 2019<br>
                            Notes: Calculated using civilian population
                            """,
                        unsafe_allow_html=True,
                    )
                # with st.expander("Source details"):
                #     st.markdown('*People in Poverty*<br>'\
                #         'Description: Share of residents experiencing poverty living in high-poverty neighborhoods<br>' \
                #         'Source: ACS 5-year data',unsafe_allow_html=True)

                #     st.markdown('*Racial Diversity*<br>' \
                #         "Description: Neighborhood exposure index, or share of a person's neighbors who are people of other races and ethnicities<br>" \
                #         'Source: ACS 5-year data<br>' \
                #         'Notes: Used the <a href="https://censusscope.org/about_exposure.html">Census Scope</a> Exposure Index Formula to calculate the exposure index for each race at the tract level.',unsafe_allow_html=True)

                #     st.markdown('*Transportation access*<br>' \
                #         'Description: Transit trips index<br>' \
                #         'Source: Department of Housing and Urban Development Accessed via <a href="https://hudgis-hud.opendata.arcgis.com/datasets/location-affordability-index-v-3/api">API</a><br>' \
                #         'Assumptions: Converted the index (hh6_transit_trips_renters)  given to percentile ranked nationally<br>' \
                #         'Interpretation: Higher scores reflect better access to public transportation.',  unsafe_allow_html=True)
