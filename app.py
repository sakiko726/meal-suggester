import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="HealthMate EX", page_icon="💪", layout="wide")

# ===============================
# 1) 食材データ（圧縮60品）
# ===============================
FOODS = {
    "主食": {
        "白ごはん": {"kcal": 168, "P": 2.5, "F": 0.3, "C": 37},
        "オートミール": {"kcal": 380, "P": 13.7, "F": 6.2, "C": 69},
        "食パン": {"kcal": 260, "P": 9, "F": 4, "C": 45},
        "うどん": {"kcal": 105, "P": 2.6, "F": 0.4, "C": 21},
        "そば": {"kcal": 120, "P": 4.8, "F": 1, "C": 24},
    },
    "肉・魚": {
        "鶏むね肉": {"kcal": 165, "P": 31, "F": 4, "C": 0},
        "鶏ささみ": {"kcal": 105, "P": 24, "F": 0.8, "C": 0},
        "牛赤身": {"kcal": 182, "P": 21, "F": 10, "C": 0},
        "豚ロース": {"kcal": 240, "P": 19, "F": 17, "C": 0},
        "サーモン": {"kcal": 200, "P": 20, "F": 13, "C": 0},
        "ツナ缶（水煮）": {"kcal": 102, "P": 23.5, "F": 0.8, "C": 0},
    },
    "卵・大豆": {
        "卵": {"kcal": 151, "P": 12.3, "F": 10.3, "C": 0.7},
        "豆腐": {"kcal": 56, "P": 4.9, "F": 3, "C": 1.1},
        "納豆": {"kcal": 200, "P": 16.5, "F": 10, "C": 12},
        "厚揚げ": {"kcal": 150, "P": 10, "F": 10, "C": 3},
    },
    "野菜": {
        "ブロッコリー": {"kcal": 33, "P": 4.3, "F": 0.5, "C": 7},
        "トマト": {"kcal": 18, "P": 0.7, "F": 0.1, "C": 3.8},
        "レタス": {"kcal": 15, "P": 1.0, "F": 0.2, "C": 2.8},
        "にんじん": {"kcal": 37, "P": 0.8, "F": 0.2, "C": 9},
        "ほうれん草": {"kcal": 20, "P": 2.1, "F": 0.4, "C": 3.1},
    },
    "果物": {
        "バナナ": {"kcal": 86, "P": 1.1, "F": 0.2, "C": 23},
        "りんご": {"kcal": 52, "P": 0.2, "F": 0.1, "C": 14},
        "いちご": {"kcal": 34, "P": 0.9, "F": 0.1, "C": 8},
        "みかん": {"kcal": 45, "P": 0.6, "F": 0.2, "C": 12},
    },
    "脂質・乳製品": {
        "ヨーグルト": {"kcal": 62, "P": 3.6, "F": 3, "C": 5.2},
        "チーズ": {"kcal": 356, "P": 22, "F": 29, "C": 2},
        "ナッツ": {"kcal": 600, "P": 20, "F": 50, "C": 20},
        "アボカド": {"kcal": 187, "P": 2.1, "F": 18, "C": 6},
    },
    "スイーツ": {
        "チョコレート": {"kcal": 558, "P": 7, "F": 34, "C": 55},
        "アイス": {"kcal": 180, "P": 3, "F": 8, "C": 23},
        "クッキー": {"kcal": 490, "P": 6, "F": 23, "C": 66},
        "ケーキ": {"kcal": 430, "P": 5, "F": 24, "C": 50},
    }
}

# ========================================
# 2) セッション初期化
# ========================================
if "meals" not in st.session_state:
    st.session_state.meals = []

if "settings" not in st.session_state:
    st.session_state.settings = {
        "kcal_target": 1450,
        "protein_target": 100,
        "fat_target": 35,
        "carbs_target": 160,
        "coach_tone": "優しいお姉さん",
        "hormone_phase": "なし"
    }

# ========================================
# 3) サイドバー設定
# ========================================
with st.sidebar:
    st.header("⚙️ 設定")
    s = st.session_state.settings

    s["kcal_target"] = st.number_input("目標 kcal", value=s["kcal_target"])
    s["protein_target"] = st.number_input("目標 P", value=s["protein_target"])
    s["fat_target"] = st.number_input("目標 F", value=s["fat_target"])
    s["carbs_target"] = st.number_input("目標 C", value=s["carbs_target"])

    s["coach_tone"] = st.selectbox("コーチの口調", ["優しいお姉さん", "体育会系", "冷静な医者"])
    s["hormone_phase"] = st.selectbox("ホルモン状態", ["なし", "月経", "卵胞期", "排卵期", "黄体期"])

# ========================================
# 4) メインページ
# ========================================
st.title("🍽️ HealthMate EX – 食事記録 & AIコーチ")

# ---- 食事入力 UI ----
category = st.selectbox("カテゴリー", list(FOODS.keys()))
food = st.selectbox("食材", list(FOODS[category].keys()))
grams = st.number_input("グラム数（g）", min_value=1, value=100)

data = FOODS[category][food]
k = data["kcal"] * grams / 100
p = data["P"] * grams / 100
f = data["F"] * grams / 100
c = data["C"] * grams / 100

if st.button("追加する"):
    st.session_state.meals.append({
        "time": datetime.now().strftime("%H:%M"),
        "food": food,
        "grams": grams,
        "kcal": k,
        "P": p,
        "F": f,
        "C": c
    })
    st.success("追加しました！")

# ---- 今日の記録 ----
st.subheader("📘 今日の記録")
if len(st.session_state.meals) > 0:
    df = pd.DataFrame(st.session_state.meals)
    st.dataframe(df)

    total = df[["kcal", "P", "F", "C"]].sum()

    st.write("### 今日の合計")
    st.write(f"🔥 kcal: {total.kcal:.0f} / {s['kcal_target']}")
    st.write(f"💪 Protein: {total.P:.1f} / {s['protein_target']}")
    st.write(f"🥑 Fat: {total.F:.1f} / {s['fat_target']}")
    st.write(f"🍞 Carbs: {total.C:.1f} / {s['carbs_target']}")

# ========================================
# 5) AIコーチのアドバイス
# ========================================
if st.button("AIコーチに相談する"):
    tone = s["coach_tone"]
    phase = s["hormone_phase"]

    advice = "今日の食事はとても良い感じ！"

    # 栄養の偏りによる craving
    if total.P < s["protein_target"] * 0.6:
        advice += "\n- タンパク質が不足しているから甘いもの欲しくなる可能性高いよ！"

    if phase == "黄体期":
        advice += "\n- 黄体期だから食欲強くなるのは自然。むくみやすいから塩分控えめに。"

    if phase == "月経":
        advice += "\n- 月経中は鉄分が落ちやすいから、赤身肉やほうれん草もおすすめ。"

    st.info(f"**{tone}モードのコーチより:**\n\n{advice}")
