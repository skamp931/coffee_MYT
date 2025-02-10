import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd  # ここでgeopandasをインポート
import geodatasets

# Streamlitのページ設定
st.set_page_config(page_title="コーヒーの世界地図", layout="wide")

world = gpd.read_file(geodatasets.get_path('naturalearth.land'))

# 列名を表示
st.write(world.columns)

# 地図の中心座標を設定
center = [0, 0]  # 世界地図の中心

# コーヒー生産国のリスト
countries = {
    "ブラジル": "Brazil",
    "コロンビア": "Colombia",
    "グラテマラ": "Guatemala",
    "ケニア": "Kenya",
    "パナマ": "Panama",
    "タンザニア": "Tanzania",
    "エチオピア": "Ethiopia",
    "エルサルバドル": "El Salvador"
}

# ユーザーが選択した国を取得
selected_country = st.selectbox("コーヒー生産国を選択してください", list(countries.keys()))

# Folium地図オブジェクトを作成
m = folium.Map(location=center, zoom_start=2)

# 世界の国境データを読み込む
world = gpd.read_file(geodatasets.get_path('naturalearth.land'))

# 選択された国を強調表示
country_name = countries[selected_country]
country_geom = world[world['name'] == country_name].geometry

# 選択された国の境界を描画
for _, geom in country_geom.iteritems():
    folium.GeoJson(geom, style_function=lambda x: {'fillColor': 'yellow', 'color': 'red'}).add_to(m)

# Streamlitで地図を表示
st_folium(m, width=700, height=500)
