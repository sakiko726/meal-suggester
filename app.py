import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { motion } from "framer-motion";

食材データ（追加し放題）
const FOODS = [
  { name: "さつまいも", caloriesPerGram: 1.3 },
  { name: "白ごはん", caloriesPerGram: 1.68 },
  { name: "鶏胸肉", caloriesPerGram: 1.65 },
  { name: "卵", caloriesPerGram: 1.55 },
  { name: "アボカド", caloriesPerGram: 1.6 },
  { name: "りんご", caloriesPerGram: 0.52 },
  { name: "バナナ", caloriesPerGram: 0.86 },
  { name: "ブロッコリー", caloriesPerGram: 0.33 },
  { name: "トマト", caloriesPerGram: 0.18 },
  { name: "レタス", caloriesPerGram: 0.15 },
　{ name: "オートミール", caloriesPerGram: 3.8 },
  { name: "納豆", caloriesPerGram: 2.0 },
  { name: "豆腐", caloriesPerGram: 0.76 },
  { name: "味噌汁", caloriesPerGram: 0.5 },
  { name: "ヨーグルト", caloriesPerGram: 0.62 },
  { name: "ツナ（水煮）", caloriesPerGram: 0.8 },
  { name: "サーモン", caloriesPerGram: 1.5 },
  { name: "チーズ", caloriesPerGram: 3.56 },
  { name: "きゅうり", caloriesPerGram: 0.15 },
  { name: "キャベツ", caloriesPerGram: 0.23 },

  { name: "玄米", caloriesPerGram: 1.65 },
  { name: "梅干し", caloriesPerGram: 0.33 },
  { name: "鮭の塩焼き", caloriesPerGram: 2.0 },
  { name: "スクランブルエッグ", caloriesPerGram: 1.6 },
  { name: "目玉焼き", caloriesPerGram: 1.7 },
  { name: "トースト（食パン）", caloriesPerGram: 2.6 },
  { name: "ベーグル", caloriesPerGram: 2.5 },
  { name: "クロワッサン", caloriesPerGram: 4.0 },
  { name: "バター", caloriesPerGram: 7.2 },
  { name: "ジャム", caloriesPerGram: 2.6 },

  { name: "うどん", caloriesPerGram: 1.05 },
  { name: "そば（茹で）", caloriesPerGram: 1.13 },
  { name: "パスタ（乾麺）", caloriesPerGram: 3.6 },
  { name: "鶏そぼろ", caloriesPerGram: 2.3 },
  { name: "牛丼の具", caloriesPerGram: 1.8 },
  { name: "豚汁", caloriesPerGram: 0.7 },
  { name: "カレー（ルー）", caloriesPerGram: 1.2 },
  { name: "ごはん（炒飯）", caloriesPerGram: 2.0 },
  { name: "オムライス", caloriesPerGram: 1.7 },
  { name: "親子丼", caloriesPerGram: 1.4 },

  { name: "唐揚げ", caloriesPerGram: 2.9 },
  { name: "焼き魚（鯖）", caloriesPerGram: 2.3 },
  { name: "麻婆豆腐", caloriesPerGram: 1.1 },
  { name: "餃子（焼き）", caloriesPerGram: 2.0 },
  { name: "春巻き", caloriesPerGram: 2.2 },
  { name: "焼きそば", caloriesPerGram: 1.8 },
  { name: "ハンバーグ", caloriesPerGram: 2.5 },
  { name: "ステーキ（牛）", caloriesPerGram: 2.7 },
  { name: "豚ロース（焼き）", caloriesPerGram: 2.4 },
  { name: "鶏つくね", caloriesPerGram: 1.8 },

  { name: "さば缶（水煮）", caloriesPerGram: 1.8 },
  { name: "ツナ（油漬け）", caloriesPerGram: 2.3 },
  { name: "厚揚げ", caloriesPerGram: 1.2 },
  { name: "きのこ炒め", caloriesPerGram: 0.7 },
  { name: "野菜炒め", caloriesPerGram: 0.9 },
  { name: "ほうれん草おひたし", caloriesPerGram: 0.3 },
  { name: "きんぴらごぼう", caloriesPerGram: 1.2 },
  { name: "ポテトサラダ", caloriesPerGram: 1.4 },
  { name: "マカロニサラダ", caloriesPerGram: 1.6 },
  { name: "海藻サラダ", caloriesPerGram: 0.3 },

  { name: "おにぎり（梅）", caloriesPerGram: 1.7 },
  { name: "おにぎり（鮭）", caloriesPerGram: 1.8 },
  { name: "サバ味噌煮", caloriesPerGram: 2.0 },
  { name: "肉じゃが", caloriesPerGram: 0.9 },
  { name: "筑前煮", caloriesPerGram: 1.1 },
  { name: "ミートソース", caloriesPerGram: 1.5 },
  { name: "カルボナーラ", caloriesPerGram: 2.0 },
  { name: "ペペロンチーノ", caloriesPerGram: 1.8 },
  { name: "ナポリタン", caloriesPerGram: 1.6 },
  { name: "ラーメン", caloriesPerGram: 1.5 },

  { name: "チャーハン", caloriesPerGram: 2.1 },
  { name: "天津飯", caloriesPerGram: 1.8 },
  { name: "中華丼", caloriesPerGram: 1.2 },
  { name: "麻婆茄子", caloriesPerGram: 1.3 },
  { name: "焼き鳥（もも）", caloriesPerGram: 2.0 },
  { name: "焼き鳥（ねぎま）", caloriesPerGram: 1.8 },
  { name: "焼き鳥（レバー）", caloriesPerGram: 1.4 },
  { name: "冷奴", caloriesPerGram: 0.76 },
  { name: "茶碗蒸し", caloriesPerGram: 0.9 },
  { name: "高野豆腐（戻し）", caloriesPerGram: 0.85 }
];

export default function CalorieCoach() {
  const [selected, setSelected] = useState(null);
  const [grams, setGrams] = useState(0);
  const [logs, setLogs] = useState([]);

  const handleAdd = () => {
    if (!selected || grams <= 0) return;
    const cal = selected.caloriesPerGram * grams;
    setLogs([...logs, { name: selected.name, grams, cal }]);
    setGrams(0);
    setSelected(null);
  };

  const totalCalories = logs.reduce((a, b) => a + b.cal, 0);

  const suggestion = () => {
    if (totalCalories < 300) return "まだ軽めなので、たんぱく質を追加してもOK！";
    if (totalCalories < 600) return "バランス良いよ！次は野菜を増やすと◎";
    return "少しハイカロリーなので、次は低カロリー食材中心にしてみて！";
  };

  return (
    <div className="p-6 max-w-xl mx-auto space-y-6">
      <motion.h1 className="text-2xl font-bold text-center" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        カロリーコーチ
      </motion.h1>

      {/* 食材選択 */}
      <Card className="p-4">
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-2">
            {FOODS.map((f) => (
              <Button
                key={f.name}
                variant={selected?.name === f.name ? "default" : "secondary"}
                onClick={() => setSelected(f)}
                className="rounded-xl"
              >
                {f.name}
              </Button>
            ))}
          </div>

          {/* グラム入力 */}
          <Input
            type="number"
            placeholder="グラム数を入力"
            value={grams}
            onChange={(e) => setGrams(Number(e.target.value))}
          />

          <Button onClick={handleAdd} className="w-full rounded-xl text-lg py-6">
            追加する
          </Button>
        </CardContent>
      </Card>

      {/* ログ表示 */}
      <Card className="p-4">
        <CardContent className="space-y-3">
          <h2 className="text-xl font-bold">今日の記録</h2>
          {logs.map((l, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="p-2 bg-gray-100 rounded-xl"
            >
              {l.name}：{l.grams}g（{Math.round(l.cal)} kcal）
            </motion.div>
          ))}
          <p className="text-lg font-bold">合計：{Math.round(totalCalories)} kcal</p>
        </CardContent>
      </Card>

      {/* 提案 */}
      <Card className="p-4">
        <CardContent>
          <h2 className="text-xl font-bold mb-2">次のアドバイス</h2>
          <p>{suggestion()}</p>
        </CardContent>
      </Card>
    </div>
  );
}

