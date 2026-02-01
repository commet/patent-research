"""
Research Papers Database Builder
특허 관련 연구 논문 메타데이터 추출 및 DB 구축
"""

import os
import sys
import json
import re
import warnings
from datetime import datetime
from pathlib import Path

# 경고 억제
warnings.filterwarnings('ignore')

# Windows 콘솔 인코딩 문제 해결
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from pypdf import PdfReader

# 설정
RESEARCH_DIR = Path(r"C:\Users\admin\documents\research\patent\Research papers")
MY_PAPERS_DIR = Path(r"C:\Users\admin\documents\research\patent\My papers")
OUTPUT_DIR = Path(r"C:\Users\admin\documents\research\patent")

# 대용량 PDF 처리 시 스킵할 파일 크기 (MB)
MAX_PDF_SIZE_MB = 200

def extract_year_from_filename(filename):
    """파일명에서 연도 추출"""
    patterns = [
        r'\((\d{4})\)',
        r'_(\d{4})(?:_|\.)',
        r'(\d{4})-\d{4}',
        r'(\d{4})~\d{4}',
    ]
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            year = int(match.group(1))
            if 1400 <= year <= 2100:
                return year
    return None

def extract_category_from_filename(filename):
    """파일명에서 카테고리 태그 추출"""
    categories = []

    tag_patterns = [
        (r'\(사료\)', 'primary_source'),
        (r'\(original\)', 'primary_source'),
        (r'\(Working paper\)', 'working_paper'),
        (r'\(기술-과학\)', 'tech_science'),
        (r'\(Early \d+C', 'early_modern'),
        (r'Wikipedia', 'reference'),
        (r'Book Review', 'book_review'),
    ]

    for pattern, category in tag_patterns:
        if re.search(pattern, filename, re.IGNORECASE):
            categories.append(category)

    topic_keywords = {
        'industrial_revolution': ['Industrial Revolution', 'Industrialisation', 'Industrialization'],
        'statute_of_monopolies': ['Statute of Monopolies', '1624'],
        'venice': ['Venice', 'Venetian', '베니스'],
        'british_patent': ['British Patent', 'English Patent', 'England'],
        'innovation': ['Innovation', 'Invention'],
        'economic_history': ['Economic History', '경제'],
        'legal_history': ['Law', 'Legal', '법제사', '법'],
        'patent_policy': ['Policy', 'Reform'],
    }

    for topic, keywords in topic_keywords.items():
        for kw in keywords:
            if kw.lower() in filename.lower():
                categories.append(topic)
                break

    return list(set(categories)) if categories else ['general']

def parse_pdf_date(date_str):
    """PDF 날짜 문자열 파싱"""
    if not date_str:
        return None
    try:
        if isinstance(date_str, str):
            if date_str.startswith('D:'):
                date_str = date_str[2:]
            date_part = date_str[:8]
            return datetime.strptime(date_part, '%Y%m%d').isoformat()[:10]
    except:
        pass
    return None

def extract_pdf_metadata(filepath, skip_large=True):
    """PDF 파일에서 메타데이터 추출 (대용량 파일 안전 처리)"""
    try:
        file_size_mb = filepath.stat().st_size / (1024 * 1024)

        # 대용량 파일은 메타데이터만 추출 (페이지 수 계산 스킵)
        if skip_large and file_size_mb > MAX_PDF_SIZE_MB:
            return {
                'title': None,
                'author': None,
                'subject': None,
                'creator': None,
                'producer': None,
                'creation_date': None,
                'pages': None,
                'note': f'Large file ({file_size_mb:.1f}MB) - metadata extraction skipped'
            }

        reader = PdfReader(filepath, strict=False)
        metadata = reader.metadata or {}

        info = {
            'title': str(metadata.get('/Title', '')) if metadata.get('/Title') else None,
            'author': str(metadata.get('/Author', '')) if metadata.get('/Author') else None,
            'subject': str(metadata.get('/Subject', '')) if metadata.get('/Subject') else None,
            'creator': str(metadata.get('/Creator', '')) if metadata.get('/Creator') else None,
            'producer': str(metadata.get('/Producer', '')) if metadata.get('/Producer') else None,
            'creation_date': parse_pdf_date(str(metadata.get('/CreationDate', ''))),
            'pages': len(reader.pages) if file_size_mb < 50 else None,
        }

        for key in ['title', 'author', 'subject', 'creator', 'producer']:
            if info[key] and (info[key] == 'N/A' or not info[key].strip()):
                info[key] = None

        return info
    except Exception as e:
        return {
            'title': None,
            'author': None,
            'subject': None,
            'creator': None,
            'producer': None,
            'creation_date': None,
            'pages': None,
            'error': str(e)[:100]
        }

def build_paper_entry(filepath, paper_id, collection='research'):
    """논문 항목 생성"""
    filename = filepath.name

    try:
        file_stat = filepath.stat()
        file_size_mb = round(file_stat.st_size / (1024 * 1024), 2)
        modified_date = datetime.fromtimestamp(file_stat.st_mtime).isoformat()[:10]
    except:
        file_size_mb = 0
        modified_date = None

    pdf_meta = extract_pdf_metadata(filepath)
    year = extract_year_from_filename(filename)
    categories = extract_category_from_filename(filename)

    title = pdf_meta.get('title')
    if not title:
        title = filename.replace('.pdf', '')
        title = re.sub(r'^\([^)]+\)\s*', '', title)
        title = re.sub(r'^[\d\-\.]+\s*', '', title)

    entry = {
        'id': paper_id,
        'filename': filename,
        'filepath': str(filepath),
        'collection': collection,
        'title': title,
        'author': pdf_meta.get('author'),
        'year': year,
        'pages': pdf_meta.get('pages'),
        'categories': categories,
        'subject': pdf_meta.get('subject'),
        'creation_date': pdf_meta.get('creation_date'),
        'file_size_mb': file_size_mb,
        'modified_date': modified_date,
    }

    if 'error' in pdf_meta:
        entry['extraction_error'] = pdf_meta['error']
    if 'note' in pdf_meta:
        entry['note'] = pdf_meta['note']

    return entry

def build_database():
    """전체 데이터베이스 구축"""
    papers = []
    paper_id = 1

    print("Processing Research papers...")
    if RESEARCH_DIR.exists():
        pdf_files = sorted(RESEARCH_DIR.glob('*.pdf'))
        total = len(pdf_files)
        for i, filepath in enumerate(pdf_files, 1):
            try:
                short_name = filepath.name[:55] + '...' if len(filepath.name) > 55 else filepath.name
                print(f"  [{i}/{total}] {short_name}")
                entry = build_paper_entry(filepath, f"R{paper_id:04d}", 'research')
                papers.append(entry)
                paper_id += 1
            except Exception as e:
                print(f"    ERROR: {str(e)[:50]}")

    print("\nProcessing My papers...")
    my_paper_id = 1
    if MY_PAPERS_DIR.exists():
        pdf_files = sorted(MY_PAPERS_DIR.glob('*.pdf'))
        total = len(pdf_files)
        for i, filepath in enumerate(pdf_files, 1):
            try:
                short_name = filepath.name[:55] + '...' if len(filepath.name) > 55 else filepath.name
                print(f"  [{i}/{total}] {short_name}")
                entry = build_paper_entry(filepath, f"M{my_paper_id:04d}", 'my_papers')
                papers.append(entry)
                my_paper_id += 1
            except Exception as e:
                print(f"    ERROR: {str(e)[:50]}")

    db = {
        'metadata': {
            'created': datetime.now().isoformat(),
            'total_papers': len(papers),
            'research_count': len([p for p in papers if p['collection'] == 'research']),
            'my_papers_count': len([p for p in papers if p['collection'] == 'my_papers']),
        },
        'papers': papers
    }

    output_path = OUTPUT_DIR / 'papers_db.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Database saved to: {output_path}")
    print(f"Total papers: {len(papers)}")

    print("\nSummary by Category:")
    all_categories = {}
    for paper in papers:
        for cat in paper.get('categories', ['unknown']):
            all_categories[cat] = all_categories.get(cat, 0) + 1

    for cat, count in sorted(all_categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    return db

if __name__ == '__main__':
    try:
        db = build_database()
        print("\nDone!")
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)
