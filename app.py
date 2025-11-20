import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="HealthMate — 食事入力", page_icon="🍽️", layout="wide")

# -----------------------
# 食材データベース（1人前当たりの栄養） — 必要なら追加・編集可
# -----------------------
FOODS = {
  "主食": {
        "白ごはん": {"kcal_per_100g": 168, "protein": 2.5, "fat": 0.3, "carbs": 37},
        "オートミール": {"kcal_per_100g": 380, "protein": 13.7, "fat": 6.2, "carbs": 69},
        "うどん": {"kcal_per_100g": 105, "protein": 2.6, "fat": 0.4, "carbs": 21},
        "そば": {"kcal_per_100g": 120, "protein": 4.8, "fat": 1.0, "carbs": 24},
        "食パン": {"kcal_per_100g": 260, "protein": 9, "fat": 4, "carbs": 45},
        # --- ここに主食を追加（あと200件でもOK） ---
    },

    "肉・魚": {
        "鶏むね肉": {"kcal_per_100g": 165, "protein": 31, "fat": 4, "carbs": 0},
        "鶏ささみ": {"kcal_per_100g": 105, "protein": 24, "fat": 0.8, "carbs": 0},
        "豚ロース": {"kcal_per_100g": 240, "protein": 19, "fat": 17, "carbs": 0},
        "牛赤身": {"kcal_per_100g": 182, "protein": 21, "fat": 10, "carbs": 0},
        "サーモン": {"kcal_per_100g": 200, "protein": 20, "fat": 13, "carbs": 0},
        "ツナ缶（水煮）": {"kcal_per_100g": 102, "protein": 23.5, "fat": 0.8, "carbs": 0},
        # --- ここに肉・魚を追加 ---
    },

    "卵・大豆製品": {
        "卵": {"kcal_per_100g": 151, "protein": 12.3, "fat": 10.3, "carbs": 0.7},
        "豆腐": {"kcal_per_100g": 56, "protein": 4.9, "fat": 3, "carbs": 1.1},
        "納豆": {"kcal_per_100g": 200, "protein": 16.5, "fat": 10, "carbs": 12},
        # --- ここに追加 ---
    },

    "野菜": {
        "ブロッコリー": {"kcal_per_100g": 33, "protein": 4.3, "fat": 0.5, "carbs": 7},
        "トマト": {"kcal_per_100g": 18, "protein": 0.7, "fat": 0.1, "carbs": 3.8},
        "レタス": {"kcal_per_100g": 15, "protein": 1.0, "fat": 0.2, "carbs": 2.8},
        # --- 野菜を追加 ---
    },

    "果物": {
        "バナナ": {"kcal_per_100g": 86, "protein": 1.1, "fat": 0.2, "carbs": 23},
        "りんご": {"kcal_per_100g": 52, "protein": 0.2, "fat": 0.1, "carbs": 14},
        "いちご": {"kcal_per_100g": 34, "protein": 0.9, "fat": 0.1, "carbs": 8},
        # --- 果物を追加 ---
    },

    "乳製品・脂質": {
        "ヨーグルト": {"kcal_per_100g": 62, "protein": 3.6, "fat": 3, "carbs": 5.2},
        "チーズ": {"kcal_per_100g": 356, "protein": 22, "fat": 29, "carbs": 2},
        "バター": {"kcal_per_100g": 700, "protein": 0.2, "fat": 81, "carbs": 0.1},
        "ナッツ": {"kcal_per_100g": 600, "protein": 20, "fat": 50, "carbs": 20},
        "アボカド": {"kcal_per_100g": 187, "protein": 2.1, "fat": 18, "carbs": 6},
        # --- 脂質系を追加 ---
    },

    "加工食品・総菜": {
        "唐揚げ": {"kcal_per_100g": 290, "protein": 17, "fat": 20, "carbs": 10},
        "ハンバーグ": {"kcal_per_100g": 230, "protein": 14, "fat": 17, "carbs": 9},
        "餃子": {"kcal_per_100g": 200, "protein": 8, "fat": 10, "carbs": 20},
        # --- 総菜を追加 ---
    },

    "スイーツ": {
        "チョコレート": {"kcal_per_100g": 558, "protein": 7.0, "fat": 34, "carbs": 55},
        "アイスクリーム": {"kcal_per_100g": 180, "protein": 3, "fat": 8, "carbs": 23},
        "クッキー": {"kcal_per_100g": 490, "protein": 6, "fat": 23, "carbs": 66},
        # --- スイーツ追加 ---
    }   
}

# -----------------------
# セッションステート初期化（今日の記録を保存）
# -----------------------
if "meals" not in st.session_state:
    st.session_state.meals = []  # リスト of dict: {time, food, qty, kcal, protein, fat, carbs}
if "settings" not in st.session_state:
    st.session_state.settings = {
        "kcal_target": 1450,
        "protein_target": 100,
        "fat_target": 35,
        "carbs_target": 160,
        "coach_tone": "優しいお姉さん",
        "hormone_phase": "なし"  # なし / 月経 / 卵胞期 / 排卵期 / 黄体期
    }

# -----------------------
# サイドバー：設定（ユーザーがカスタマイズ可能）
# -----------------------
with st.sidebar:
    st.header("設定（カスタマイズ可）")
    s = st.session_state.settings
    s["kcal_target"] = st.number_input("目標 kcal", value=int(s["kcal_target"]), step=50)
    s["protein_target"] = st.number_input("目標 Protein (g)", value=int(s["protein_target"]), step=5)
    s["fat_target"] = st.number_input("目標 Fat (g)", value=int(s["fat_target"]), step=1)
    s["carbs_target"] = st.number_input("目標 Carbs (g)", value=int(s["carbs_target"]), step=5)
    st.markdown("---")
    s["coach_tone"] = st.selectbox("コーチの口調", ["優しいお姉さん", "親友系", "淡々と科学的", "ストイックトレーナー"])
    s["hormone_phase"] = st.selectbox("月経フェーズ（任意）", ["なし", "月経", "卵胞期", "排卵期", "黄体期"])
    st.markdown("**ヒント**: ホルモンフェーズを入れると、欲求解析に反映されます。")
    st.button("設定を保存")  # 見た目用。session_stateは自動保存される

# -----------------------
# ヘッダー / 今日の概要
# -----------------------
st.title("🍽️ HealthMate — 食事入力 & 栄養解析")
st.write("食べたものを追加すると、その日の合計と不足栄養・欲求分析を表示します。")

col1, col2 = st.columns([2, 1])
with col2:
    st.subheader("今日の要約")
    today = datetime.now().date()
    st.write(f"日付: {today}")
    st.write(f"コーチ口調: **{st.session_state.settings['coach_tone']}**")
    st.write(f"ホルモンフェーズ: **{st.session_state.settings['hormone_phase']}**")

# -----------------------
# 食事入力フォーム（食材選択 + 分量）
# -----------------------
with st.form("food_entry", clear_on_submit=True):
    st.subheader("食事を追加")

    category = st.selectbox("カテゴリ", options=list(FOODS.keys()))
    food = st.selectbox("食品", options=list(FOODS[category].keys()))

    gram = st.number_input("分量（g）", min_value=1, max_value=2000, value=100, step=1)
# 100g あたり栄養に変換
nut = FOODS[food]
ratio = gram / 100  


    note = st.text_input("備考（例: 朝食 / サラダに追加等）")

    submitted = st.form_submit_button("追加")

    if submitted:
        item = FOODS[category][food]

        qty_factor = grams / 100.0
        
        entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "food": food,
            "grams": grams,
            "kcal": item["kcal_per_100g"] * qty_factor,
            "protein": item["protein"] * qty_factor,
            "fat": item["fat"] * qty_factor,
            "carbs": item["carbs"] * qty_factor,
            "note": note,
        }
        st.session_state.meals.append(entry)
        st.success(f"{food} を {grams}g 追加しました！")

# -----------------------
# 今日の食事一覧表示 & 集計
# -----------------------
st.subheader("今日の記録")
if len(st.session_state.meals) == 0:
    st.info("まだ何も追加されていません。上のフォームで食事を追加してください。")
else:
    df = pd.DataFrame(st.session_state.meals)
    df_display = df[["time", "food", "qty", "kcal", "protein", "fat", "carbs", "note"]]
    st.dataframe(df_display.style.format({"kcal":"{:.0f}", "protein":"{:.1f}", "fat":"{:.1f}", "carbs":"{:.1f}"}), height=220)

    # 合計計算
    totals = {
        "kcal": df["kcal"].sum(),
        "protein": df["protein"].sum(),
        "fat": df["fat"].sum(),
        "carbs": df["carbs"].sum()
    }

    targets = {
        "kcal": st.session_state.settings["kcal_target"],
        "protein": st.session_state.settings["protein_target"],
        "fat": st.session_state.settings["fat_target"],
        "carbs": st.session_state.settings["carbs_target"]
    }

    colA, colB, colC, colD = st.columns(4)
    colA.metric("kcal", f"{totals['kcal']:.0f} / {targets['kcal']}")
    colB.metric("Protein (g)", f"{totals['protein']:.1f} / {targets['protein']}")
    colC.metric("Fat (g)", f"{totals['fat']:.1f} / {targets['fat']}")
    colD.metric("Carbs (g)", f"{totals['carbs']:.1f} / {targets['carbs']}")

    # 不足判定
    deficit = {k: targets[k] - totals[k] for k in totals if totals[k] < targets[k]}
    excess = {k: totals[k] - targets[k] for k in totals if totals[k] > targets[k]}

    st.subheader("解析結果（ルールベース）")
    if len(deficit) == 0 and len(excess) == 0:
        st.success("おめでとう！目標にぴったりか、ほぼ達成しています。")
    else:
        if deficit:
            st.write("不足している栄養素：")
            for k, v in deficit.items():
                st.write(f"- {k}: {v:.1f} 足りません。")
        if excess:
            st.write("過剰になっている栄養素：")
            for k, v in excess.items():
                st.write(f"- {k}: {v:.1f} 過剰です。")

    # -----------------------
    # 欲求（Craving）解析ルール
    # -----------------------
    st.subheader("💭 欲求（Craving）解析")
    # 基本ルール（シンプルで解釈しやすい）
    cravings = []
    # タンパク質が大きく不足していると甘いものを欲しがる/夜の暴食の原因になりやすい
    prot_def = deficit.get("protein", 0)
    carb_def = deficit.get("carbs", 0)
    fat_def = deficit.get("fat", 0)

    hormone = st.session_state.settings["hormone_phase"]

    if prot_def >= 10:
        cravings.append(("タンパク質不足", "タンパク質が不足していると血糖変動で甘いものを欲しくなることが多いです。鶏むね肉・納豆・ツナがおすすめ。"))
    if carb_def >= 20:
        cravings.append(("炭水化物不足", "エネルギーが足りないと甘い物やパンを欲することがあります。ごはん・バナナ・オートミールを。"))
    if fat_def >= 10:
        cravings.append(("脂質不足", "油分を欲する傾向があります。ナッツ・アボカド・チーズ等を少量。"))

    # ホルモン影響の上乗せルール（簡易）
    if hormone == "黄体期":
        cravings.append(("黄体期の影響", "PMS期は甘いものやパンが欲しくなりやすいです。自分を責めず、代替案（高タンパクなスイーツ等）を試してみてください。"))
    elif hormone == "月経":
        cravings.append(("月経期の影響", "体調優先でOK。無理せず消化の良いものや温かいものを選ぶと楽になります。"))

    if len(cravings) == 0:
        st.info("現時点のデータでは特に強い『欲求シグナル』は検出されません。")
    else:
        for title, msg in cravings:
            st.markdown(f"**{title}** — {msg}")

    # -----------------------
    # 食べ過ぎたときのメンタルケアメッセージ
    # -----------------------
    st.subheader("🫶 メンタルケア（やさしいコーチング）")
    kcal_over = totals["kcal"] - targets["kcal"]
    tone = st.session_state.settings["coach_tone"]

    # ルールベースで文面変化
    def coach_message(over_kcal, tone):
        if over_kcal <= 0:
            base = "今日の摂取は目標内です。よくできました！"
        elif over_kcal <= targets["kcal"] * 0.10:
            base = "少しオーバーしましたが、挽回できる範囲です。次の食事で調整しましょう。"
        else:
            base = "今日は食べ過ぎてしまったかも。まずは深呼吸して、自分を責めないでください。"

        if tone == "優しいお姉さん":
            return base + " 大丈夫、次に活かせばOKだよ。ゆっくり休んでね。"
        if tone == "親友系":
            return base + " 気にするな！明日は一緒に軽く運動しよう🙂"
        if tone == "淡々と科学的":
            return base + " エネルギーバランスの理論的アドバイスを参照して調整を。"
        if tone == "ストイックトレーナー":
            return base + " いいね。次は少しタンパク質多めにしてリカバリーしよう。"

    st.info(coach_message(kcal_over, tone))

    # -----------------------
    # おすすめの具体的食材（不足を補う）
    # -----------------------
    st.subheader("🍳 不足を補うおすすめ（一例）")
    if "protein" in deficit:
        st.write("- 卵 / 鶏むね肉 / 豆腐 / 納豆 など（タンパク質を重点的に）")
    if "carbs" in deficit:
        st.write("- ごはん / バナナ / オートミール など（エネルギー補給）")
    if "fat" in deficit:
        st.write("- アボカド / ナッツ / チーズ など（良質な脂質）")
    if "kcal" in deficit:
        st.write("- ナッツ / ごはん / サーモン など（総カロリーを増やす）")

    # -----------------------
    # ログ出力・ダウンロード
    # -----------------------
    st.subheader("データ操作")
    if len(st.session_state.meals) > 0:
        df_save = pd.DataFrame(st.session_state.meals)
        csv = df_save.to_csv(index=False).encode("utf-8")
        st.download_button("今日のログをCSVでダウンロード", csv, file_name=f"meals_{today}.csv", mime="text/csv")
        if st.button("今日のログをクリアする"):
            st.session_state.meals = []
            st.experimental_rerun()

st.caption("※このアプリは医療行為の代替ではありません。体調不良が続く場合は専門医に相談してください。")
