import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.title("AIコーチ付き 食事 & 体調サポートアプリ 💛")

# =========================================================
# 初期化
# =========================================================
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

s = st.session_state.settings

# =========================================================
# 🩸 生理周期チェック
# =========================================================
st.header("🩸 生理周期チェック")

period_start = st.date_input("直近の生理開始日を入力してね")
cycle_length = st.number_input("平均生理周期（日）", min_value=20, max_value=40, value=28)
period_length = st.number_input("生理期間の日数", min_value=3, max_value=10, value=5)

today = datetime.now().date()

phase = "不明"
coach_msg = ""

if period_start:
    days_passed = (today - period_start).days % cycle_length

    if days_passed < period_length:
        phase = "月経期（Menstruation）"
        coach_msg = "今日はゆっくり休んでね…生きてるだけで偉いよ💛"

    elif days_passed < 14:
        phase = "卵胞期（Follicular）"
        coach_msg = "代謝が上がりやすい時期！ここから一緒にペース上げよ💛"

    elif days_passed == 14:
        phase = "排卵期（Ovulation）"
        coach_msg = "魅力MAXの時期✨ 気分も肌も調子よくなりがち！"

    else:
        phase = "黄体期（Luteal）"
        coach_msg = "むくみ・食欲UPしがち！甘い物ほしくなるのはホルモンのせい🍫"

    st.subheader(f"📌 現在のあなたのフェーズ： **{phase}**")
    st.write(coach_msg)


# =========================================================
# 🍚 食材データ
# =========================================================
{
  "主食": {
    "白ごはん": {"kcal_per_100g":168, "protein":2.5, "fat":0.3, "carbs":37},
    "オートミール": {"kcal_per_100g":380, "protein":13.7, "fat":6.2, "carbs":69},
    "食パン": {"kcal_per_100g":260, "protein":9.0, "fat":4.0, "carbs":45},
    "うどん": {"kcal_per_100g":105, "protein":2.6, "fat":0.4, "carbs":21},
    "そば": {"kcal_per_100g":120, "protein":4.8, "fat":1.0, "carbs":24}
  },
  "肉・魚": {
    "鶏むね肉": {"kcal_per_100g":165, "protein":31, "fat":4, "carbs":0},
    "鶏ささみ": {"kcal_per_100g":105, "protein":24, "fat":0.8, "carbs":0},
    "牛赤身": {"kcal_per_100g":182, "protein":21, "fat":10, "carbs":0},
    "豚ロース": {"kcal_per_100g":240, "protein":19, "fat":17, "carbs":0},
    "サーモン": {"kcal_per_100g":200, "protein":20, "fat":13, "carbs":0},
    "ツナ缶（水煮）": {"kcal_per_100g":102, "protein":23.5, "fat":0.8, "carbs":0}
  },
  "卵・大豆": {
    "卵": {"kcal_per_100g":151, "protein":12.3, "fat":10.3, "carbs":0.7},
    "豆腐": {"kcal_per_100g":56, "protein":4.9, "fat":3, "carbs":1.1},
    "納豆": {"kcal_per_100g":200, "protein":16.5, "fat":10, "carbs":12},
    "厚揚げ": {"kcal_per_100g":150, "protein":10, "fat":10, "carbs":3}
  },
  "野菜": {
    "ブロッコリー": {"kcal_per_100g":33, "protein":4.3, "fat":0.5, "carbs":7},
    "トマト": {"kcal_per_100g":18, "protein":0.7, "fat":0.1, "carbs":3.8},
    "レタス": {"kcal_per_100g":15, "protein":1.0, "fat":0.2, "carbs":2.8},
    "にんじん": {"kcal_per_100g":37, "protein":0.8, "fat":0.2, "carbs":9},
    "ほうれん草": {"kcal_per_100g":20, "protein":2.1, "fat":0.4, "carbs":3.1}
  },
  "果物": {
    "バナナ": {"kcal_per_100g":86, "protein":1.1, "fat":0.2, "carbs":23},
    "りんご": {"kcal_per_100g":52, "protein":0.2, "fat":0.1, "carbs":14},
    "いちご": {"kcal_per_100g":34, "protein":0.9, "fat":0.1, "carbs":8},
    "みかん": {"kcal_per_100g":45, "protein":0.6, "fat":0.2, "carbs":12}
  },
  "脂質・乳製品": {
    "ヨーグルト": {"kcal_per_100g":62, "protein":3.6, "fat":3, "carbs":5.2},
    "チーズ": {"kcal_per_100g":356, "protein":22, "fat":29, "carbs":2},
    "ナッツ": {"kcal_per_100g":600, "protein":20, "fat":50, "carbs":20},
    "アボカド": {"kcal_per_100g":187, "protein":2.1, "fat":18, "carbs":6}
  },
  "スイーツ": {
    "チョコレート": {"kcal_per_100g":558, "protein":7, "fat":34, "carbs":55},
    "アイス": {"kcal_per_100g":180, "protein":3, "fat":8, "carbs":23},
    "クッキー": {"kcal_per_100g":490, "protein":6, "fat":23, "carbs":66},
    "ケーキ": {"kcal_per_100g":430, "protein":5, "fat":24, "carbs":50}
  }
}

# =========================================================
# 🍽 食事入力
# =========================================================
st.header("🍽 食事入力（グラムでOK！）")

selected_food = st.selectbox("食べたものを選ぶ", food_names)
grams = st.number_input("食べた量（g）", min_value=1, max_value=2000, value=100)

if st.button("カロリー計算"):
    total = FOODS[selected_food] * (grams / 100)
    st.subheader(f"👉 **{selected_food}：{total:.1f} kcal**")

if st.button("追加する 🍽️"):
    kcal = FOODS[selected_food] * (grams / 100)

    st.session_state.meals.append({
        "time": datetime.now().strftime("%H:%M"),
        "food": selected_food,
        "grams": grams,
        "kcal": kcal,
    })
    st.success("追加しました！✨")


# =========================================================
# 📘 今日の記録
# =========================================================
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

    # =====================================================
    # コーチコメント
    # =====================================================
    st.write("---")
    st.subheader("🤖 今日のコーチコメント")

    tone = s["coach_tone"]

    if tone == "優しいお姉さん":
        st.write("💛 頑張ってるね…偉すぎるよ〜〜！！")
    elif tone == "厳しめトレーニー":
        st.write("💪 よし！タンパク質まだいける！！攻めろ！！")
    else:
        st.write("👓 データ良好。次はPFC比率も管理しましょう。")


# =========================================================
# ⚙️ サイドバー設定
# =========================================================
with st.sidebar:
    st.header("⚙️ 設定（目標値を変えられるよ）")

    s["kcal_target"] = st.number_input("目標 kcal", value=s["kcal_target"])
    s["protein_target"] = st.number_input("目標 P", value=s["protein_target"])
    s["fat_target"] = st.number_input("目標 F", value=s["fat_target"])
    s["carbs_target"] = st.number_input("目標 C", value=s["carbs_target"])

    st.markdown("### 🩺 生理周期")
    s["hormone_phase"] = st.selectbox("ホルモン状態", ["なし", "月経", "卵胞期", "排卵期", "黄体期"])

    st.markdown("### 🎤 コーチのタイプ")
    s["coach_tone"] = st.selectbox("コーチの口調", ["優しいお姉さん", "厳しめトレーニー", "医者"])
