import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

def get_url(row):

  row['url'] = 'https://www.google.com/search?q=fips ' + str(row['id'])

  return row

counties_df = pd.read_csv('counties_merged.csv')
county_display_df = counties_df[['NAME','FIPS']]
county_display_df.columns = ['NAME','id']
county_display_df['url'] = ''
county_display_df = county_display_df.apply(get_url, axis=1)

counties = alt.topo_feature(data.us_10m.url, 'counties')
source = data.unemployment.url

c = alt.Chart(counties).mark_geoshape().encode(
    color='rate:Q',
    tooltip=['NAME:N', 'url:N'],
    href='url:N'
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(county_display_df, 'id', ['NAME', 'url'])
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(source, 'id', ['rate'])
).project(
    type='albersUsa'
).properties(
    width=500,
    height=300
)

st.altair_chart(c)