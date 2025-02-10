import streamlit as st
import folium
from streamlit_folium import st_folium

# Streamlitのページ設定
st.set_page_config(page_title="地図表示", layout="wide")

# 地図の中心座標を設定
center = [35.6895, 139.6917]  # 東京の緯度経度

# Folium地図オブジェクトを作成
m = folium.Map(location=center, zoom_start=10)

# Streamlitで地図を表示
st_folium(m, width=700, height=500)
