---
type: index
---

# 📚 Research Papers Index

> 자동 생성: 2026-02-01 21:29

## 통계

- 전체: **124**편
- Research papers: 119편
- My papers: 5편

## Dataview 쿼리

### 전체 논문 목록
```dataview
TABLE author, year, pages
FROM "Papers"
WHERE type = "paper"
SORT year DESC
```

### 카테고리별
```dataview
TABLE length(rows) as Count
FROM "Papers"
WHERE type = "paper"
FLATTEN categories as cat
GROUP BY cat
SORT rows.length DESC
```

### 최근 추가
```dataview
TABLE title, author
FROM "Papers"
WHERE type = "paper"
SORT file.ctime DESC
LIMIT 10
```

## 카테고리 목록
- [[general]] (50)
- [[legal_history]] (21)
- [[innovation]] (21)
- [[british_patent]] (16)
- [[industrial_revolution]] (13)
- [[economic_history]] (8)
- [[primary_source]] (7)
- [[patent_policy]] (6)
- [[statute_of_monopolies]] (4)
- [[venice]] (3)
- [[working_paper]] (2)
- [[early_modern]] (1)
- [[book_review]] (1)
- [[tech_science]] (1)
- [[reference]] (1)
