import numpy as np
from typing import Any, Dict
import streamlit as st
import pandas as pd 
import altair as alt
import plotly.express as px

import wikipedia
import requests
import json


WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

# per https://stackoverflow.com/questions/30595918/is-there-any-api-to-get-image-from-wiki-page
def get_wiki_image(search_term):
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

def build_page_content(fips_code: int):
    df, averages = get_dataframe()

    county_only_df = df[df['FIPS']==int(fips_code)]

    if len(county_only_df) == 1:
        name = county_only_df.NAME.values[0]
        st.title(f"{name}")

        wiki_image = get_wiki_image(name)

        if wiki_image != 0:
            st.markdown(f'<img src="{wiki_image}" width="300" height="225" alt="Wikipedia image of {name}"/>', unsafe_allow_html=True)

        st.markdown('<a href="#population">Population</a> | <a href="#strong-and-healthy-families">Strong and Healthy Families</a> | <a href="#supportive-communities">Supportive Communities</a> | <a href="#opportunities-to-learn-and-earn">Opportunities to Learn and Earn</a>', unsafe_allow_html=True)

        #############################
        # Population
        #############################
        
        col1, col2 = st.columns([1,3])
        
        with col1:
           st.markdown('##### Population')
           st.metric("2019 Population",value = '{:,}'.format(int(county_only_df["population"].values[0])))
        
        with col2:
            categories = ['white','black','native_american','asian','hawaiian',	'some_other_race_alone','two_more_races','hispanic_or_latino']

            categories_names = {'white': 'White',
                'black': 'Black',
                'native_american': 'Native American',
                'asian': 'Asian',
                'hawaiian': 'Hawaiian',	
                'some_other_race_alone': 'Other',
                'two_more_races': 'Two or more races',
                'hispanic_or_latino': 'Hispanic/Latino'
                }

            values = []

            category_labels = []
            
            for c in categories:
                value = county_only_df[c].values[0]

                if value > 0:
                    category_labels.append(categories_names[c])
                    values.append(value)
                
            chart_df = pd.DataFrame({"race": category_labels, "value": values}) #, "labels": value_texts})
        
            fig = px.pie(
                chart_df, values="value", names='race', hole = 0.4, #width=300, height=400,
                #title='Population by Race',
                color_discrete_sequence=px.colors.sequential.Blues_r
            )

            # fig.add_annotation(x= 0.5, y = 0.5,
            #             text = 'Population by Race',
            #             showarrow = False)

            fig.update_layout(legend=dict(
                orientation="h",
                # yanchor="bottom",
                # y=1.02,
                # xanchor="left",
                # x=1
            ))

            #fig.update_layout(showlegend=False)
            #fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))            
            fig.update_traces(hovertemplate='<b>%{label}</b>') #
            
            st.plotly_chart(fig)#,use_container_width=False)

        #############################
        # Strong and Healthy Families
        #############################

        st.header('Strong and Healthy Families')

        fin_being, housing, health = st.tabs(['Financial Wellbeing','Housing','Health'])

        with fin_being:
            
            col1, col2 = st.columns([1.5,2.5])
            
            with col1:
                
                st.markdown('##### Income')
            
                get_metric("Income 20%", "income_20_percentile",  county_only_df, averages, '${0:,.0f}')
                get_metric("Median Family Income", "median_family_income", county_only_df, averages, '${0:,.0f}')
                get_metric("Income 80%", "income_80_percentile",  county_only_df, averages, '${0:,.0f}')
            
            with col2:
                
                categories = ['median_family_income_white','median_family_income_black','median_family_income_indigenous','median_family_income_asian','median_family_income_hispanic']

                category_names = {'median_family_income_white': 'White',
                    'median_family_income_black': 'Black',
                    'median_family_income_indigenous': 'Native American',
                    'median_family_income_asian': 'Asian',
                    'median_family_income_hispanic': 'Hispanic/Latino'
                    }

                labels = []
                values = []

                for c in categories:
                    value = county_only_df[c].values[0]
                    
                    if value > 0:
                        labels.append(category_names[c])
                        values.append(value)
                    
                chart_df = pd.DataFrame({"race": labels, "value": values})         

                fig = px.bar(chart_df, 
                    x='race', 
                    y='value',
                    title='Median Income by Race/Ethnicity',
                    color_discrete_sequence=px.colors.sequential.Blues_r,
                    labels=dict(race="", value="")
                )

                st.plotly_chart(fig,use_container_width=False)

            with st.expander("Source details"):
                st.write('Description: Household income at 20th, 50th, and 80th percentiles')
                st.write('Source: ACS 5-year data')

        with housing:
                 
            st.subheader('Housing instability and homelessness')

            get_metric("Proportion Homeless Students","proportion_homeless", county_only_df, averages, '{:.0%}', 'inverse')
        
            with st.expander("Source details"):
                st.write('Description: Portion of public-school children who are ever homeless during the school year')
                st.markdown('Source: <a href="https://www2.ed.gov/about/inits/ed/edfacts/data-files/school-status-data.html">US Department of Education</a>',unsafe_allow_html=True)
                st.write("Notes: See appendix")
                
        with health:
            
            col1, col2 = st.columns([1.5,2.5])

            with col1:
                st.markdown('##### Access to and utilization of health services')
                get_metric("HPSA Score","HPSA Score", county_only_df, averages, '{:.2f}', delta_color='inverse')

                st.markdown('##### Neonatal Health')
                get_metric("Low Birth Rate","low_birth_rate", county_only_df, averages, '{:.0%}',delta_color='inverse')

            with col2:
                categories = ['Not Hispanic or Latino_low_birth_rate','Hispanic or Latino_low_birth_rate','Unknown or Not Stated_low_birth_rate','Black or African American_low_birth_rate','White_low_birth_rate','Asian_low_birth_rate','More than one race_low_birth_rate','American Indian or Alaska Native_low_birth_rate','Native Hawaiian or Other Pacific Islander_low_birth_rate']

                category_names = {'White_low_birth_rate': 'White',
                    'Black or African American_low_birth_rate': 'Black',
                    'American Indian or Alaska Native_low_birth_rate': 'Indiginous',
                    'Asian_low_birth_rate': 'Asian',
                    'Hispanic or Latino_low_birth_rate': 'Hispanic/Latino',
                    'Not Hispanic or Latino_low_birth_rate': 'Non Hispanic/Latino',
                    'Unknown or Not Stated_low_birth_rate': 'Unknown/Not stated',
                    'More than one race_low_birth_rate': 'More than 1 race',
                    'Native Hawaiian or Other Pacific Islander_low_birth_rate': 'Hawaiian/Islander'
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

                    fig = px.bar(chart_df, x='race', y='value',
                        color_discrete_sequence=px.colors.sequential.Blues_r,
                        title='Low Birth Rate by Race/Ethnicity',
                        labels=dict(race="", value="")
                        )

                    st.plotly_chart(fig,use_container_width=False)

            with st.expander("Source details"):
                st.write('Health Professional Shortage Area ranking for primary care providers')
                st.markdown('Source: <a href="https://data.hrsa.gov/data/download">Health Resources & Services Administration</a>',unsafe_allow_html=True)
                st.write('Share of low-weight births')
                st.markdown('Source: <a href="https://wonder.cdc.gov/natality-expanded-current.html">Center for Disease Control </a>',unsafe_allow_html=True)

        #############################
        # Supportive Communities
        #############################

        st.header('Supportive Communities')

        local_gov, neighborhoods, safety = st.tabs(['Local Governance','Neighborhoods','Safety'])

        with local_gov:
            
            st.markdown('##### Political participation')

            get_metric("Eligible population who turn out to vote","proportion_voter", county_only_df, averages, '{:.0%}')
        
            with st.expander("Source details"):
                st.write('Description: Share of the voting eligible population who turn out to vote')
                st.markdown('Source: <a href="https://dataverse.harvard.edu/file.xhtml?fileId=6100388&version=1.1">Harvard Dataverse</a> and ACS 5-year data',unsafe_allow_html=True)
                st.write("Notes: This is voter turnout for the 2020 presidential election. There are overvote and undervote numbers but validity of the vote was not the focus, but rather that a ballot was cast (turnout), therefore vote total was used.")

        with neighborhoods:

            col1, col2 = st.columns([1.5,2.5])
            
            with col1:
                
                st.markdown('##### Economic inclusion')
            
                st.metric("People in Poverty", 
                    value = '{:,}'.format(int(county_only_df["all_in_poverty"].values[0])), 
                    delta_color='inverse'
                )

                
                get_metric("Proportion high poverty neighborhood", "proportion_high_poverty_neighborhood", county_only_df, averages, '{0:.0%}', delta_color='inverse')

                st.markdown('##### Transportation Access')

                get_metric("Transit Trips Index", "transit_trips_index", county_only_df, averages, '{0:.2f}')
                get_metric("Transit Trips Cost", "transit_low_cost_index", county_only_df, averages, '{0:.2f}')
            
            with col2:
                
                categories = ['hispanic_or_latino_exposure','white_exposure','black_exposure','native_american_exposure','asian_exposure','hawaiian_exposure','some_other_race_alone_exposure','two_more_races_exposure']

                category_names = {'white_exposure': 'White',
                    'black_exposure': 'Black',
                    'native_american_exposure': 'Native American',
                    'asian_exposure': 'Asian',
                    'hispanic_or_latino_exposure': 'Hispanic/Latino',
                    'hawaiian_exposure': 'Hawaiian',
                    'some_other_race_alone_exposure': 'Other race',
                    'two_more_races_exposure': 'Two or more races'
                }

                labels = []
                values = []

                for c in categories:
                    value = county_only_df[c].values[0]

                    if value > 0:
                        labels.append(category_names[c])
                        values.append(value)
                    
                chart_df = pd.DataFrame({"race": labels, "value": values})         

                fig = px.bar(chart_df, 
                    x='race', 
                    y='value',
                    title='Racial Exposure Index',
                    color_discrete_sequence=px.colors.sequential.Blues_r,
                    labels=dict(race="", value="")
                )

                st.plotly_chart(fig,use_container_width=False)

            with st.expander("Source details"):
                st.markdown('*People in Poverty*<br>'\
                    'Description: Share of residents experiencing poverty living in high-poverty neighborhoods<br>' \
                    'Source: ACS 5-year data',unsafe_allow_html=True)

                st.markdown('*Racial Diversity*<br>' \
                    'Description: Neighborhood exposure index, or share of a person’s neighbors who are people of other races and ethnicities<br>' \
                    'Source: ACS 5-year data<br>' \
                    'Notes: Used the <a href="https://censusscope.org/about_exposure.html">Census Scope</a> Exposure Index Formula to calculate the exposure index for each race at the tract level.',unsafe_allow_html=True)
                
                st.markdown('*Transportation access*<br>' \
                    'Description: Transit trips index<br>' \
                    'Source: Department of Housing and Urban Development Accessed via <a href="https://hudgis-hud.opendata.arcgis.com/datasets/location-affordability-index-v-3/api">API</a><br>' \
                    'Assumptions: Converted the index (hh6_transit_trips_renters)  given to percentile ranked nationally<br>' \
                    'Interpretation: Higher scores reflect better access to public transportation.',  unsafe_allow_html=True)


        with safety:
            
            col1, col2 = st.columns(2)

            with col1:
                st.markdown('##### Exposure to crime')
                get_metric("Violent crime","crime_rate", county_only_df, averages, '{0:.2f}', delta_color='inverse')
                st.markdown('*per 100k residents*')
           
            with col2:
                st.markdown('##### Overly punitive policing')
                get_metric("Juvenile Crime Rate","juvenile_crime_rate", county_only_df, averages, '{0:.2f}', delta_color='inverse')
                st.markdown('*per 100k residents*')

            with st.expander("Source details"):
                st.markdown('*Exposure to crime*<br>' \
                    'Description: Rates of reported violent crime<br>' \
                    'Source: <a href="http://api.usa.gov/">api.usa.gov</a><br>' \
                    'Assumptions: To calculate the rate of crime per 100k residents the ACS population data was used for each city',unsafe_allow_html=True)

        #############################
        # Opportunities to Learn and Earn
        #############################

        st.header('Opportunities to Learn and Earn')

        education, work = st.tabs(['Education','Work'])

        with education:
            
            col1, col2 = st.columns([1.5,2.5])
            
            with col1:
                st.markdown('##### Access to preschool')
                get_metric("Preschool enrollment","preschool_enroll", county_only_df, averages, '{:.0%}')
                st.metric("PreK-12 enrollment", 
                    value = '{:,}'.format(int(county_only_df["public_students_pre_12"].values[0]))
                )

            with col2:
                categories = ['preschool_enrollment_white','preschool_enrollment_black','preschool_enrollment_hispanic','preschool_enrollment_indigenous','preschool_enrollment_asian']

                category_names = {'preschool_enrollment_white': 'White',
                    'preschool_enrollment_black': 'Black',
                    'preschool_enrollment_indigenous': 'Indigenous',
                    'preschool_enrollment_asian': 'Asian',
                    'preschool_enrollment_hispanic': 'Hispanic/Latino'
                }

                labels = []
                values = []

                for c in categories:
                    value = county_only_df[c].values[0]

                    if value > 0:
                        labels.append(category_names[c])
                        values.append(value)
                    
                chart_df = pd.DataFrame({"race": labels, "value": values})         

                fig = px.bar(chart_df, 
                    x='race', 
                    y='value',
                    title='PreK Enrollment by Race/Ethnicity',
                    color_discrete_sequence=px.colors.sequential.Blues_r,
                    labels=dict(race="", value="")
                )

                st.plotly_chart(fig,use_container_width=False)

            with st.expander("Source details"):
                
                 st.markdown('*Access to preschool*<br>' \
                    'Description: Share of children enrolled in nursery school or preschool<br>' \
                    'Source: ACS 5-year data',  unsafe_allow_html=True)

        with work:

            col1, col2 = st.columns([1.5,2.5])
            
            with col1:
                
                st.markdown('##### Employment')
                
                get_metric("Ages 16-64","employed_16_64_population", county_only_df, averages, '{:.0%}')
                get_metric("Ages 25-54","employed_25_54_population", county_only_df, averages, '{:.0%}')
            
            with col2:
                
                categories = ['white_employed_16_64','black_employed_16_64','american_indian_employed_16_64','asian_employed_16_64','some_other_race_alone_employed_16_64','two_or_more_race_employed_16_64','hispanic_or_latino_employed_16_64']

                category_names = {'white_employed_16_64': 'White',
                    'black_employed_16_64': 'Black',
                    'american_indian_employed_16_64': 'Native American',
                    'asian_employed_16_64': 'Asian',
                    'hispanic_or_latino_employed_16_64': 'Hispanic/Latino',
                    'some_other_race_alone_employed_16_64': 'Other race',
                    'two_or_more_race_employed_16_64': 'Two or more races'
                }

                labels = []
                values = []

                for c in categories:
                    value = county_only_df[c].values[0]

                    if value > 0:
                        labels.append(category_names[c])
                        values.append(value)
                    
                chart_df = pd.DataFrame({"race": labels, "value": values})         

                fig = px.bar(chart_df, 
                    x='race', 
                    y='value',
                    title='Employment by Race, Age 16-64',
                    color_discrete_sequence=px.colors.sequential.Blues_r,
                    labels=dict(race="", value="")
                )

                st.plotly_chart(fig,use_container_width=False)

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

################################
# page start             
################################

def get_parameter(name, default_value):
    url_params = st.experimental_get_query_params()

    param_value = default_value

    if name in url_params and len(url_params[name][0])>0:
        param_value = url_params[name][0]

    return param_value

url_params = st.experimental_get_query_params()

fips_parameter = 'fips'

fips_code = ''

if fips_parameter in url_params:
    fips_code = url_params[fips_parameter][0]
    
    if len(fips_code) > 0 and fips_code.isnumeric():
       build_page_content(fips_code)
    else:
        st.title(f"Cant find any data for {fips_code}")
else:
    import streamlit as st
    import pandas as pd
    import altair as alt

    url = ''
    
    debug = get_parameter('debug','false')

    if debug =='true':
         url = 'http://localhost:8501/?fips='
    else:
         #url = 'https://upwardmobility.pythonanywhere.com/county-details?fips='
         url = 'https://davidhcoe-mads697-county-details-pr63wa.streamlitapp.com/?fips='

    def get_url(row):
        row['url'] = url + str(row['id'])

        return row

    counties_df = pd.read_csv('counties_merged.csv')
    county_display_df = counties_df[['NAME','FIPS']]
    county_display_df.columns = ['NAME','id']
    county_display_df['url'] = ''
    county_display_df = county_display_df.apply(get_url, axis=1)

    def get_map(metric):
        counties = alt.topo_feature('https://cdn.jsdelivr.net/npm/vega-datasets@v1.29.0/data/us-10m.json', 'counties')

        c = alt.Chart(counties).mark_geoshape(
            stroke='#706545', strokeWidth=0.5
        ).encode(
            color=metric+':Q',
            tooltip=['NAME:N'],
            href='url:N'
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(county_display_df, 'id', ['NAME', 'url'])
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(counties_df, 'FIPS', [metric])
        ).project(
            type='albersUsa'
        ).properties(
            width=900,
            height=500
        )

        return c

    metric = get_parameter('metric','population')

    c = get_map(metric)
    
    st.altair_chart(c)
