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

# ページのタイトル
st.title("コーヒーノート")

# お店の情報
st.write("お店の情報を入力してください。")
store_name = st.text_input("店名", "")
store_address = st.text_input("住所", "")

# コーヒーの情報
st.write("コーヒーの情報を入力してください。")
roast_level = st.selectbox("焙煎度合", ["浅煎り", "中浅煎り", "中煎り", "中深煎り", "深煎り"])
grind_type = st.selectbox("豆の挽き方", ["粗挽き", "中挽き", "細挽き"])

# 味の特徴
st.write("味の特徴を入力してください。")
st.write("1: 弱い, 5: 強い")
aroma = st.slider("香り", 1, 5, 3)
acidity = st.slider("酸味", 1, 5, 3)
sweetness = st.slider("甘味", 1, 5, 3)
body = st.slider("コク", 1, 5, 3)
aftertaste = st.slider("後味", 1, 5, 3)

# 感想
st.write("コーヒーに関する感想を自由に書いてください。")
impressions = st.text_area("感想を書く", "")

# 写真のアップロード
photo = st.file_uploader("写真をアップロード", type=["jpg", "jpeg", "png"])

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
