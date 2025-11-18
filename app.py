import streamlit as st

st.set_page_config(page_title="カロリーコーチ", page_icon="🍙", layout="centered")

# -------------------------
# 食材データ（あなたが自由に追加できる）
# -------------------------

FOODS = [
    {"name": "さつまいも", "caloriesPerGram": 1.3},
    {"name": "白ごはん", "caloriesPerGram": 1.68},
    {"name": "鶏胸肉", "caloriesPerGram": 1.65},
    {"name": "卵", "caloriesPerGram": 1.55},
    {"name": "アボカド", "caloriesPerGram": 1.6},
    {"name": "トマト", "caloriesPerGram": 0.18},
    {"name": "レタス", "caloriesPerGram": 0.15},

    # ↓↓↓ここにどんどん食材を追加してOK！↓↓↓
    # {"name": "オートミール", "caloriesPerGram": 3.8},
    # {"name": "納豆", "caloriesPerGram": 2.0},
    # みたいに好きなだけ！
]

# -------------------------
# セッション状態の準備
# -------------------------
if "logs" not in st.session_state:
    st.session_state.logs = []   # 今日の食事記録List


# -------------------------
# UI
# -------------------------
st.title("🍙 カロリーコーチ")
st.write("食材を選んでグラム数を入力すると、自動でカロリー計算します！")
st.write("食材は自由に追加できます。")


# -------------------------
# 食材選択
# -------------------------
selected_food = st.selectbox("食べた食材を選んでください", [f["name"] for f in FOODS])

grams = st.number_input("グラム数を入力（g）", min_value=0, step=10)

# -------------------------
# 追加ボタン
# -------------------------
if st.button("追加する"):
    if grams > 0:
        # 食材データを検索
        food_obj = next((f for f in FOODS if f["name"] == selected_food), None)
        if food_obj:
            cal = food_obj["caloriesPerGram"] * grams
            st.session_state.logs.append({
                "name": selected_food,
                "grams": grams,
                "cal": cal
            })
            st.success(f"{selected_food} を {grams}g 追加しました！（{round(cal,1)} kcal）")
    else:
        st.warning("グラム数を入力してください！")


# -------------------------
# 今日のログ
# -------------------------
st.subheader("📘 今日の食事記録")

if len(st.session_state.logs) == 0:
    st.write("まだ記録がありません。")
else:
    total = 0
    for item in st.session_state.logs:
        st.write(f"- {item['name']}：{item['grams']}g（{round(item['cal'])} kcal）")
        total += item["cal"]

    st.write("### 🧮 合計カロリー：", round(total), "kcal")


    # -------------------------
    # コーチのアドバイス（AI風）
    # -------------------------
    st.subheader("💡 コーチのアドバイス")

    if total < 300:
        st.write("✔ まだ軽め！たんぱく質を追加してもOK！")
    elif total < 600:
        st.write("✔ いい感じのバランスです！次は野菜を増やすとさらに◎")
    else:
        st.write("✔ 少しカロリー高め。次は低カロリー食材中心が良いかも！")


# -------------------------
# RESET
# -------------------------
if st.button("今日の記録をリセット"):
    st.session_state.logs = []
    st.info("記録をリセットしました！")


