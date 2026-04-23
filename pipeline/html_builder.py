"""
VIGIL — HTML Builder v3
重厚エディトリアルデザイン × 動的インタラクション
"""
from datetime import datetime
from pathlib import Path

SITE_DIR = Path(__file__).parent.parent / "docs"
FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Barlow+Condensed:wght@600;700;800;900&"
    "family=Inter:wght@400;500;600;700&"
    "family=JetBrains+Mono:wght@400;500;600;700&"
    "family=Noto+Sans+JP:wght@400;500;700&display=swap"
)

WEEKDAYS_EN = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
MONTHS_EN   = ["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE",
               "JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"]


# ── 共通パーツ ────────────────────────────────────────────────

def _head(title: str, desc: str, css_path: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="{css_path}" />
</head>
<body>"""


def _dispatch(issue: str, date_str: str, count: int, build: str) -> str:
    """最上部の黒いティッカーリボン"""
    inner = (
        f'<span class="tick">VIGIL №{issue}</span>'
        f'<span class="sep">/</span>'
        f'<span>{date_str}</span>'
        f'<span class="sep">/</span>'
        f'<span>MORNING EDITION</span>'
        f'<span class="sep">/</span>'
        f'<span>{count} ITEMS</span>'
        f'<span class="sep">/</span>'
        f'<span>BUILD {build}</span>'
        f'<span class="sep">/</span>'
        f'<span class="live">LIVE</span>'
        f'<span class="sep">/</span>'
        f'<span>CURATED BY 山中秀斗</span>'
    )
    return f'<div class="dispatch"><div class="container row">{inner}</div></div>'


def _masthead(root: str, today_str: str, weekday: str) -> str:
    """スティッキーナビ"""
    nav_items = [
        ("TODAY",   f"{root}news/{today_str}/"),
        ("ARCHIVE", f"{root}#archive"),
        ("BRIEFINGS", f"{root}#archive"),
        ("SOURCES", f"{root}#about"),
        ("ABOUT",   f"{root}#about"),
    ]
    nav_html = "\n".join(
        f'      <a href="{href}">{label}</a>' for label, href in nav_items
    )
    return f"""<header class="masthead">
  <div class="container row">
    <a href="{root}" class="wordmark">
      <span class="dot-red"></span>VIGIL
    </a>
    <button class="nav-toggle" type="button" aria-label="メニュー"
            aria-expanded="false" aria-controls="main-nav">
      <span class="nav-toggle-bar"></span>
      <span class="nav-toggle-bar"></span>
      <span class="nav-toggle-bar"></span>
    </button>
    <nav class="main-nav" id="main-nav">
{nav_html}
    </nav>
    <a href="#" class="subscribe-btn">SUBSCRIBE · 07:15 DAILY →</a>
    <div class="meta">JST · 07:15 · {weekday}</div>
  </div>
</header>
<script>
(function(){{
  var btn=document.querySelector('.nav-toggle'),nav=document.getElementById('main-nav');
  if(!btn||!nav)return;
  function setOpen(o){{
    btn.setAttribute('aria-expanded',o?'true':'false');
    nav.classList.toggle('is-open',o);
  }}
  btn.addEventListener('click',function(){{setOpen(btn.getAttribute('aria-expanded')!=='true');}});
  nav.querySelectorAll('a').forEach(function(a){{a.addEventListener('click',function(){{setOpen(false);}});}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape')setOpen(false);}});
}})();
</script>"""


INTERACTIVE_JS = """
<div class="lightbox-overlay" id="lightbox">
  <button class="lightbox-close" id="lightbox-close">× CLOSE</button>
  <img src="" id="lightbox-img" alt="" />
</div>
<script>
(function(){
  /* --- Lightbox --- */
  var overlay = document.getElementById('lightbox');
  var img     = document.getElementById('lightbox-img');
  var close   = document.getElementById('lightbox-close');

  document.querySelectorAll('.zoom-image').forEach(function(el){
    el.addEventListener('click', function(){
      img.src = '';
      overlay.classList.add('is-open');
      setTimeout(function(){ img.src = el.dataset.src; img.alt = el.dataset.alt || ''; }, 20);
    });
  });
  function closeBox(){
    img.style.opacity = '0'; img.style.transform = 'scale(0.93)';
    setTimeout(function(){
      overlay.classList.remove('is-open');
      img.src = ''; img.style.opacity = ''; img.style.transform = '';
    }, 300);
  }
  close.addEventListener('click', closeBox);
  overlay.addEventListener('click', function(e){ if(e.target === overlay) closeBox(); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') closeBox(); });

  /* --- Scroll fade-in (.daily-topic) --- */
  var topics = document.querySelectorAll('.daily-topic');
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){ entry.target.classList.add('is-visible'); io.unobserve(entry.target); }
      });
    }, {threshold: 0.07, rootMargin: '0px 0px -32px 0px'});
    topics.forEach(function(el){ io.observe(el); });
  } else {
    topics.forEach(function(el){ el.classList.add('is-visible'); });
  }

  /* --- Dispatch ticker: seamless duplicate --- */
  var row = document.querySelector('.dispatch .row');
  if(row){ row.parentNode.appendChild(row.cloneNode(true)); }
})();
</script>
"""


# ── index page ───────────────────────────────────────────────

def build_index(all_dates: list[str], today_articles: list[dict], today_str: str) -> Path:
    """トップページを生成"""
    dt    = datetime.strptime(today_str, "%Y-%m-%d")
    issue = str(int(dt.strftime("%m%d"))).zfill(4)
    build = dt.strftime("%Y%m%d") + ".0715"
    weekday   = WEEKDAYS_EN[dt.weekday()]
    month_en  = MONTHS_EN[dt.month - 1]

    dispatch = _dispatch(issue, today_str, len(today_articles), build)
    masthead = _masthead("./", today_str, weekday)

    # ── ヒーロー統計 ──
    days_count    = len(all_dates)
    archive_count = days_count * len(today_articles) if days_count else len(today_articles)
    stats_html = f"""<div class="hero-stats">
  <div class="hero-stat">
    <div class="hero-stat-val">{len(today_articles):02d}</div>
    <div class="hero-stat-label">TODAY</div>
  </div>
  <div class="hero-stat">
    <div class="hero-stat-val">{days_count * 5}</div>
    <div class="hero-stat-label">BRIEFINGS / 30D</div>
  </div>
  <div class="hero-stat">
    <div class="hero-stat-val">{archive_count:,}</div>
    <div class="hero-stat-label">ARCHIVE</div>
  </div>
  <div class="hero-stat">
    <div class="hero-stat-val">{days_count * 8}</div>
    <div class="hero-stat-label">DELIVERED</div>
  </div>
</div>"""

    hero_html = f"""<section class="hero">
  <div class="container">
    <div class="hero-meta-line">
      <span>MORNING DISPATCH</span>
      <span class="sep">//</span>
      <span>{weekday}, {month_en} {dt.day}, {dt.year}</span>
      <span class="sep">//</span>
      <span>ISSUE N°{issue}</span>
      <span class="sep">//</span>
      <span>CURATED BY VIGIL · AI MORNING INTELLIGENCE</span>
    </div>
    <div class="hero-title-wrap">
      <h1>VIGIL</h1>
      <div class="hero-issue">N°{issue}</div>
    </div>
    <hr class="hero-divider" />
    <div class="hero-tagline">
      AI業界で<em>昨夜起きたこと</em>を、毎朝<em>07:15 JST</em>に。
      ニュース・モデル発表・論文・注目のスレッドを、朝刊として一枚に。
    </div>
    {stats_html}
  </div>
</section>"""

    # ── 今日の記事カードグリッド ──
    img_dir  = SITE_DIR / "assets" / "images" / today_str
    cards_html = _build_card_grid(today_articles, today_str, img_dir, root="./")

    # ── アーカイブ ──
    archive_html = ""
    for d in sorted(all_dates, reverse=True)[:30]:
        dd = datetime.strptime(d, "%Y-%m-%d")
        archive_html += (
            f'    <a href="./news/{d}/" class="archive-card">\n'
            f'      <div class="d">{d}</div>\n'
            f'      <div class="n">{WEEKDAYS_EN[dd.weekday()]} · MORNING DISPATCH</div>\n'
            f'    </a>\n'
        )

    html = _head(
        "VIGIL — AI Morning Intelligence",
        "山中秀斗が毎朝整理するAI業界のモーニングディスパッチ。",
        "./assets/style.css",
    ) + f"""
{dispatch}
{masthead}

{hero_html}

<section class="section" id="today">
  <div class="container">
    <div class="section-head">
      <div class="section-label">
        <span class="num">§01</span>
        <h2>Today · Dispatch<span class="sub">今朝の配信</span></h2>
      </div>
      <a href="./news/{today_str}/" class="section-link">ALL {len(today_articles)} ITEMS →</a>
    </div>
  </div>
  {cards_html}
</section>

<section class="section" id="archive">
  <div class="container">
    <div class="section-head">
      <div class="section-label">
        <span class="num">§02</span>
        <h2>Archive<span class="sub">過去のディスパッチ</span></h2>
      </div>
    </div>
    <div class="archive-grid">
{archive_html}    </div>
  </div>
</section>

<section class="section" id="about">
  <div class="container">
    <div class="section-head">
      <div class="section-label">
        <span class="num">§03</span>
        <h2>About<span class="sub">VIGILについて</span></h2>
      </div>
    </div>
    <p style="max-width:600px;color:var(--ink-soft);line-height:1.8;">
      毎朝07:15 JSTにAIエージェントが自律起動し、RSS・ニュースソースを収集・要約・スライド化してGitHub Pagesに自動配信。
      人間の介入ほぼゼロで動くモーニングディスパッチです。
    </p>
    <p style="margin-top:16px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:var(--mute);">
      PIPELINE: RSS → CLAUDE HAIKU → GEMINI SLIDES → GITHUB PAGES
    </p>
  </div>
</section>

<footer>
  <div class="container row">
    <span class="brand">VIGIL</span>
    <span>AI Morning Intelligence — 山中秀斗 / TREPRO</span>
    <span>{today_str}</span>
  </div>
</footer>
{INTERACTIVE_JS}
</body>
</html>"""

    out_path = SITE_DIR / "index.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


# ── daily page ───────────────────────────────────────────────

def build_daily_page(date_str: str, articles: list[dict], issue_num: int = None) -> Path:
    """日付別詳細ページ"""
    dt         = datetime.strptime(date_str, "%Y-%m-%d")
    issue      = str(issue_num or int(dt.strftime("%m%d"))).zfill(4)
    build      = dt.strftime("%Y%m%d") + ".0715"
    today_str  = dt.strftime("%Y-%m-%d")
    weekday    = WEEKDAYS_EN[dt.weekday()]
    month_en   = MONTHS_EN[dt.month - 1]

    out_dir = SITE_DIR / "news" / date_str
    out_dir.mkdir(parents=True, exist_ok=True)
    img_dir = SITE_DIR / "assets" / "images" / date_str
    img_dir.mkdir(parents=True, exist_ok=True)

    dispatch = _dispatch(issue, today_str, len(articles), build)
    masthead = _masthead("../../", today_str, weekday)

    # ── 記事カード（detail） ──
    topics_html = ""
    for i, a in enumerate(articles, 1):
        slide_rel   = f"../../assets/images/{date_str}/topic_{i}.png"
        slide_exists = (img_dir / f"topic_{i}.png").exists()

        slide_html = ""
        if slide_exists:
            slide_html = (
                f'      <div class="slide-img zoom-image" '
                f'data-src="{slide_rel}" data-alt="{a["title"]}" '
                f'role="button" tabindex="0">\n'
                f'        <img src="{slide_rel}" alt="{a["title"]}" loading="lazy" />\n'
                f'      </div>'
            )

        kp_html = "\n".join(
            f'        <li data-i="{str(j).zfill(2)}">{kp}</li>'
            for j, kp in enumerate(a.get("keypoints", [])[:5], 1)
        )
        links_html = "\n".join(
            f'        <dd><a href="{lnk}">{lnk[:55]}…</a></dd>' if len(lnk) > 55
            else f'        <dd><a href="{lnk}">{lnk}</a></dd>'
            for lnk in a.get("links", [])[:3]
        )
        likes = a.get("likes", "")
        likes_html = (
            f'        <dt>ENGAGEMENT</dt>\n'
            f'        <dd><span class="likes">{likes:,}</span>'
            f'<div class="likes-label">likes on X</div></dd>'
        ) if likes else ""

        topics_html += f"""
<article class="daily-topic" id="topic-{i}">
  <div class="container">
    <aside class="numeral">{str(i).zfill(2)}<span class="ord">TOPIC {str(i).zfill(2)} · {a.get('source','').upper()}</span></aside>
    <div class="main">
      <div class="cat-line">
        {a.get('category','AI情報')} <span class="sep">/</span> {a.get('source','')} <span class="sep">/</span> NEWS
      </div>
      <h2>{a['title']}</h2>
{slide_html}
      <p class="lede">{a.get('lede','')}</p>
      <h3>キーポイント</h3>
      <ul class="keypoints">
{kp_html}
      </ul>
      <div class="pull">{a.get('pull','')}</div>
    </div>
    <aside class="side">
      <dl>
{likes_html}
        <dt>SOURCE</dt>
        <dd>{a.get('source','')}</dd>
        <dt>PUBLISHED</dt>
        <dd>{date_str}</dd>
        <dt>CATEGORY</dt>
        <dd>{a.get('category','')}</dd>
        <dt>LINKS</dt>
{links_html}
      </dl>
    </aside>
  </div>
</article>"""

    html = _head(
        f"{date_str} Morning Dispatch — VIGIL",
        f"{date_str} の VIGIL モーニングディスパッチ — {len(articles)}本のAI業界ニュース。",
        "../../assets/style.css",
    ) + f"""
{dispatch}
{masthead}

<section class="daily-head">
  <div class="container">
    <div class="hero-meta-line">
      MORNING DISPATCH
      <span class="sep">//</span> {weekday} · {month_en} {dt.day}, {dt.year}
    </div>
    <h1 class="date-huge">{dt.year}<span class="dot">.</span>{dt.strftime('%m')}<span class="dot">.</span>{dt.strftime('%d')}</h1>
    <div class="strap">
      <span><span class="count">{len(articles):02d}</span>&nbsp;ITEMS</span>
      <span>AI MORNING INTELLIGENCE</span>
    </div>
  </div>
</section>

{topics_html}

<footer>
  <div class="container row">
    <span class="brand">VIGIL</span>
    <span>AI Morning Intelligence — 山中秀斗 / TREPRO</span>
    <span>{date_str} DISPATCH</span>
  </div>
</footer>
{INTERACTIVE_JS}
</body>
</html>"""

    out_path = out_dir / "index.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


# ── カードグリッド共通ビルダー ────────────────────────────────

def _build_card_grid(articles: list[dict], date_str: str, img_dir: Path, root: str = "../../") -> str:
    """インデックス用カードグリッドを生成"""
    if not articles:
        return ""

    img_root = f"{root}assets/images/{date_str}"
    cards = []

    for i, a in enumerate(articles, 1):
        slide_rel    = f"{img_root}/topic_{i}.png"
        slide_exists = (img_dir / f"topic_{i}.png").exists()
        detail_url   = f"{root}news/{date_str}/#topic-{i}"
        likes        = a.get("likes", 0)
        category     = a.get("category", "AI情報")
        source       = a.get("source", "")
        title        = a["title"]
        lede         = a.get("lede", "")
        keypoints    = a.get("keypoints", [])[:3]
        impr         = a.get("impressions", 0)

        # カテゴリバッジ
        badge_html = f'<span class="badge badge-cat">{category}</span>'
        date_badge = f'<span class="badge badge-date">{date_str}</span>'
        src_html   = f'<span class="src-chips">{source}</span>' if source else ""
        meta_html  = f'<div class="card-meta">{badge_html}{date_badge}{src_html}</div>'

        # キーポイント
        kp_html = "".join(
            f'<li>{kp}</li>' for kp in keypoints
        ) if keypoints else ""
        kp_block = f'<ul class="card-points">{kp_html}</ul>' if kp_html else ""

        # 統計フッター
        likes_str = f"{likes:,}" if likes else "—"
        impr_str  = f"{impr/1_000_000:.1f}M" if impr >= 1_000_000 else (f"{impr/1000:.0f}K" if impr >= 1000 else "—")
        foot_html = (
            f'<div class="card-foot">'
            f'<div class="card-stats">'
            f'<span>♥ <span class="card-stat-val card-stat-likes">{likes_str}</span></span>'
            + (f'<span>SHR <span class="card-stat-val">{impr_str}</span></span>' if impr else "")
            + f'</div>'
            f'<a href="{detail_url}" class="card-read">READ →</a>'
            f'</div>'
        )

        # 1枚目はトップストーリー（横長レイアウト）
        if i == 1:
            img_html = ""
            if slide_exists:
                img_html = (
                    f'<div class="card-img zoom-image" data-src="{slide_rel}" '
                    f'data-alt="{title}" role="button" tabindex="0">\n'
                    f'  <img src="{slide_rel}" alt="{title}" loading="lazy" />\n'
                    f'  <div class="card-img-cap">FIG 01 · {title[:40]}{"…" if len(title)>40 else ""}</div>\n'
                    f'</div>'
                )
            top_card = (
                f'<div class="card-top">\n'
                f'  <div>\n'
                f'    <div class="card-num-wrap">'
                f'      <div class="card-num">01</div>'
                f'      <div class="card-num-label">TOP STORY</div>'
                f'    </div>\n'
                f'    {meta_html}\n'
                f'    <h2>{title}</h2>\n'
                f'    <p class="card-lede">{lede}</p>\n'
                f'    {kp_block}\n'
                f'    {foot_html}\n'
                f'  </div>\n'
                f'  {img_html}\n'
                f'</div>'
            )
            cards.append(("top", top_card))
        else:
            img_html = ""
            if slide_exists:
                img_html = (
                    f'<div class="card-img zoom-image" data-src="{slide_rel}" '
                    f'data-alt="{title}" role="button" tabindex="0">\n'
                    f'  <img src="{slide_rel}" alt="{title}" loading="lazy" />\n'
                    f'</div>'
                )
            card = (
                f'<div class="card">\n'
                f'  <div class="card-num">{str(i).zfill(2)}</div>\n'
                f'  {meta_html}\n'
                f'  <h2>{title}</h2>\n'
                f'  {img_html}\n'
                f'  <p class="card-lede">{lede}</p>\n'
                f'  {kp_block}\n'
                f'  {foot_html}\n'
                f'</div>'
            )
            cards.append(("normal", card))

    # グリッド組み立て：1枚目は全幅、残りは3列
    html = ""
    if cards:
        top_type, top_html = cards[0]
        html += f'<div class="dispatch-grid cols-1">\n{top_html}\n</div>\n'

    remaining = cards[1:]
    if remaining:
        html += '<div class="dispatch-grid cols-3">\n'
        html += "\n".join(c for _, c in remaining)
        html += "\n</div>\n"

    return html


# ── CLI テスト ────────────────────────────────────────────────

if __name__ == "__main__":
    test_articles = [
        {
            "title": "ChatGPT Images 2.0 発表 — 文字・UIが崩れない「thinking-level」画像モデル",
            "category": "新モデル発表",
            "source": "@OpenAI",
            "lede": "OpenAIが新世代画像生成モデル「ChatGPT Images 2.0」（内部コード名 telepathy）を正式発表。最大2K解像度で、細かい文字・UI要素・複雑なレイアウトを崩さずに描画できる推論型モデル。",
            "keypoints": [
                "最大2K解像度・文字・UI・密度の高い構図でも破綻しにくい",
                "\"thinking\"（推論）で指示追従性が大幅向上",
                "ChatGPT（Proプラン$200含む）で即日利用可能",
            ],
            "pull": "Sam Altmanは「OpenAI過去最高のリリース」と評価。",
            "links": ["https://openai.com/index/chatgpt-images-2"],
            "likes": 21440,
            "impressions": 4200000,
        },
        {
            "title": "OpenAI Codex、MAU 4M突破+レート上限リセット",
            "category": "ツール更新",
            "source": "@sama",
            "lede": "Codexでタスクを中断していた人は、今週もう一度踏み込めるタイミング。受講生向けには「今週はCodexを使い倒すチャンス」として伝えられるタイムセンシティブ情報。",
            "keypoints": ["レート上限全アカウント一斉リセット", "MAU 4M突破、長時間エージェント運用が定着"],
            "pull": "MAU急増の背景にはChronicleメモリ・Mac連携・Computer Useなどの大型アップデート。",
            "links": ["https://openai.com/codex"],
            "likes": 23499,
            "impressions": 412000,
        },
        {
            "title": "Cursor × SpaceX 提携 — Composerを「現実の難コード」で強化",
            "category": "業界動向",
            "source": "@cursor_ai",
            "lede": "Cursor Composerの完成度が上がると従量課金を回避しつつ高速という選択肢が現実になる。コスト重視派には中期的に重要な材料。",
            "keypoints": ["Composerモデルを実運用コードで再訓練", "従来APIコスト回避の現実解に"],
            "pull": "実際のSpaceXコードベースで訓練することで、エッジケースへの対応力が向上。",
            "links": ["https://cursor.com"],
            "likes": 11483,
            "impressions": 318000,
        },
    ]
    today = "2026-04-24"
    p1 = build_daily_page(today, test_articles)
    print(f"生成: {p1}")
    p2 = build_index([today], test_articles, today)
    print(f"生成: {p2}")
