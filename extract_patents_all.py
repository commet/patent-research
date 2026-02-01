"""
영국 역사 특허 데이터 전체 추출 (1617-1899)
322,874건 전체
"""
import sys
import json
import csv
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from datasets import load_dataset

OUTPUT_DIR = Path(r"C:\Users\admin\documents\research\patent")

print("Loading dataset...")
ds = load_dataset("matthewleechen/300YearsOfBritishPatents", streaming=True)

patents = []
count = 0

print("Extracting ALL patents (1617-1899)...")
print("약 322,874건 - 시간이 걸립니다...")

for item in ds['train']:
    patent = {
        'id': item.get('patent_id', ''),
        'year': item.get('year', 0),
        'title': item.get('patent_title', '').strip(),
        'has_full_text': bool(item.get('full_text')),
    }

    # 엔티티에서 추출
    entities = item.get('front_page_entities', {})
    if isinstance(entities, dict):
        patent['patentees'] = entities.get('PERSON', [])
        patent['locations'] = entities.get('GPE', [])
        patent['organizations'] = entities.get('ORG', [])

    patents.append(patent)
    count += 1

    if count % 5000 == 0:
        year = patent['year']
        print(f"  {count:,} patents processed (year: {year})...")

print(f"\nTotal: {count:,} patents extracted")

# JSON 저장
json_path = OUTPUT_DIR / "patents_all.json"
print(f"\nSaving JSON... (큰 파일, 잠시 대기)")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump({
        'metadata': {
            'total': count,
            'period': '1617-1899',
            'source': 'matthewleechen/300YearsOfBritishPatents'
        },
        'patents': patents
    }, f, ensure_ascii=False)
print(f"Saved: {json_path}")

# CSV 저장
csv_path = OUTPUT_DIR / "patents_all.csv"
print("Saving CSV...")
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'year', 'title', 'patentees', 'locations'])
    for p in patents:
        patentees = '; '.join(p.get('patentees', [])[:3])
        locations = '; '.join(p.get('locations', [])[:2])
        writer.writerow([p['id'], p['year'], p['title'], patentees, locations])
print(f"Saved: {csv_path}")

# 연도별 통계 (10년 단위)
print("\n연도별 특허 수 (10년 단위):")
year_counts = {}
for p in patents:
    y = p['year']
    year_counts[y] = year_counts.get(y, 0) + 1

decade_counts = {}
for y, c in year_counts.items():
    decade = (y // 10) * 10
    decade_counts[decade] = decade_counts.get(decade, 0) + c

for decade in sorted(decade_counts.keys()):
    bar = '█' * (decade_counts[decade] // 500)
    print(f"  {decade}s: {decade_counts[decade]:6,} {bar}")

print("\n✅ 완료!")
