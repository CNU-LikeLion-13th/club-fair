import pandas as pd
import string
import itertools

input_path = "before.xlsx"

mapping = {
    '외향/내향': {'외향형': '1', '내향형': '0'},
    # '결과/감상': {'감상형': '1', '결과중심형': '0'},
    '실용/취미': {'취미형': '1', '실용형': '0'},
    '열정/자율': {'열정형': '1', '자율형': '0'},
    '협업/정서': {'협업형': '1', '정서형': '0'},
    '외부/내부': {'외부지향형': '1', '내부지향형': '0'},
    '실습/사고': {'실습형': '1', '사고형': '0'},
    '도전/안정': {'도전형': '1', '안정형': '0'}
}

def generate_group_names():
    for size in range(1, 3):
        for s in itertools.product(string.ascii_uppercase, repeat=size):
            yield '그룹 ' + ''.join(s)

df = pd.read_excel(input_path)

def generate_code(row):
    code = ''
    for col in mapping:
        val = row[col]
        code += mapping[col].get(val, 'X') 
    return code

df['코드'] = df.apply(generate_code, axis=1)

group_name_gen = generate_group_names()
group_map = {}
for code in df['코드'].unique():
    group_map[code] = next(group_name_gen)

df['그룹'] = df['코드'].map(group_map)

output_path = "after_grouped.xlsx"
df.to_excel(output_path, index=False)

print("✅ 저장 완료: ", output_path)
