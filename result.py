import random

# 전체 리스트 (이름 - 아이디 형태 또는 아이디만)
people = [
    "이혜주 : heajuuuuu",
    "안규리 : yesmandarine",
    "오시우 : swoouou",
    "김다은 : zr__a948",
    "이영준 : joon_0304",
    "trail_jin0235",
    "한규빈 : hgyuhuygh",
    "미령 : mizuka_livingwater",
    "김가희 : *rlarkgml17",
    "강선미 : rkd.tjsal",
    "aseunxa",
    "이수연 : archit__sy",
    "진우신 : wooshin.jin",
    "im*.sunny_._",
    "주연 : yeon.*.5845",
    "한연수 : nyeontn",
    "하승현 : hsh_cnuhi",
    "박종현 : jonghhnn",
    "sleunn__",
    "윤경민 : kminyn",
    "hyohyorin0",
    "joo.seunghoon",
    "김경민 : kimkm_03",
    "김지유 : jiyujoy0228",
    "송경민 : g.m.song*",
    "김우형 : woobro02",
    "윤민지 : m_nnzy",
    "장현성: hsjjj_ang"
]

# 뽑을 인원 수 설정
n = 3  # 원하는 인원 수로 변경

# 랜덤 추첨
winners = random.sample(people, n)

# 결과 출력
print("🎉 커피 쿠폰 당첨자 🎉")
for winner in winners:
    print("-", winner)
