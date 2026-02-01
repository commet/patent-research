---
type: index
---

# 🏛️ British Historical Patents (1617-1899)

> **322,874건** 영국 역사 특허 데이터베이스
> 출처: [300 Years of British Patents](https://github.com/matthewleechen/UKHistoricalPatents)

## 데이터 파일

| 파일 | 크기 | 용도 |
|------|------|------|
| `patents_all.csv` | 28MB | Excel/스프레드시트 |
| `patents_all.json` | 44MB | 프로그래밍/분석 |

📂 위치: `C:\Users\admin\documents\research\patent\`

## 시대별 분포

```
시대          특허 수    비고
─────────────────────────────────────
1617-1700       365     초기 특허 시대
1700-1760       380     산업혁명 전야
1760-1800     1,621     산업혁명 초기
1800-1852     9,796     산업혁명 전성기 (구제도)
─────────────────────────────────────
1852-1899   310,712     신특허법 이후 (폭발적 증가)
```

## CSV 필드

| 필드 | 설명 | 예시 |
|------|------|------|
| id | 특허 ID | GB161700005A |
| year | 등록 연도 | 1617 |
| title | 특허 제목 | Making swords and rapiers |
| patentees | 특허권자 | John Smith; James Brown |
| locations | 지역 | London; Manchester |

## 검색 방법

### Excel에서 검색
1. `patents_all.csv` 열기
2. `Ctrl+F`로 검색
3. 필터 기능으로 연도별 분류

### Python으로 분석
```python
import pandas as pd
df = pd.read_csv('patents_all.csv')

# 특정 연도 필터
df_1760s = df[(df['year'] >= 1760) & (df['year'] < 1770)]

# 키워드 검색
df[df['title'].str.contains('steam', case=False, na=False)]
```

## 연구 활용 예시

### 1. 산업혁명기 직물 특허 분석
```python
textile_keywords = ['cotton', 'wool', 'spinning', 'weaving', 'loom']
pattern = '|'.join(textile_keywords)
df[df['title'].str.contains(pattern, case=False, na=False)]
```

### 2. 특정 발명가 추적
```python
df[df['patentees'].str.contains('Watt', na=False)]
```

## 관련 자료

- [[R0031 - British patent system during the Industrial Revolution|Bottomley의 특허 시스템 연구]]
- [[R0077 - Patents for invention- setting the stage for the Industrial Revolution|산업혁명과 특허]]

## 주요 특허 노트

> 개별 특허 연구 시 여기에 링크 추가

- [ ] James Watt 증기기관 특허 (1769)
- [ ] Arkwright 방적기 특허 (1769)
- [ ] 초기 특허 (1617-1630) 분석

