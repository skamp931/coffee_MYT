import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd
import altair as alt
from countries import countries

# Streamlitのページ設定
st.set_page_config(page_title="コーヒーの世界地図", layout="wide")

# レイアウト調整
st.sidebar.title("コーヒー生産国の選択")
selected_country = st.sidebar.selectbox("コーヒー生産国を選択してください", ["選択してください"] + list(countries.keys()), index=0)

if selected_country == "選択してください":
    st.write("コーヒーの産地を選んで、その特徴を知りましょう。")
else:
    # 選択された国の特徴を取得
    country_features = countries[selected_country]['特徴']
    country_description = countries[selected_country]['説明']
    country_latlon = countries[selected_country]['緯度経度']

    # 特徴をデータフレームに変換
    df = pd.DataFrame(list(country_features.items()), columns=['特徴', '値'])

    # 世界の国境データを読み込む
    world = gpd.read_file("shp/ne_110m_admin_0_countries.shp")

    # 選択された国を強調表示
    country_name = countries[selected_country]['name']
    country_geom = world[world['NAME'] == country_name].geometry

    # 地図の中心を選択された国の緯度経度に設定
    center = [country_latlon['lat'], country_latlon['lon']]

    # Folium地図オブジェクトを作成
    m = folium.Map(location=center, zoom_start=5)

    # 選択された国の境界を描画
    # 地図の中心を選択された国の緯度経度に設定
    zoom_level = countries[selected_country]['ズームレベル']  # 各国のズームレベルを取得
    # Folium地図オブジェクトを作成
    m = folium.Map(location=center, zoom_start=zoom_level)

    # Streamlitで地図と横棒グラフを並べて表示
    col1, col2 = st.columns([2, 1])

    with col1:
        st_folium(m, width=1000, height=400)

    with col2:
        # Altairを使用して水平バーを作成
        bar_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('値:Q', scale=alt.Scale(domain=[0, 5]), axis=alt.Axis(tickMinStep=1)),
            y=alt.Y('特徴:N', sort='-x')
        ).properties(
            width=300,
            height=200
        )
        st.altair_chart(bar_chart)

    # 各国の特徴を記載
    st.write(f"### {selected_country}のコーヒーの特徴")
    st.write(
        f"酸味: {'**' + str(country_features['酸味']) + '**' if country_features['酸味'] >= 3 else country_features['酸味']}, "
        f"苦み: {'**' + str(country_features['苦み']) + '**' if country_features['苦み'] >= 3 else country_features['苦み']}, "
        f"軽さ: {'**' + str(country_features['軽さ']) + '**' if country_features['軽さ'] >= 3 else country_features['軽さ']}, "
        f"コク: {'**' + str(country_features['コク']) + '**' if country_features['コク'] >= 3 else country_features['コク']}"
    )
    st.write(f"説明: {country_description}")
