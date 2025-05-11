// clubs.js - after_grouped.xlsx를 변환한 JSON 데이터 + 추천 함수 포함

  // 2. 추천 로직: Python 코드와 동일한 흐름 구현
  function hammingDistance(code1, code2) {
    return [...code1].filter((c, i) => c !== code2[i]).length;
  }
  
  function recommendClubsJS(userCode, max = 1) {
    const normalizedCode = userCode.padStart(7, '0');
  
    // 코드 → 그룹, 그룹 → 동아리명 맵 생성
    const codeToGroup = {};
    const groupToClubs = {};
    const codeFrequency = {};
  
    clubData.forEach(({ 코드, 그룹, 동아리명 }) => {
      if (!groupToClubs[그룹]) groupToClubs[그룹] = [];
      groupToClubs[그룹].push(동아리명);
      codeToGroup[코드] = 그룹;
      codeFrequency[코드] = (codeFrequency[코드] || 0) + 1;
    });
  
    // 정확히 일치
    if (codeToGroup[normalizedCode]) {
      const group = codeToGroup[normalizedCode];
      const clubs = groupToClubs[group] || [];
      return pickRandom(clubs, max);
    }
  
    // 해밍 거리 1
    const candidates1 = Object.keys(codeToGroup).filter(c => hammingDistance(c, normalizedCode) === 1);
    if (candidates1.length > 0) {
      const groups = new Set(candidates1.map(c => codeToGroup[c]));
      const clubs = [...groups].flatMap(g => groupToClubs[g] || []);
      return pickRandom([...new Set(clubs)], max);
    }
  
    // 해밍 거리 2
    const candidates2 = Object.keys(codeToGroup).filter(c => hammingDistance(c, normalizedCode) === 2);
    if (candidates2.length > 0) {
      const groups = new Set(candidates2.map(c => codeToGroup[c]));
      const clubs = [...groups].flatMap(g => groupToClubs[g] || []);
      return pickRandom([...new Set(clubs)], max);
    }
  
    // fallback: 가장 빈도 높은 코드 기반 그룹 추천
    const fallbackCode = Object.entries(codeFrequency).sort((a, b) => b[1] - a[1])[0][0];
    const fallbackGroup = codeToGroup[fallbackCode];
    const fallbackClubs = groupToClubs[fallbackGroup] || [];
    return pickRandom(fallbackClubs, max);
  }
  
  // 유틸 함수: 리스트에서 n개 랜덤 선택
  function pickRandom(arr, n) {
    const shuffled = arr.sort(() => 0.5 - Math.random());
    return shuffled.slice(0, Math.min(n, arr.length));
  }
  
  // export처럼 global에서 접근할 수 있게 window에 등록
  window.recommendClubsJS = recommendClubsJS;
  