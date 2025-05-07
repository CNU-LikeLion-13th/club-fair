import pandas as pd
import random

# 1. 데이터 불러오기
df = pd.read_excel("after_grouped.xlsx")

# 2. 코드 값을 문자열로 변환 (앞자리 0 보존)
df['코드'] = df['코드'].astype(str).str.zfill(7)

# 3. 코드 → 그룹 매핑 / 그룹 → 동아리명 매핑
code_to_group = dict(zip(df['코드'], df['그룹']))
group_to_clubnames = df.groupby('그룹')['동아리명'].apply(list).to_dict()
code_frequency = df['코드'].value_counts().to_dict()

# 4. 해밍 거리 계산 함수
def hamming_distance(code1, code2):
    return sum(c1 != c2 for c1, c2 in zip(str(code1), str(code2)))

# 5. 추천 함수 (동아리명 기준)
def recommend_clubs(user_code, max_recommendations=3):
    user_code = str(user_code).zfill(7)
    
    # 1. 정확히 일치하는 코드의 그룹
    if user_code in code_to_group:
        group = code_to_group[user_code]
        clubs = group_to_clubnames.get(group, [])
        return random.sample(clubs, min(len(clubs), max_recommendations))

    # 2. 해밍 거리 1
    candidates_1 = [code for code in code_to_group if hamming_distance(user_code, code) == 1]
    if candidates_1:
        groups = {code_to_group[c] for c in candidates_1}
        clubs = sum([group_to_clubnames.get(g, []) for g in groups], [])
        unique_clubs = list(set(clubs))
        return random.sample(unique_clubs, min(len(unique_clubs), max_recommendations))

    # 3. 해밍 거리 2
    candidates_2 = [code for code in code_to_group if hamming_distance(user_code, code) == 2]
    if candidates_2:
        groups = {code_to_group[c] for c in candidates_2}
        clubs = sum([group_to_clubnames.get(g, []) for g in groups], [])
        unique_clubs = list(set(clubs))
        return random.sample(unique_clubs, min(len(unique_clubs), max_recommendations))

    # 4. fallback: 가장 빈도가 높은 그룹 기준 추천
    fallback_codes = sorted(code_frequency.items(), key=lambda x: x[1], reverse=True)
    for code, _ in fallback_codes:
        group = code_to_group[code]
        clubs = group_to_clubnames.get(group, [])
        if clubs:
            return random.sample(clubs, min(len(clubs), max_recommendations))
    
    return []

# 6. 실행
if __name__ == "__main__":
    example_code = input("사용자의 7자리 코드 입력 (예: 1010101): ")
    if len(example_code) == 7 and set(example_code) <= {'0', '1'}:
        recommendations = recommend_clubs(example_code)
        print("✅ 추천 동아리:", recommendations)
    else:
        print("❌ 7자리 이진수 형식으로 입력해주세요 (예: 1010101)")
