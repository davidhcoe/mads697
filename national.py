import streamlit as st
import pandas as pd
import altair as alt
from utilities import get_parameter, METRIC_PARAMETER

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