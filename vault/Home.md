---
type: home
---

# 🏠 Patent Research Vault

## 📊 현황

| 컬렉션 | 수량 |
|--------|------|
| 연구 논문 | 124편 |
| 1차 사료 (영국 특허) | 322,874건 |

## 빠른 링크

### 논문
- [[Papers Index]] - 전체 논문 목록 (Dataview 테이블)

### 1차 사료
- [[Sources/Patents Index|영국 역사 특허 DB]] - 1617-1899 (32만건)

### 연구 노트
- [[Notes/]] - 연구 노트

## 최근 작업

```dataview
LIST
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 5
```

## 연구 주제별

### 시대별
- [[industrial_revolution|산업혁명기 (1760-1850)]]
- [[early_modern|근대 초기 (1617-1760)]]

### 주제별
- [[statute_of_monopolies|1624 전매조례]]
- [[venice|베네치아 특허법]]
- [[british_patent|영국 특허 제도]]

## 검색 팁

- `Ctrl+Shift+F` - 전체 검색
- `Ctrl+O` - 빠른 파일 열기
- `Ctrl+G` - 그래프 뷰

---
*Vault 생성: 2026-02-01*
