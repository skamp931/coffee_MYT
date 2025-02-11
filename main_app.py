import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd
import altair as alt
from countries import countries
from datetime import datetime
from coffee_notes import load_diary

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
    zoom_level = countries[selected_country]['ズームレベル']  # 各国のズームレベルを取得

    # 各国の特徴を記載
    st.write(f"### {selected_country}のコーヒーの特徴")

    # Folium地図オブジェクトを作成
    m = folium.Map(location=center, zoom_start=zoom_level)

    # 選択された国の境界を描画
    for _, geom in country_geom.items():
        folium.GeoJson(geom, style_function=lambda x: {'fillColor': 'yellow', 'color': 'red'}).add_to(m)

    # Streamlitで地図と横棒グラフを並べて表示
    col1, col2 = st.columns([2, 1])

    with col1:
        st_folium(m, width=1000, height=400)

    with col2:
        # Altairを使用して水平バーを作成
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
        # 各国の特徴を記載
        st.write(
            f"酸味: {'**' + str(country_features['酸味']) + '**' if country_features['酸味'] >= 3 else country_features['酸味']}, "
            f"苦み: {'**' + str(country_features['苦み']) + '**' if country_features['苦み'] >= 3 else country_features['苦み']}, "
            f"軽さ: {'**' + str(country_features['軽さ']) + '**' if country_features['軽さ'] >= 3 else country_features['軽さ']}, "
            f"コク: {'**' + str(country_features['コク']) + '**' if country_features['コク'] >= 3 else country_features['コク']}"
        )

    st.write(f"・{country_description}")

    # コーヒーノートの入力
    st.write("### コーヒーノートを追加")
    store_info = st.text_input("店名、住所など", "")
    roast_level = st.selectbox("焙煎度合", ["浅煎り", "中浅煎り", "中煎り", "中深煎り", "深煎り"])
    grind_type = st.selectbox("豆の挽き方", ["粗挽き", "中挽き", "細挽き"])
    st.write("1: 弱い, 5: 強い")
    aroma = st.slider("香り", 1, 5, 3)
    acidity = st.slider("酸味", 1, 5, 3)
    sweetness = st.slider("甘味", 1, 5, 3)
    body = st.slider("コク", 1, 5, 3)
    aftertaste = st.slider("後味", 1, 5, 3)
    impressions = st.text_area("感想を書く", "")

    # 日記を保存するボタン
    if st.button("日記を保存"):
        if store_info or impressions:
            diary_df = load_diary()
            new_entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "store_info": store_info,
                "coffee_info": f"焙煎度合: {roast_level}, 豆の挽き方: {grind_type}",
                "taste_characteristics": f"香り: {aroma}, 酸味: {acidity}, 甘味: {sweetness}, コク: {body}, 後味: {aftertaste}",
                "impressions": impressions
            }
            diary_df = diary_df.append(new_entry, ignore_index=True)
            save_diary(diary_df)
            st.success("日記が保存されました。")
        else:
            st.error("少なくとも1つの項目を入力してください。")

    # 保存された日記を表示
    st.write("保存された日記:")
    diary_df = load_diary()
    st.dataframe(diary_df)
