import streamlit as st

st.set_page_config(page_title="コーヒーアプリ", layout="wide")

# タイトル
st.title("☕ ようこそ、こだわりのコーヒーの世界へ ☕")

# キャッチコピー
st.write("最高のコーヒー体験をあなたに<br>"")

# アプリの紹介
st.write("このアプリでは、世界中のコーヒー豆の情報を手軽に検索できます。")
st.write("お好みのコーヒー豆を見つけたり、新しいコーヒーの発見に役立てたりできます。")
st.write("また、コーヒーノートを使って、お気に入りのコーヒーの記録を残すこともできます。")
st.write("さらに、世界中のコーヒー生産国の情報を地図やグラフで確認することもできます。<br>") 

# 写真の追加
col1, col2, col3 = st.columns(3)
with col1:
    st.image("page_photo/coffee1.jpeg", caption="香り高いコーヒー", use_container_width=True)
with col2:
    st.image("page_photo/coffee2.jpeg", caption="こだわりの焙煎", use_container_width=True)
with col3:
    st.image("page_photo/coffee3.jpeg", caption="至福の一杯", use_container_width=True)
