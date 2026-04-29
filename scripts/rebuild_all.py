"""
全日付の HTML を再ビルドするスクリプト
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "pipeline"))
from html_builder import build_daily_page, build_index, SITE_DIR

base = SITE_DIR / "news"
date_dirs = sorted(d for d in base.iterdir() if d.is_dir() and (d / "articles.json").exists())

all_dates = [d.name for d in date_dirs]
print(f"Found {len(date_dirs)} date directories: {all_dates}")

# 最新日のarticles
latest_articles = []
latest_date = ""
if date_dirs:
    latest_date = date_dirs[-1].name
    latest_articles = json.loads((date_dirs[-1] / "articles.json").read_text(encoding="utf-8"))

for i, d in enumerate(date_dirs, 1):
    articles = json.loads((d / "articles.json").read_text(encoding="utf-8"))
    issue_num = i
    p = build_daily_page(d.name, articles, issue_num)
    print(f"  [{i}/{len(date_dirs)}] {d.name} → {p.name}  ({len(articles)} articles)")

# index rebuild
p_idx = build_index(all_dates, latest_articles, latest_date)
print(f"\nIndex → {p_idx}")
print("\nAll pages rebuilt successfully!")
