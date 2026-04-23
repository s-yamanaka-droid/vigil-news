"""
VIGIL — HTML Builder
ニュースデータからVCBスタイルのHTMLを生成する
"""
from datetime import datetime
from pathlib import Path
import json

SITE_DIR = Path(__file__).parent.parent / "site"
FONTS = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap"

NAV_LINKS = """
      <a href="{root}">HOME</a>
      <a href="{root}news/{today}/">TODAY</a>
      <a href="{root}#archive">ARCHIVE</a>
      <a href="{root}#about">ABOUT</a>
"""

DISPATCH_BAR = """<div class="dispatch">
  <div class="container row">
    <span class="tick">VIGIL №{issue}</span>
    <span class="sep">/</span>
    <span>{date}</span>
    <span class="sep">/</span>
    <span>MORNING EDITION</span>
    <span class="sep">/</span>
    <span>{count} ITEMS</span>
    <span class="sep">/</span>
    <span>BUILD {build}</span>
    <span class="sep">/</span>
    <span class="live">LIVE</span>
    <span class="sep">/</span>
    <span>CURATED BY 山中秀斗</span>
  </div>
</div>"""

MASTHEAD = """<header class="masthead">
  <div class="container row">
    <a href="{root}" class="wordmark"><span class="bar"></span>VIGIL</a>
    <button class="nav-toggle" type="button" aria-label="メニュー" aria-expanded="false" aria-controls="main-nav">
      <span class="nav-toggle-bar"></span><span class="nav-toggle-bar"></span><span class="nav-toggle-bar"></span>
    </button>
    <nav class="main-nav" id="main-nav">{nav}</nav>
    <div class="meta">JST · {time} · {weekday}</div>
  </div>
</header>
<script>
(function(){{
  var btn=document.querySelector('.nav-toggle'),nav=document.getElementById('main-nav');
  if(!btn||!nav)return;
  function setOpen(o){{btn.setAttribute('aria-expanded',o?'true':'false');nav.classList.toggle('is-open',o);}}
  btn.addEventListener('click',function(){{setOpen(btn.getAttribute('aria-expanded')!=='true');}});
  nav.querySelectorAll('a').forEach(function(a){{a.addEventListener('click',function(){{setOpen(false);}});}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape')setOpen(false);}});
}})();
</script>"""

LIGHTBOX_JS = """
<div class="lightbox-overlay" id="lightbox">
  <button class="lightbox-close" id="lightbox-close">× CLOSE</button>
  <img src="" id="lightbox-img" alt="" />
</div>
<script>
(function(){
  var overlay=document.getElementById('lightbox');
  var img=document.getElementById('lightbox-img');
  var close=document.getElementById('lightbox-close');
  document.querySelectorAll('.zoom-image').forEach(function(el){
    el.addEventListener('click',function(){
      img.src=el.dataset.src; img.alt=el.dataset.alt||'';
      overlay.classList.add('is-open');
    });
  });
  function closeBox(){overlay.classList.remove('is-open');img.src='';}
  close.addEventListener('click',closeBox);
  overlay.addEventListener('click',function(e){if(e.target===overlay)closeBox();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closeBox();});
})();
</script>
"""

WEEKDAYS_EN = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
MONTHS_EN = ["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE","JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"]

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


def build_daily_page(date_str: str, articles: list[dict], issue_num: int = None) -> Path:
    """
    日付別ニュースページを生成
    articles: [{ title, category, source, lede, keypoints, pull, links, slide_path, likes }, ...]
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    issue = issue_num or int(dt.strftime("%m%d"))
    build = dt.strftime("%Y%m%d") + ".0715"
    today_str = dt.strftime("%Y-%m-%d")
    weekday = WEEKDAYS_EN[dt.weekday()]
    month_en = MONTHS_EN[dt.month - 1]
    time_str = "07:15"

    out_dir = SITE_DIR / "news" / date_str
    out_dir.mkdir(parents=True, exist_ok=True)
    img_dir = SITE_DIR / "assets" / "images" / date_str
    img_dir.mkdir(parents=True, exist_ok=True)

    nav = NAV_LINKS.format(root="../../", today=today_str)
    dispatch = DISPATCH_BAR.format(issue=str(issue).zfill(4), date=today_str,
                                   count=len(articles), build=build)
    masthead = MASTHEAD.format(root="../../", nav=nav, time=time_str, weekday=weekday)

    # 記事カード生成
    topics_html = ""
    for i, a in enumerate(articles, 1):
        slide_rel = f"../../assets/images/{date_str}/topic_{i}.png"
        slide_exists = (img_dir / f"topic_{i}.png").exists()

        slide_html = ""
        if slide_exists:
            slide_html = f"""      <div class="slide-img zoom-image" data-src="{slide_rel}" data-alt="{a['title']}" role="button" tabindex="0">
        <img src="{slide_rel}" alt="{a['title']}" loading="lazy" />
      </div>"""

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
        likes_html = f"""        <dt>ENGAGEMENT</dt>
        <dd><span class="likes">{likes:,}</span><div class="likes-label">likes on X</div></dd>""" if likes else ""

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
    <div style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:0.18em;text-transform:uppercase;color:var(--accent);margin-bottom:20px;">
      MORNING DISPATCH · {weekday} · {month_en} {dt.day}, {dt.year}
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
{LIGHTBOX_JS}
</body>
</html>"""

    out_path = out_dir / "index.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


def build_index(all_dates: list[str], today_articles: list[dict], today_str: str) -> Path:
    """トップページを生成"""
    dt_today = datetime.strptime(today_str, "%Y-%m-%d")
    issue = int(dt_today.strftime("%m%d"))
    build = dt_today.strftime("%Y%m%d") + ".0715"
    weekday = WEEKDAYS_EN[dt_today.weekday()]
    time_str = "07:15"

    nav = NAV_LINKS.format(root="./", today=today_str)
    dispatch = DISPATCH_BAR.format(issue=str(issue).zfill(4), date=today_str,
                                   count=len(today_articles), build=build)
    masthead = MASTHEAD.format(root="./", nav=nav, time=time_str, weekday=weekday)

    # アーカイブカード
    archive_html = ""
    for d in sorted(all_dates, reverse=True)[:30]:
        dt = datetime.strptime(d, "%Y-%m-%d")
        archive_html += f"""    <a href="./news/{d}/" class="archive-card">
      <div class="d">{d}</div>
      <div class="n">{WEEKDAYS_EN[dt.weekday()]} · MORNING DISPATCH</div>
    </a>\n"""

    hero_topics = " · ".join(a["title"][:30] + "…" for a in today_articles[:3])

    html = _head(
        "VIGIL — AI Morning Intelligence",
        "山中秀斗が毎朝整理するAI業界のモーニングディスパッチ。",
        "./assets/style.css",
    ) + f"""
{dispatch}
{masthead}

<section class="hero">
  <div class="container">
    <div class="grid">
      <div>
        <div class="eyebrow">MORNING DISPATCH <span class="dot">·</span> {today_str} <span class="dot">·</span> ISSUE N°{str(issue).zfill(4)}</div>
        <h1>VIGIL<br><span style="font-size:0.45em;letter-spacing:0.08em;color:var(--mute);">AI INTELLIGENCE</span></h1>
      </div>
      <aside class="aside">
        <p>山中秀斗が毎朝整理する AI 業界のモーニングディスパッチ。</p>
        <p>ニュース・ツール・論文・良質な情報を、朝刊として一枚に。</p>
      </aside>
    </div>
    <div class="hero-strap">
      <span><span class="k">{len(today_articles):02d}</span>TODAY</span>
      <span><span class="k">{len(all_dates)}</span>DAYS</span>
      <span>SINCE {min(all_dates) if all_dates else today_str}</span>
      <span>07:15 JST DAILY</span>
    </div>
  </div>
</section>

<section class="section" id="today">
  <div class="container">
    <div class="section-head">
      <div class="title">
        <span class="en">§01 · Today's Dispatch</span>
        <h2>本日のAIニュース</h2>
      </div>
      <a href="./news/{today_str}/" style="font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.1em;text-transform:uppercase;color:var(--accent);">ALL {len(today_articles)} ITEMS →</a>
    </div>
  </div>
</section>

<section class="section" id="archive">
  <div class="container">
    <div class="section-head">
      <div class="title">
        <span class="en">§02 · Archive</span>
        <h2>過去のディスパッチ</h2>
      </div>
    </div>
    <div class="archive-grid">
{archive_html}    </div>
  </div>
</section>

<section class="section" id="about">
  <div class="container">
    <div class="section-head">
      <div class="title">
        <span class="en">§03 · About</span>
        <h2>VIGILについて</h2>
      </div>
    </div>
    <p style="max-width:640px;color:var(--ink-soft);">毎朝07:15 JSTにAIエージェントが自律起動し、RSS・ニュースソースを収集・要約・スライド化してGitHub Pagesに自動配信。人間の介入ほぼゼロで動くモーニングディスパッチです。</p>
    <p style="margin-top:16px;font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:0.1em;text-transform:uppercase;color:var(--mute);">PIPELINE: RSS → CLAUDE HAIKU → GEMINI SLIDES → GITHUB PAGES</p>
  </div>
</section>

<footer>
  <div class="container row">
    <span class="brand">VIGIL</span>
    <span>AI Morning Intelligence — 山中秀斗 / TREPRO</span>
    <span>{today_str}</span>
  </div>
</footer>
{LIGHTBOX_JS}
</body>
</html>"""

    out_path = SITE_DIR / "index.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    test_articles = [
        {
            "title": "OpenAI Codex MAU 400万人突破",
            "category": "ツール更新",
            "source": "OpenAI Blog",
            "lede": "CodexのMAUが400万人に到達。わずか2週間で100万人増。",
            "keypoints": ["MAU 400万人到達", "2週間で3M→4M", "レートリミット即日緩和"],
            "pull": "利用急増の背景にはChronicleメモリ・Mac連携・Computer Useなどの大型アップデート。",
            "links": ["https://openai.com/codex"],
            "likes": 23499,
        },
    ]
    p = build_daily_page("2026-04-22", test_articles)
    print(f"生成: {p}")
    p2 = build_index(["2026-04-22"], test_articles, "2026-04-22")
    print(f"生成: {p2}")
