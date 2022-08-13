import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from utilities import get_dataframe, get_parameter, PREFERRED_METRICS

def show_county_picker_page():

    cached_df,_ = get_dataframe()

    url = ''

    debug = get_parameter('debug','false')

    if debug =='true':
        url = 'http://localhost:8501/?fips='
    else:
        url = 'https://davidhcoe-mads697-main-1sf12v.streamlitapp.com/?fips='

    def get_url(row):
        row['url'] = url + str(row['id'])
        return row

    df = cached_df.copy()
    df['HPSA Score'] = df['HPSA Score'].fillna(0) # I think this means that it doesn't have HPSA shortage
    county_display_df = df[['NAME','FIPS']]
    county_display_df.columns = ['NAME','id']
    county_display_df['url'] = ''
    county_display_df = county_display_df.apply(get_url, axis=1)

    def get_map(ranking_df):
        counties = alt.topo_feature('https://cdn.jsdelivr.net/npm/vega-datasets@v1.29.0/data/us-10m.json', 'counties')

        c = alt.Chart(counties).mark_geoshape(
            stroke='#706545', strokeWidth=0.5
        ).encode(
            color=alt.Color('ranking:Q', legend=alt.Legend(title="")),
            tooltip=['NAME:N', 'ranking:Q'],
            href='url:N'
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(county_display_df, 'id', ['NAME', 'url'])
        ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(ranking_df, 'FIPS', ['ranking'])
        ).project(
            type='albersUsa'
        ).properties(
            width=900,
            height=500
        )


        background = alt.Chart(counties).mark_geoshape(
            fill='#ededed',
            stroke='white'
        ).project('albersUsa')

        return background + c

    feature_names = PREFERRED_METRICS
    ideal_scores =  {
        'proportion_homeless': df['proportion_homeless'].min(),
        'HPSA Score':  df['HPSA Score'].min(),
        'low_birth_rate':  df['low_birth_rate'].min(),
        'proportion_voter': df['proportion_voter'].max(),
        'proportion_high_poverty_neighborhood': df['proportion_high_poverty_neighborhood'].min(),
        'hispanic_or_latino_exposure': .5,
        'white_exposure': .5,
        'black_exposure': .5,
        'native_american_exposure':.5,
        'transit_trips_index': df['transit_trips_index'].max(),
        'transit_low_cost_index': df['transit_low_cost_index'].max(),
        'crime_rate': df['crime_rate'].min(),
        'juvenile_crime_rate': df['juvenile_crime_rate'].min(),
        'avg_edu_prof_diff': df['avg_edu_prof_diff'].max(),
        'preschool_enroll': df['preschool_enroll'].max(),
        'employed_25_54_population': df['employed_25_54_population'].max(),
        'median_family_income': df['median_family_income'].max(),
        'income_20_percentile': df['income_20_percentile'].max(),
        'income_80_percentile': df['income_80_percentile'].max(),
    }

    options = [0,10,20,30,40,50,60,70,80,100]

    col1, col2 = st.columns(2)

    with col1:
        choice1_select = st.selectbox('Option 1', feature_names.keys())

    with col2:
        choice1 = st.select_slider(
            '',
            options=options)


    col1, col2 = st.columns(2)

    with col1:
        choice2_select = st.selectbox('Option 2', feature_names.keys())

    with col2:
        choice2= st.select_slider(
            '',
            key='2',
            options=options)


    col1, col2 = st.columns(2)

    with col1:
        choice3_select = st.selectbox('Option 3', feature_names.keys())

    with col2:
        choice3 = st.select_slider(
            '',
            key='3',
            options=options)

    if st.button('Choose my County'):
        if choice1 + choice2 + choice3 != 100:
            st.write('The values must add up to 100')
        else:
            if choice1_select == choice2_select or choice2_select == choice3_select or choice1_select == choice3_select:
                st.write('Your choices must be unique')
            else:
    
                input1, input2, input3 = feature_names[choice1_select],feature_names[choice2_select],feature_names[choice3_select]

                metrics = [
                'median_family_income',
                'income_20_percentile',
                'income_80_percentile',
                'year',
                'employed_25_54_population',
                'preschool_enroll',
                'avg_edu_prof_diff',
                'low_birth_rate',
                'HPSA Score',
                'proportion_homeless',
                'proportion_voter',
                'transit_trips_index',
                'transit_low_cost_index',
                'crime_rate',
                'juvenile_crime_rate',
                'hispanic_or_latino_exposure',
                'white_exposure',
                'black_exposure',
                'native_american_exposure',
                'proportion_high_poverty_neighborhood']

                mean_values=df[metrics].mean()
                df[metrics] = df[metrics].fillna(mean_values)

                inputs = [input1, input2, input3]
                ideals = [ideal_scores[input1], ideal_scores[input2], ideal_scores[input3]]
                weights = [choice1, choice2, choice3]
                ranking_df = df[['NAME','FIPS', input1,input2,input3]]

                new_names= []

                for ind in range(0,3):
                    distance_from_ideal = np.abs(ranking_df[inputs[ind]]-ideals[ind])
                    high = max(distance_from_ideal)
                    low = min(distance_from_ideal)
                    ranking_df[inputs[ind] + '_scaled'] = (1-(distance_from_ideal - low)/(high - low))*100
                    new_names.append(inputs[ind] + '_scaled')

                ranking_df['ranking']=choice1/100*ranking_df[new_names[0]] + choice2/100*ranking_df[new_names[1]] + choice3/100*ranking_df[new_names[2]]

                sorted_ranking_df = ranking_df.sort_values('ranking',ascending=False).head(5)
                c = get_map(ranking_df)
                st.title('Ranked Counties Based on Selected Preferred Metrics')
                st.altair_chart(c)
                st.dataframe(sorted_ranking_df)
