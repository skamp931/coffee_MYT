import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import os

# 日記データを保存するファイル名
DIARY_FILE = "coffee_diary.csv"
PHOTO_DIR = "photos"

# 写真ディレクトリが存在しない場合は作成
if not os.path.exists(PHOTO_DIR):
    os.makedirs(PHOTO_DIR)

# 日記データを読み込む関数
def load_diary():
    try:
        return pd.read_csv(DIARY_FILE)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=["date", "store_name", "store_address", "coffee_info", "taste_characteristics", "impressions", "photo"])

# 日記データを保存する関数
def save_diary(diary_df):
    diary_df.to_csv(DIARY_FILE, index=False)

# 日記を保存するボタン
if st.button("日記を保存"):
    if store_name or impressions:
        diary_df = load_diary()
        photo_filename = None
        if photo:
            photo_filename = os.path.join(PHOTO_DIR, f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{photo.name}")
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

# 保存された日記を表示
st.write("保存された日記:")
diary_df = load_diary()
st.dataframe(diary_df)
