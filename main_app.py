import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from countries import countries
import japanize_matplotlib

# Streamlitのページ設定
st.set_page_config(page_title="コーヒーの世界地図", layout="wide")

# ユーザーが選択した国を取得
selected_country = st.selectbox("コーヒー生産国を選択してください", list(countries.keys()))

# 選択された国の特徴を取得
country_features = countries[selected_country]['特徴']

# 特徴をデータフレームに変換
df = pd.DataFrame(list(country_features.items()), columns=['特徴', '値'])

# レーダーチャートを作成
st.write(f"{selected_country}のコーヒーの特徴")
categories = list(df['特徴'])
values = df['値'].tolist()
values += values[:1]  # レーダーチャートを閉じるために最初の値を追加

angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
plt.xticks(angles[:-1], categories, color='grey', size=8)
ax.plot(angles, values, linewidth=1, linestyle='solid')
ax.fill(angles, values, 'b', alpha=0.1)
st.pyplot(fig)


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

# Streamlitで地図を表示
st_folium(m, width=1000, height=500)
