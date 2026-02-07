# Patent Research Database

특허 역사 연구를 위한 데이터베이스 및 Obsidian vault.

## 개요

이 프로젝트는 **특허 제도의 역사**를 연구하기 위한 자료를 구조화한 것입니다.

| 데이터 | 수량 | 설명 |
|--------|------|------|
| 연구 논문 | 124편 | 특허법, 경제사, 기술사 관련 |
| 영국 역사 특허 | 322,874건 | 1617-1899년 전체 특허 |

## 폴더 구조

```
patent-research/
├── vault/                      # Obsidian vault
│   ├── Home.md                 # 시작 페이지
│   ├── Papers Index.md         # 논문 인덱스 (Dataview 쿼리)
│   ├── Papers/                 # 124개 논문 노트
│   │   ├── R0001 - ....md
│   │   └── M0001 - ....md      # 내 논문
│   └── Sources/
│       └── Patents Index.md    # 1차 사료 가이드
│
├── papers_db.json              # 논문 메타데이터 (JSON)
├── build_papers_db.py          # 논문 DB 생성 스크립트
├── convert_to_obsidian.py      # Obsidian 노트 변환
├── extract_patents_all.py      # 특허 데이터 추출
└── README.md
```

## 사용 방법

### 1. Obsidian vault 열기

1. [Obsidian](https://obsidian.md/) 설치
2. `vault/` 폴더를 vault로 열기
3. **Dataview 플러그인** 설치 (설정 → 커뮤니티 플러그인)

### 2. 대용량 데이터 다운로드

322,874건의 영국 역사 특허 데이터는 용량 문제로 Git에 포함되지 않습니다.

```bash
# Python 실행
python extract_patents_all.py
```

또는 직접 다운로드:
- [Hugging Face: 300 Years of British Patents](https://huggingface.co/datasets/matthewleechen/300YearsOfBritishPatents)

생성되는 파일:
- `patents_all.json` (44MB) - 상세 데이터
- `patents_all.csv` (28MB) - Excel용

## 데이터 설명

### 논문 메타데이터 (papers_db.json)

```json
{
  "id": "R0001",
  "title": "The Economic History of England",
  "author": "...",
  "year": 2016,
  "pages": 23,
  "categories": ["british_patent", "economic_history"],
  "filepath": "...(PDF 경로)..."
}
```

### 영국 역사 특허 (patents_all.csv)

| 필드 | 설명 | 예시 |
|------|------|------|
| id | 특허 ID | GB161700005A |
| year | 등록 연도 | 1617 |
| title | 특허 제목 | Making swords... |
| patentees | 특허권자 | John Smith |
| locations | 지역 | London |

### 시대별 특허 분포

```
1617-1700:      365건   초기 특허 시대
1700-1760:      380건   산업혁명 전야
1760-1800:    1,621건   산업혁명 초기
1800-1852:    9,796건   산업혁명 전성기
1852-1899:  310,712건   신특허법 이후
```

## 연구 주제

이 데이터베이스는 다음 연구 주제를 다룹니다:

- **영국 특허 제도사** (1617-1852)
- **1624년 전매조례** (Statute of Monopolies)
- **산업혁명과 특허**
- **베네치아 특허법** (비교 연구)
- **특허와 혁신의 관계**

## 데이터 출처

- **연구 논문**: 직접 수집한 PDF에서 메타데이터 추출
- **영국 특허 데이터**: [300 Years of British Patents](https://github.com/matthewleechen/UKHistoricalPatents)
  - 원본: Bennet Woodcroft의 특허 명세서 색인

## 요구사항

```bash
pip install pypdf datasets
```

## 라이선스

- 코드: MIT
- 논문 메타데이터: 연구 목적 사용
- 영국 특허 데이터: [원본 데이터셋 라이선스](https://huggingface.co/datasets/matthewleechen/300YearsOfBritishPatents) 참조
