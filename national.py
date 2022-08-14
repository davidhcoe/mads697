import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from utilities import (
    get_parameter,
    get_county_details_url,
    METRIC_PARAMETER,
    INTEGER_METRICS,
    PERCENT_METRICS,
    HUMAN_READABLE_METRICS,
)


def show_national_page():
    """
    executes the code needed for the county_details page to display
    """
    url = get_county_details_url()

    def get_url(row):
        row["url"] = url + str(row["id"])
        return row

    counties_df = pd.read_csv("counties_merged.csv")
    county_display_df = counties_df[["NAME", "FIPS"]]
    county_display_df.columns = ["NAME", "id"]
    county_display_df["url"] = ""
    county_display_df = county_display_df.apply(get_url, axis=1)

    def get_map(metric):
        counties = alt.topo_feature(
            "https://cdn.jsdelivr.net/npm/vega-datasets@v1.29.0/data/us-10m.json",
            "counties",
        )
        if metric in PERCENT_METRICS:
            formatting = alt.Tooltip(f"{metric}:Q", format=".2%", title="Value")
        else:
            formatting = alt.Tooltip(f"{metric}:Q", format=",.0f", title="Value")
        c = (
            alt.Chart(counties)
            .mark_geoshape(stroke="#706545", strokeWidth=0.5)
            .encode(
                color=alt.Color(metric + ":Q", legend=alt.Legend(title="")),
                tooltip=["NAME:N", formatting],
                href="url:N",
            )
            .transform_lookup(
                lookup="id",
                from_=alt.LookupData(county_display_df, "id", ["NAME", "url"]),
            )
            .transform_lookup(
                lookup="id", from_=alt.LookupData(counties_df, "FIPS", [metric])
            )
            .project(type="albersUsa")
            .properties(width=900, height=500)
        )

        background = (
            alt.Chart(counties)
            .mark_geoshape(fill="#ededed", stroke="white")
            .project("albersUsa")
        )

        return background + c

    metric = get_parameter(METRIC_PARAMETER, "population")

    c = get_map(metric)
    st.title(HUMAN_READABLE_METRICS[metric])
    st.altair_chart(c)

    if metric in INTEGER_METRICS:
        st.metric(
            "National Average", value="{:,}".format(int(counties_df[metric].mean()))
        )
        counties_df[metric] = pd.to_numeric(counties_df[metric], errors="coerce")
        counties_df["Value"] = (
            counties_df[metric].astype(float).map(lambda n: "{0:,.0f}".format(n))
        )

    elif metric in PERCENT_METRICS:
        counties_df.dropna(subset=[metric], inplace=True)
        st.metric("National Average", value="{:.2%}".format(counties_df[metric].mean()))
        counties_df["Value"] = (
            counties_df[metric].astype(float).map(lambda n: "{:.2%}".format(n))
        )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.header("5 Highest Counties")
        st.dataframe(
            counties_df.sort_values(by=metric, ascending=False)
            .set_index("NAME")
            .head(5)["Value"]
        )

    with col2:
        st.header("5 Lowest Counties")
        st.dataframe(
            counties_df.sort_values(by=metric, ascending=True)
            .set_index("NAME")
            .head(5)["Value"]
        )
