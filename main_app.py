import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from countries import countries

# Streamlitのページ設定
st.set_page_config(page_title="コーヒーの世界地図", layout="wide")

# ユーザーが選択した国を取得
selected_country = st.selectbox("コーヒー生産国を選択してください", list(countries.keys()))

# 選択された国の特徴を取得
country_features = countries[selected_country]['特徴']

# 特徴をデータフレームに変換
df = pd.DataFrame(list(country_features.items()), columns=['特徴', '値'])

# 特徴をチャートで表示
st.write(f"{selected_country}のコーヒーの特徴")
fig, ax = plt.subplots()
df.plot(kind='bar', x='特徴', y='値', ax=ax, legend=False)
st.pyplot(fig)

# 世界の国境データを読み込む
world = gpd.read_file("shp/ne_110m_admin_0_countries.shp")

# 選択された国を強調表示
country_name = countries[selected_country]['name']
country_geom = world[world['NAME'] == country_name].geometry

# 選択された国の中心座標を計算
country_center = country_geom.centroid.iloc[0].coords[0]

# Folium地図オブジェクトを作成
m = folium.Map(location=country_center, zoom_start=5)

# 選択された国の境界を描画
for _, geom in country_geom.items():
    folium.GeoJson(geom, style_function=lambda x: {'fillColor': 'yellow', 'color': 'red'}).add_to(m)

# Streamlitで地図を表示
st_folium(m, width=700, height=500)
