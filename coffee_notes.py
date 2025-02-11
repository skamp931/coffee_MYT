import streamlit as st
import pandas as pd
from datetime import datetime

# 日記データを保存するファイル名
DIARY_FILE = "coffee_diary.csv"

# 日記データを読み込む関数
def load_diary():
    try:
        return pd.read_csv(DIARY_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["date", "store_info", "coffee_info", "taste_characteristics", "impressions"])

# 日記データを保存する関数
def save_diary(diary_df):
    diary_df.to_csv(DIARY_FILE, index=False)

# ページのタイトル
st.title("コーヒーノート")

# お店の情報
st.write("お店の情報を入力してください。")
store_info = st.text_input("店名、住所など", "")

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
