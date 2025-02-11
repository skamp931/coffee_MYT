import streamlit as st
import pandas as pd
from datetime import datetime
import os
from coffee_notes import load_diary, save_diary
from countries import countries

st.title("コーヒーノート")

# ユーザー名を入力
user_name = st.text_input("ユーザー名", "")

# 年月日を入力
date = st.date_input("日付", datetime.now())

# 店名と住所を入力
store_name = st.text_input("店名", "")
store_address = st.text_input("住所", "")

# コーヒー豆の生産国を選択
country = st.selectbox("コーヒー豆の生産国", ["選択してください"] + list(countries.keys()))

# コーヒーの情報を入力
roast_level = st.selectbox("焙煎度合", ["浅煎り", "中浅煎り", "中煎り", "中深煎り", "深煎り"])
grind_type = st.selectbox("豆の挽き方", ["粗挽き", "中挽き", "細挽き"])
st.write("1: 弱い, 5: 強い")
aroma = st.slider("香り", 1, 5, 3)
acidity = st.slider("酸味", 1, 5, 3)
sweetness = st.slider("甘味", 1, 5, 3)
body = st.slider("コク", 1, 5, 3)
aftertaste = st.slider("後味", 1, 5, 3)

# 感想と写真を入力
impressions = st.text_area("感想を書く", "")
photo = st.file_uploader("写真をアップロード", type=["jpg", "jpeg", "png"])

# 日記を保存するボタン
if st.button("日記を保存"):
    if user_name and (store_name or impressions):
        diary_df = load_diary()
        photo_filename = None
        if photo:
            photo_filename = os.path.join("photos", f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{photo.name}")
            with open(photo_filename, "wb") as f:
                f.write(photo.getbuffer())
        
        new_entry = pd.DataFrame([{
            "user_name": user_name,
            "date": date.strftime("%Y-%m-%d"),
            "store_name": store_name,
            "store_address": store_address,
            "country": country if country != "選択してください" else "",
            "coffee_info": f"焙煎度合: {roast_level}, 豆の挽き方: {grind_type}",
            "taste_characteristics": f"香り: {aroma}, 酸味: {acidity}, 甘味: {sweetness}, コク: {body}, 後味: {aftertaste}",
            "impressions": impressions,
            "photo": photo_filename
        }])
        
        diary_df = pd.concat([diary_df, new_entry], ignore_index=True)
        save_diary(diary_df)
        st.success("日記が保存されました。")
    else:
        st.error("ユーザー名と少なくとも1つの項目を入力してください。")

# 保存された日記を表示
st.write("保存された日記:")
diary_df = load_diary()

# ユーザー名でフィルタリング
filter_user_name = st.text_input("表示するユーザー名を入力", "")
if filter_user_name:
    filtered_diary_df = diary_df[diary_df['user_name'] == filter_user_name]
    st.dataframe(filtered_diary_df)
else:
    st.dataframe(diary_df)
