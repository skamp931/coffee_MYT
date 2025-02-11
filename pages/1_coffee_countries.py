import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd
from countries import countries

st.title("コーヒー生産国")

selected_country = st.sidebar.selectbox("コーヒー生産国を選択してください", ["選択してください"] + list(countries.keys()), index=0)

if selected_country == "選択してください":
    st.write("コーヒーの産地を選んで、その特徴を知りましょう。")
else:
    country_features = countries[selected_country]['特徴']
    country_description = countries[selected_country]['説明']
    country_latlon = countries[selected_country]['緯度経度']

    df = pd.DataFrame(list(country_features.items()), columns=['特徴', '値'])

    world = gpd.read_file("shp/ne_110m_admin_0_countries.shp")
    country_name = countries[selected_country]['name']
    country_geom = world[world['NAME'] == country_name].geometry

    center = [country_latlon['lat'], country_latlon['lon']]
    zoom_level = countries[selected_country]['ズームレベル']

    st.write(f"### {selected_country}のコーヒーの特徴")

    m = folium.Map(location=center, zoom_start=zoom_level)
    for _, geom in country_geom.items():
        folium.GeoJson(geom, style_function=lambda x: {'fillColor': 'yellow', 'color': 'red'}).add_to(m)

    col1, col2 = st.columns([2, 1])

    with col1:
        st_folium(m, width=1000, height=400)

    with col2:
        bar_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('値:Q', scale=alt.Scale(domain=[0, 5]), axis=alt.Axis(tickMinStep=1), title=None),
            y=alt.Y('特徴:N', sort='-x', title=None)
        ).properties(
            width=300,
            height=200,
            title=alt.TitleParams(
                text='特徴',
                align='center'
            )
        )
        st.altair_chart(bar_chart)
        st.write(
            f"酸味: {'**' + str(country_features['酸味']) + '**' if country_features['酸味'] >= 3 else country_features['酸味']}, "
            f"苦み: {'**' + str(country_features['苦み']) + '**' if country_features['苦み'] >= 3 else country_features['苦み']}, "
            f"軽さ: {'**' + str(country_features['軽さ']) + '**' if country_features['軽さ'] >= 3 else country_features['軽さ']}, "
            f"コク: {'**' + str(country_features['コク']) + '**' if country_features['コク'] >= 3 else country_features['コク']}"
        )

    st.write(f"・{country_description}")
