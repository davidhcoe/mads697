import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from utilities import get_parameter, METRIC_PARAMETER, INTEGER_METRICS, PERCENT_METRICS

def show_national_page():
    url = ''

    debug = get_parameter('debug','false')

    if debug =='true':
            url = 'http://localhost:8501/?fips='
    else:
            #url = 'https://upwardmobility.pythonanywhere.com/county-details?fips='
            url = 'https://davidhcoe-mads697-main-1sf12v.streamlitapp.com/?fips='

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

    metric = get_parameter(METRIC_PARAMETER,'population')

    c = get_map(metric)

    st.altair_chart(c)
    
    if metric in INTEGER_METRICS:
        st.metric("National Average",value = '{:,}'.format(int(counties_df[metric].mean())))
        counties_df[metric]  = np.floor(pd.to_numeric(counties_df[metric], errors='coerce')).astype('Int64')

        col1, col2 = st.columns(2, gap='medium')
    
        with col1:
            st.header("5 Highest Counties")
            st.dataframe(counties_df[['NAME', metric]].sort_values(by=[metric], ascending=False).set_index('NAME').head(5))
        
        with col2:
            st.header("5 Lowest Counties")
            st.dataframe(counties_df[['NAME', metric]].sort_values(by=[metric], ascending=True).set_index('NAME').head(5))
        
    elif metric in PERCENT_METRICS:
        counties_df.dropna(subset=[metric], inplace=True)
        st.metric("National Average",value = '{:.2%}'.format(counties_df[metric].mean()))
        counties_df['metric_original'] = counties_df[metric] 
        counties_df[metric] = counties_df[metric].astype(float).map(lambda n: '{:.2%}'.format(n))
    
        col1, col2 = st.columns(2, gap='medium')
        
        with col1:
            st.header("5 Highest Counties")
            st.dataframe(counties_df.sort_values(by='metric_original', ascending=False).set_index('NAME').head(5)[metric])
        
        with col2:
            st.header("5 Lowest Counties")
            st.dataframe(counties_df.sort_values(by='metric_original', ascending=True).set_index('NAME').head(5)[metric])