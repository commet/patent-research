"""
papers_db.json → Obsidian 마크다운 노트 변환
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 경로 설정
BASE_DIR = Path(r"C:\Users\admin\documents\research\patent")
VAULT_DIR = BASE_DIR / "vault"
PAPERS_DIR = VAULT_DIR / "Papers"
DB_FILE = BASE_DIR / "papers_db.json"

def sanitize_filename(name):
    """파일명에 사용할 수 없는 문자 제거"""
    # Windows 금지 문자: \ / : * ? " < > |
    invalid_chars = r'[\\/:*?"<>|]'
    name = re.sub(invalid_chars, '', name)
    # 연속 공백 제거
    name = re.sub(r'\s+', ' ', name)
    # 앞뒤 공백/점 제거
    name = name.strip(' .')
    # 너무 긴 이름 자르기
    if len(name) > 100:
        name = name[:100]
    return name

def create_paper_note(paper):
    """논문 마크다운 노트 생성"""

    # YAML frontmatter
    categories = paper.get('categories', [])
    tags = ' '.join([f'#{cat}' for cat in categories])

    frontmatter = f"""---
id: {paper['id']}
title: "{paper['title']}"
author: {paper.get('author') or 'unknown'}
year: {paper.get('year') or 'unknown'}
pages: {paper.get('pages') or 'unknown'}
categories: [{', '.join(categories)}]
file_size_mb: {paper.get('file_size_mb', 0)}
created: {paper.get('creation_date') or 'unknown'}
type: paper
collection: {paper['collection']}
---
"""

    # 본문
    title = paper['title']
    author = paper.get('author') or '*저자 미상*'
    year = paper.get('year') or ''
    year_str = f" ({year})" if year else ""

    # PDF 링크 (상대 경로)
    pdf_path = paper['filepath'].replace('\\', '/')

    body = f"""# {title}

**저자**: {author}{year_str}
**페이지**: {paper.get('pages') or '?'}p | **크기**: {paper.get('file_size_mb', 0)}MB

## 메타데이터
- **ID**: `{paper['id']}`
- **컬렉션**: {paper['collection']}
- **카테고리**: {tags}

## PDF
📄 [원문 열기](file:///{pdf_path})

## 요약
> [!note] 핵심 내용
> (여기에 논문 요약 작성)

## 주요 인용
-

## 메모
-

## 관련 논문
-

"""

    return frontmatter + body

def create_index_note(papers):
    """전체 논문 인덱스 노트 생성"""

    content = """---
type: index
---

# 📚 Research Papers Index

> 자동 생성: """ + datetime.now().strftime('%Y-%m-%d %H:%M') + """

## 통계
"""

    # 통계
    total = len(papers)
    research = len([p for p in papers if p['collection'] == 'research'])
    my_papers = len([p for p in papers if p['collection'] == 'my_papers'])

    content += f"""
- 전체: **{total}**편
- Research papers: {research}편
- My papers: {my_papers}편

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
"""

    # 카테고리 집계
    all_cats = {}
    for p in papers:
        for cat in p.get('categories', []):
            all_cats[cat] = all_cats.get(cat, 0) + 1

    for cat, count in sorted(all_cats.items(), key=lambda x: -x[1]):
        content += f"- [[{cat}]] ({count})\n"

    return content

def main():
    print("Loading database...")
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        db = json.load(f)

    papers = db['papers']
    print(f"Found {len(papers)} papers")

    # 각 논문 노트 생성
    print("\nCreating paper notes...")
    for i, paper in enumerate(papers, 1):
        title = sanitize_filename(paper['title'])
        filename = f"{paper['id']} - {title}.md"
        filepath = PAPERS_DIR / filename

        content = create_paper_note(paper)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  [{i}/{len(papers)}] {filename[:60]}...")

    # 인덱스 노트 생성
    print("\nCreating index note...")
    index_content = create_index_note(papers)
    with open(VAULT_DIR / "Papers Index.md", 'w', encoding='utf-8') as f:
        f.write(index_content)

    # 홈 노트 생성
    print("Creating home note...")
    home_content = """---
type: home
---

# 🏠 Patent Research Vault

## 빠른 링크
- [[Papers Index]] - 전체 논문 목록
- [[Sources Index]] - 1차 사료 (예정)
- [[Notes/]] - 연구 노트

## 최근 작업
```dataview
LIST
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 5
```

## 연구 주제
- [[industrial_revolution|산업혁명과 특허]]
- [[statute_of_monopolies|1624 전매조례]]
- [[venice|베네치아 특허법]]
- [[british_patent|영국 특허 제도]]
"""

    with open(VAULT_DIR / "Home.md", 'w', encoding='utf-8') as f:
        f.write(home_content)

    print(f"\n✅ Done!")
    print(f"   Vault: {VAULT_DIR}")
    print(f"   Papers: {len(papers)} notes created")
    print(f"\n📌 다음 단계: Obsidian에서 vault 폴더 열기")

if __name__ == '__main__':
    main()
