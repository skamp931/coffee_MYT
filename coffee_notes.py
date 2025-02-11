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
