import streamlit as st
import plotly.express as px
import pandas as pd
import json

county_json = open(f"geojson-counties-fips.json")
counties = json.load(county_json)

def handleclick(trace, points, selector):
    print(trace)
    st.write(trace)
    st.write(points)
    st.write(selector)

# df = pd.read_csv('counties_merged.csv')


# fig = px.choropleth(df, geojson=counties, locations='FIPS', color='median_family_income',
#                            color_continuous_scale="Viridis",
#                            range_color=(0, 12),
#                            scope="usa",
#                            labels={'median_family_income':'Median Family Income'}
#                           )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

metric = 'median_family_income'

df = pd.read_csv(f"counties_merged.csv",
                dtype={"fips": str})[['FIPS', metric, 'NAME']]

df['FIPS'] = df['FIPS'].astype(int).astype(str).str.zfill(5)

df['LINK'] = "[Link](https://upwardmobility.pythonanywhere.com/compare-counties?fips=" + df['FIPS'] + ")"
if metric:
    low = min(df[metric].values)
    high = max(df[metric].values)
else:
    low = 0
    high = 1
fig2 = px.choropleth(df, geojson=counties, locations='FIPS', color=metric,
                        color_continuous_scale="Viridis",
                        range_color=(low, high),
                        scope="usa",
                        labels={metric:metric},hover_data=["NAME", metric])

mapinfo = fig2.data[0]

mapinfo.on_click(handleclick)

st.plotly_chart(fig2)