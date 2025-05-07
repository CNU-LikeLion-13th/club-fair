from flask_cors import CORS

from flask import Flask, request, jsonify
import pandas as pd
import random

app = Flask(__name__)
CORS(app)

# 1. 데이터 불러오기 및 전처리
df = pd.read_excel("after_grouped.xlsx")
df['코드'] = df['코드'].astype(str).str.zfill(7)
code_to_group = dict(zip(df['코드'], df['그룹']))
group_to_clubnames = df.groupby('그룹')['동아리명'].apply(list).to_dict()
code_frequency = df['코드'].value_counts().to_dict()

# 2. 해밍 거리 함수
def hamming_distance(code1, code2):
    return sum(c1 != c2 for c1, c2 in zip(str(code1), str(code2)))

# 3. 추천 함수
def recommend_clubs(user_code, max_recommendations=3):
    user_code = str(user_code).zfill(7)

    if user_code in code_to_group:
        group = code_to_group[user_code]
        clubs = group_to_clubnames.get(group, [])
        return random.sample(clubs, min(len(clubs), max_recommendations))

    candidates_1 = [code for code in code_to_group if hamming_distance(user_code, code) == 1]
    if candidates_1:
        groups = {code_to_group[c] for c in candidates_1}
        clubs = sum([group_to_clubnames.get(g, []) for g in groups], [])
        return random.sample(list(set(clubs)), min(len(set(clubs)), max_recommendations))

    candidates_2 = [code for code in code_to_group if hamming_distance(user_code, code) == 2]
    if candidates_2:
        groups = {code_to_group[c] for c in candidates_2}
        clubs = sum([group_to_clubnames.get(g, []) for g in groups], [])
        return random.sample(list(set(clubs)), min(len(set(clubs)), max_recommendations))

    fallback_codes = sorted(code_frequency.items(), key=lambda x: x[1], reverse=True)
    for code, _ in fallback_codes:
        group = code_to_group[code]
        clubs = group_to_clubnames.get(group, [])
        if clubs:
            return random.sample(clubs, min(len(clubs), max_recommendations))
    return []

# 4. API 엔드포인트
@app.route("/recommend", methods=["POST"])
def recommend_api():
    data = request.get_json()
    user_code = data.get("code", "")
    if len(user_code) == 7 and set(user_code) <= {"0", "1"}:
        result = recommend_clubs(user_code)
        return jsonify({"recommendations": result})
    else:
        return jsonify({"error": "Invalid code format"}), 400

# 5. 서버 실행
if __name__ == "__main__":
    app.run(debug=True)
