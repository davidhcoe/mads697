import streamlit as st
import pandas as pd 
import altair as alt

url_params = st.experimental_get_query_params()

fips_parameter = 'fips'

fips_code = ''

if fips_parameter in url_params:
    fips_code = url_params[fips_parameter][0]
    
    if len(fips_code) > 0:
        df = pd.read_csv('counties_merged.csv')

        county_only_df = df[df['FIPS']==int(fips_code)]

        if len(county_only_df) == 1:
            st.title(f"Get data for {county_only_df.NAME.values[0]}")

            st.write(county_only_df)

            st.write('Race')

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

                st.metric("Median Family Income",
                        value = '${0:,.0f}'.format(county_only_df["median_family_income"].values[0]))

                st.metric("Income 20%",
                        value = '${0:,.0f}'.format(county_only_df["income_20_percentile"].values[0]))

                st.metric("Income 80%",
                        value = '${0:,.0f}'.format(county_only_df["income_80_percentile"].values[0]))
            with col2:
                st.write(f'''
                    #### Education    
                ''')

                st.metric("Preschool enrollment",
                        value = '{:.0%}'.format(county_only_df["preschool_enroll"].values[0]))

                st.metric("Avg Edu Prof Diff",
                        value = county_only_df["avg_edu_prof_diff"].values[0])

            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f'''
                    #### Neighborhoods    
                ''')

                st.metric("Proportion High Poverty",
                        value = '{:.0%}'.format(county_only_df["proportion_high_poverty_neighborhood"].values[0]))

                st.metric("Transit Trips",
                        value = county_only_df["transit_trips_index"].values[0])

                st.metric("Low Cost Transit",
                        value = county_only_df["transit_low_cost_index"].values[0])

            with col2:
                st.write(f'''
                    #### Housing    
                ''')

                st.metric("Homeless Students",
                        value = county_only_df["HOM_STUDENTS"].values[0])

                st.metric("Proportion homeless",
                        value = '{:.0%}'.format(county_only_df["proportion_homeless"].values[0]))
            
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

                # st.metric("HPSA Score",
                #         value = county_only_df["HPSA Score"].values[0])
        else:
            st.title(f"Cant find any data for {fips_code}")



else:
    st.title("Hello, World")
