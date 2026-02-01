"""
영국 역사 특허 데이터셋 다운로드 및 확인
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from datasets import load_dataset
import json

print("Loading dataset from Hugging Face...")
print("(첫 실행시 다운로드에 시간이 걸릴 수 있습니다)")

# 데이터셋 로드 (streaming=True로 메모리 절약)
try:
    ds = load_dataset("matthewleechen/300YearsOfBritishPatents", streaming=True)

    print("\n데이터셋 구조:")
    print(ds)

    # 샘플 몇 개 확인
    print("\n샘플 데이터 (처음 3개):")
    for i, item in enumerate(ds['train'].take(3)):
        print(f"\n--- 특허 {i+1} ---")
        for key, value in item.items():
            if isinstance(value, str) and len(value) > 200:
                print(f"{key}: {value[:200]}...")
            else:
                print(f"{key}: {value}")

except Exception as e:
    print(f"Error: {e}")
    print("\n대체 방법: 직접 다운로드")
    print("https://huggingface.co/datasets/matthewleechen/300YearsOfBritishPatents")
