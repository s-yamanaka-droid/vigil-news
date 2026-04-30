"""指定日の topic_*.png を新プロンプトで再生成"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from pipeline.slide_maker import generate_slide

DATE = sys.argv[1] if len(sys.argv) > 1 else "2026-04-30"
articles_path = ROOT / "docs" / "news" / DATE / "articles.json"
img_dir = ROOT / "docs" / "assets" / "images" / DATE
img_dir.mkdir(parents=True, exist_ok=True)

articles = json.loads(articles_path.read_text(encoding="utf-8"))
print(f"[{DATE}] Regenerating {len(articles)} slides with new infographic prompt...")

for i, a in enumerate(articles, 1):
    out = img_dir / f"topic_{i}.png"
    print(f"  [{i}/{len(articles)}] {a.get('title','')[:40]}...")
    ok = generate_slide(
        title=a.get("title", ""),
        category=a.get("category", "AI情報"),
        source=a.get("source", ""),
        summary=a.get("lede", "") or a.get("summary", ""),
        keypoints=a.get("keypoints", []),
        output_path=out,
    )
    print(f"      → {'OK' if ok else 'FAIL'}: {out.name}")

print("Done.")
