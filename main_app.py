import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from countries import countries

# Streamlitのページ設定
st.set_page_config(page_title="コーヒーの世界地図", layout="wide")

# レイアウト調整
st.sidebar.title("コーヒー生産国の選択")
selected_country = st.sidebar.selectbox("コーヒー生産国を選択してください", list(countries.keys()), index=0)

# 選択された国の特徴を取得
country_features = countries[selected_country]['特徴']

# 特徴をデータフレームに変換
df = pd.DataFrame(list(country_features.items()), columns=['特徴', '値'])

# レーダーチャートを作成
categories = ['酸味', '苦み', '軽さ', 'コク']
values = [country_features[cat] for cat in categories]
values += values[:1]  # レーダーチャートを閉じるために最初の値を追加

angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(0.6, 0.6), subplot_kw=dict(polar=True))  # サイズを小さく設定
plt.xticks(angles[:-1], categories, color='grey', size=8)
ax.set_rlabel_position(0)
ax.plot(angles, values, linewidth=1, linestyle='solid')
ax.fill(angles, values, 'b', alpha=0.1)

# 軸の配置を調整
ax.set_theta_offset(pi / 2)  # 軽さを上に
ax.set_theta_direction(-1)  # 時計回りに
fig.set_size_inches(5.0, 5.0) 

# 世界の国境データを読み込む
world = gpd.read_file("shp/ne_110m_admin_0_countries.shp")

# 選択された国を強調表示
country_name = countries[selected_country]['name']
country_geom = world[world['NAME'] == country_name].geometry

# 地図の中心を固定
center = [0, 0]  # 世界地図の中心

# Folium地図オブジェクトを作成
m = folium.Map(location=center, zoom_start=2)

# 選択された国の境界を描画
for _, geom in country_geom.items():
    folium.GeoJson(geom, style_function=lambda x: {'fillColor': 'yellow', 'color': 'red'}).add_to(m)

# Streamlitで地図とレーダーチャートを並べて表示
col1, col2 = st.columns([1, 1])

with col1:
    st_folium(m, width=1000, height=400)

with col2:
    st.pyplot(fig)

# 各国の特徴を記載
st.write(f"### {selected_country}のコーヒーの特徴")
st.write(f"酸味: {country_features['酸味']}")
st.write(f"苦み: {country_features['苦み']}")
st.write(f"軽さ: {country_features['軽さ']}")
st.write(f"コク: {country_features['コク']}")
