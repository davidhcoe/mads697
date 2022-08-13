import streamlit as st
import pandas as pd
import numpy as np
from utilities import get_dataframe

def show_county_picker_page():
    feature_names = {
        'HPSA Score': 'HPSA Score', 
        'Low Birth Rate': 'low_birth_rate',
        'Avg Edu Prof': 'avg_edu_prof_diff'
    }

    ideal_scores = {
        'HPSA Score': 0,
        'low_birth_rate': 0,
        'avg_edu_prof_diff': 10
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

                cached_df,_ = get_dataframe()

                df = cached_df.copy() #to avoid a warning

                df['HPSA Score'] = df['HPSA Score'].fillna(0) # I think this means that it doesn't have HPSA shortage

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

                st.dataframe(sorted_ranking_df)
