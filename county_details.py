from email.policy import default
from typing import Any, Dict
import streamlit as st
import pandas as pd 
import altair as alt
import queries

@st.cache(suppress_st_warning=True)
def get_dataframe():
    df = pd.read_csv('counties_merged.csv')

    averages = {}

    feature_names = ['population','white','black','native_american','asian','hawaiian','some_other_race_alone','two_more_races','hispanic_or_latino',
                 'white_employed_16_64', 'black_employed_16_64',  'american_indian_employed_16_64', 'asian_employed_16_64', 'some_other_race_alone_employed_16_64',
                 'two_or_more_race_employed_16_64', 'hispanic_or_latino_employed_16_64', 'employed_25_54_population', 'employed_16_64_population',
                 'median_family_income','income_20_percentile','income_80_percentile','median_family_income_white','median_family_income_black',
                 'median_family_income_indigenous','median_family_income_asian','median_family_income_hispanic',
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
        st.title(f"{county_only_df.NAME.values[0]}")

        st.write(county_only_df)

        st.write(f'''
                #### Racial Mix         
            ''')

        categories = ['white','black','native_american','asian','hawaiian',	'some_other_race_alone','two_more_races','hispanic_or_latino']

        values = []

        value_texts = []

        for c in categories:
            value = county_only_df[c].values[0]
            values.append(value)
            value_texts.append('{:.0%}'.format(value))

        chart_df = pd.DataFrame({"race": categories, "value": values, "labels": value_texts})

        base = alt.Chart(chart_df).encode(
            theta=alt.Theta(field="value", type="quantitative"),
            color=alt.Color(field="race", type="nominal"),
        )

        pie = base.mark_arc(outerRadius=120)
        text = base.mark_text(radius=140, size=20,color='black').encode(text="labels:N")

        c = pie + text

        st.altair_chart(c)

        domain_cols_corr = {
            "Financial wellbeing": ["median_family_income", "income_20_percentile", "income_80_percentile"],
            "Education": ['preschool_enroll','avg_edu_prof_diff'],
            
                "Neighborhoods":['proportion_high_poverty_neighborhood','transit_trips_index','transit_low_cost_index'],
                "Housing": ["HOM_STUDENTS","proportion_homeless"],
                
                "Health": ['low_birth_rate','HPSA Score'],
                "Safety": ["crime_rate"],
                
                "Local governance": ["proportion_voter"]
            }

           
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f'''
                #### Financial Wellbeing         
            ''')

            get_metric("Median Family Income", "median_family_income", county_only_df, averages, '${0:,.0f}')
            get_metric("Income 20%", "income_20_percentile",  county_only_df, averages, '${0:,.0f}')
            get_metric("Income 80%", "income_80_percentile",  county_only_df, averages, '${0:,.0f}')
            
        with col2:
            st.write(f'''
                #### Education    
            ''')

            get_metric("Preschool enrollment","preschool_enroll", county_only_df, averages, '{:.0%}')
            get_metric("Avg Edu Prof Diff", "avg_edu_prof_diff", county_only_df, averages)

        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f'''
                #### Neighborhoods    
            ''')

            get_metric("Proportion High Poverty","proportion_high_poverty_neighborhood", county_only_df, averages, '{:.0%}', 'inverse')
            get_metric("Transit Trips", "transit_trips_index", county_only_df, averages)
            get_metric("Low Cost Transit", "transit_low_cost_index", county_only_df, averages)
       
        with col2:
            st.write(f'''
                #### Housing    
            ''')
            
            get_metric("Homeless Students","HOM_STUDENTS", county_only_df, averages, delta_color='inverse')
            get_metric("Proportion homeless","proportion_homeless", county_only_df, averages, '{:.0%}', 'inverse')
            
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f'''
                #### Health    
            ''')

            st.metric("Low Birth Rate",
                    value = '{:.0%}'.format(county_only_df["low_birth_rate"].values[0]))

            st.metric("HPSA Score",
                    value = county_only_df["HPSA Score"].values[0])

        with col2:
            st.write(f'''
                #### Crime    
            ''')

            st.metric("Violent Crime Rate",
                    value = county_only_df["low_birth_rate"].values[0])

################################
# page start             
################################

# st.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

# st.write("""
# <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
#   <a class="navbar-brand" href="https://youtube.com/dataprofessor" target="_blank">Data Professor</a>
#   <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
#     <span class="navbar-toggler-icon"></span>
#   </button>
#   <div class="collapse navbar-collapse" id="navbarNav">
#     <ul class="navbar-nav">
#       <li class="nav-item active">
#         <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
#       </li>
#       <li class="nav-item">
#         <a class="nav-link" href="https://youtube.com/dataprofessor" target="_blank">YouTube</a>
#       </li>
#       <li class="nav-item">
#         <a class="nav-link" href="https://twitter.com/thedataprof" target="_blank">Twitter</a>
#       </li>
#     </ul>
#   </div>
# </nav>
# """, unsafe_allow_html=True)

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
         url = 'https://upwardmobility.pythonanywhere.com/county-details?fips='

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

        c = alt.Chart(counties).mark_geoshape().encode(
            color=metric+':Q',
            tooltip=['NAME:N', 'url:N'],
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
            width=500,
            height=300
        )

        return c

    # metric = 'population'
    # metric_param = 'metric'
    
    metric = get_parameter('metric','population')

    #if metric_param in url_params and len(url_params[metric_param][0])>0:
    #    metric = url_params[metric_param][0]

    c = get_map(metric)
    st.altair_chart(c)
