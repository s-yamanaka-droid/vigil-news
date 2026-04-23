"""
VIGIL — Main Pipeline
RSS → Haiku要約 → Geminiスライド → HTML生成 → GitHub push
"""
import sys
import logging
from datetime import datetime
from pathlib import Path
import concurrent.futures

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "agents/cmo/x_agent"))

from researcher import fetch_latest
from generator import generate_articles
from slide_maker import generate_slide
from html_builder import build_daily_page, build_index, SITE_DIR
from deploy import git_push

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / f"{datetime.now().strftime('%Y%m%d')}.log"),
    ],
)
log = logging.getLogger(__name__)


def run(date_str: str = None, dry_run: bool = False, skip_slides: bool = False):
    date_str = date_str or datetime.now().strftime("%Y-%m-%d")
    log.info(f"=== VIGIL {date_str} ===")

    # 1. RSS収集
    log.info("1. RSS収集")
    raw = fetch_latest(max_per_feed=4)
    log.info(f"   {len(raw)}件取得")

    # 2. Haiku要約
    log.info("2. 記事生成（Haiku）")
    articles = generate_articles(raw)
    log.info(f"   {len(articles)}件生成")

    # 3. Geminiスライド生成（並列）
    if not skip_slides:
        log.info("3. スライド生成（Gemini 3.1 Flash）")
        img_dir = SITE_DIR / "assets" / "images" / date_str
        img_dir.mkdir(parents=True, exist_ok=True)

        def make_slide(args):
            i, a = args
            out = img_dir / f"topic_{i}.png"
            if out.exists():
                return i, True
            ok = generate_slide(
                title=a["title"], category=a.get("category",""),
                source=a.get("source",""), summary=a.get("lede",""),
                keypoints=a.get("keypoints",[]), output_path=out,
            )
            return i, ok

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
            results = list(ex.map(make_slide, enumerate(articles, 1)))
        ok_count = sum(1 for _, ok in results if ok)
        log.info(f"   {ok_count}/{len(articles)}枚生成完了")

    # 4. HTML生成
    log.info("4. HTML生成")
    daily_path = build_daily_page(date_str, articles)
    log.info(f"   {daily_path}")

    all_dates = sorted([d.name for d in (SITE_DIR / "news").iterdir() if d.is_dir()])
    index_path = build_index(all_dates, articles, date_str)
    log.info(f"   {index_path}")

    # 5. デプロイ
    if not dry_run:
        log.info("5. GitHub push")
        ok = git_push(f"dispatch: {date_str} — {len(articles)} items")
        log.info(f"   {'✓ 完了' if ok else '✗ 失敗'}")
    else:
        log.info("5. [DRY RUN] push スキップ")
        log.info(f"   サイトプレビュー: {SITE_DIR}/index.html")

    log.info("=== 完了 ===")


if __name__ == "__main__":
    dry = "--dry" in sys.argv
    skip = "--skip-slides" in sys.argv
    run(dry_run=dry, skip_slides=skip)
