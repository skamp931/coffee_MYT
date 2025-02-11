import streamlit as st
import pandas as pd
from datetime import datetime
import os
from coffee_notes import load_diary, save_diary

st.title("コーヒーノート")

store_name = st.text_input("店名", "")
store_address = st.text_input("住所", "")
roast_level = st.selectbox("焙煎度合", ["浅煎り", "中浅煎り", "中煎り", "中深煎り", "深煎り"])
grind_type = st.selectbox("豆の挽き方", ["粗挽き", "中挽き", "細挽き"])
st.write("1: 弱い, 5: 強い")
aroma = st.slider("香り", 1, 5, 3)
acidity = st.slider("酸味", 1, 5, 3)
sweetness = st.slider("甘味", 1, 5, 3)
body = st.slider("コク", 1, 5, 3)
aftertaste = st.slider("後味", 1, 5, 3)
impressions = st.text_area("感想を書く", "")
photo = st.file_uploader("写真をアップロード", type=["jpg", "jpeg", "png"])

if st.button("日記を保存"):
    if store_name or impressions:
        diary_df = load_diary()
        photo_filename = None
        if photo:
            photo_filename = os.path.join("photos", f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{photo.name}")
            with open(photo_filename, "wb") as f:
                f.write(photo.getbuffer())
        
        new_entry = pd.DataFrame([{
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "store_name": store_name,
            "store_address": store_address,
            "coffee_info": f"焙煎度合: {roast_level}, 豆の挽き方: {grind_type}",
            "taste_characteristics": f"香り: {aroma}, 酸味: {acidity}, 甘味: {sweetness}, コク: {body}, 後味: {aftertaste}",
            "impressions": impressions,
            "photo": photo_filename
        }])
        
        diary_df = pd.concat([diary_df, new_entry], ignore_index=True)
        save_diary(diary_df)
        st.success("日記が保存されました。")
    else:
        st.error("少なくとも1つの項目を入力してください。")

st.write("保存された日記:")
diary_df = load_diary()
st.dataframe(diary_df)
