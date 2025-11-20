# 簡易栄養データ
FOODS = {
    "卵": {"protein": 6, "iron": 0.9, "vitc": 0},
    "サツマイモ": {"protein": 1, "iron": 0.3, "vitc": 23},
    "トマト": {"protein": 1, "iron": 0.1, "vitc": 15},
    "鶏肉": {"protein": 25, "iron": 1.3, "vitc": 0},
    "豆腐": {"protein": 7, "iron": 1, "vitc": 0},
}

# 推奨最低ライン
TARGET = {
    "protein": 20,
    "iron": 2,
    "vitc": 30,
}

def analyze_meal(items):
    total = {"protein": 0, "iron": 0, "vitc": 0}

    for item in items:
        if item in FOODS:
            data = FOODS[item]
            for key in total:
                total[key] += data[key]

    deficit = []
    for key in TARGET:
        if total[key] < TARGET[key]:
            deficit.append(key)

    return deficit

def suggest_food(deficit):
    suggestions = {
        "protein": "鶏胸肉・サーモン・豆腐",
        "iron": "ほうれん草・赤身肉・豆類",
        "vitc": "キウイ・パプリカ・みかん"
    }

    result = [suggestions[d] for d in deficit]
    return "、".join(result) if result else "完璧！✨"
