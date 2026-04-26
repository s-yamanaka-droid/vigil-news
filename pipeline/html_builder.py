"""
VIGIL — HTML Builder v4
vigil.css (Claude Design) の DOM 構造に完全準拠
"""
from datetime import datetime
from pathlib import Path
import json

SITE_DIR = Path(__file__).parent.parent / "docs"

WEEKDAYS_EN = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
WEEKDAYS_LONG = ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]
MONTHS_EN = ["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE",
             "JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"]

# vigil.css が要求するフォント
FONTS_VIGIL = (
    "https://fonts.googleapis.com/css2?"
    "family=JetBrains+Mono:wght@400;500;600;700;800&"
    "family=Noto+Sans+JP:wght@400;500;700&"
    "family=Noto+Serif+JP:wght@400;600;700&display=swap"
)
# detail ページ用フォント（Barlow Condensed も維持）
FONTS_DETAIL = (
    "https://fonts.googleapis.com/css2?"
    "family=Barlow+Condensed:wght@600;700;800;900&"
    "family=JetBrains+Mono:wght@400;500;600;700;800&"
    "family=Noto+Sans+JP:wght@400;500;700&"
    "family=Noto+Serif+JP:wght@400;600;700&display=swap"
)

INTERACTIVE_JS = """
<!-- Article Modal -->
<div id="article-modal" style="display:none;position:fixed;inset:0;z-index:2000;background:rgba(14,13,11,0);transition:background .3s;pointer-events:none;">
  <div id="modal-box" style="position:absolute;top:50%;left:50%;transform:translate(-50%,-48%) scale(.97);opacity:0;transition:transform .3s,opacity .3s;background:var(--paper);border:1px solid var(--rule-2);max-width:700px;width:calc(100% - 48px);max-height:88vh;overflow-y:auto;padding:0;">
    <div style="display:flex;align-items:center;justify-content:space-between;padding:16px 24px;border-bottom:1px solid var(--rule);position:sticky;top:0;background:var(--paper);z-index:1;">
      <span id="modal-cat" style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--red)"></span>
      <button id="modal-close" style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.1em;background:none;border:1px solid var(--rule-2);padding:5px 12px;cursor:pointer;color:var(--ink);transition:background .2s,color .2s;">✕ CLOSE</button>
    </div>
    <div style="padding:28px 32px 32px;">
      <h2 id="modal-title" style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:22px;line-height:1.35;margin:0 0 16px;"></h2>
      <p id="modal-lede" style="font-family:'Noto Serif JP',serif;font-size:15px;line-height:1.8;color:var(--ink-2);margin:0 0 22px;"></p>
      <div id="modal-kp" style="margin:0 0 22px;"></div>
      <div id="modal-pull" style="padding:14px 18px;border-left:3px solid var(--red);background:var(--paper-2);font-size:13px;line-height:1.7;color:var(--ink-2);font-style:italic;margin-bottom:24px;display:none;"></div>
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
        <span id="modal-src" style="font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--mute);letter-spacing:.08em;"></span>
        <a id="modal-link" href="#" style="font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.1em;color:var(--paper);background:var(--ink);padding:9px 20px;text-decoration:none;transition:background .2s;">FULL ARTICLE →</a>
      </div>
    </div>
  </div>
</div>

<!-- Image Lightbox -->
<div class="lightbox-overlay" id="lightbox">
  <button class="lightbox-close" id="lightbox-close">× CLOSE</button>
  <img src="" id="lightbox-img" alt="" />
</div>

<script>
(function(){
  /* ── modal ── */
  var modal=document.getElementById('article-modal');
  var box=document.getElementById('modal-box');
  var mclose=document.getElementById('modal-close');

  function openModal(card){
    var d=card.dataset;
    document.getElementById('modal-cat').textContent=d.category||'';
    document.getElementById('modal-title').textContent=d.title||'';
    document.getElementById('modal-lede').textContent=d.lede||'';
    document.getElementById('modal-src').textContent=d.source||'';
    var linkEl=document.getElementById('modal-link');
    linkEl.href=d.link||'#';

    /* keypoints */
    var kpEl=document.getElementById('modal-kp');
    kpEl.innerHTML='';
    try{
      var kps=JSON.parse(d.keypoints||'[]');
      if(kps.length){
        var ul=document.createElement('ul');
        ul.style.cssText='list-style:none;padding:0;margin:0;';
        kps.forEach(function(kp,i){
          var li=document.createElement('li');
          li.style.cssText='padding:9px 12px 9px 38px;margin-bottom:2px;background:var(--paper-2);position:relative;font-size:13px;line-height:1.6;border-left:2px solid transparent;transition:border-color .15s;';
          li.onmouseenter=function(){this.style.borderLeftColor='var(--red)';}; li.onmouseleave=function(){this.style.borderLeftColor='transparent';};
          var num=document.createElement('span');
          num.style.cssText='position:absolute;left:12px;top:9px;font-family:JetBrains Mono,monospace;font-size:10px;color:var(--red);';
          num.textContent=String(i+1).padStart(2,'0');
          li.appendChild(num); li.appendChild(document.createTextNode(kp));
          ul.appendChild(li);
        });
        kpEl.appendChild(ul);
      }
    }catch(e){}

    /* pull */
    var pullEl=document.getElementById('modal-pull');
    if(d.pull){pullEl.textContent=d.pull;pullEl.style.display='block';}
    else{pullEl.style.display='none';}

    modal.style.display='flex'; modal.style.alignItems='center'; modal.style.justifyContent='center';
    modal.style.pointerEvents='auto';
    requestAnimationFrame(function(){
      modal.style.background='rgba(14,13,11,.88)';
      box.style.opacity='1'; box.style.transform='translate(-50%,-50%) scale(1)';
    });
    document.body.style.overflow='hidden';
  }

  function closeModal(){
    modal.style.background='rgba(14,13,11,0)';
    box.style.opacity='0'; box.style.transform='translate(-50%,-48%) scale(.97)';
    setTimeout(function(){modal.style.display='none';modal.style.pointerEvents='none';},300);
    document.body.style.overflow='';
  }

  mclose.addEventListener('click',closeModal);
  modal.addEventListener('click',function(e){if(e.target===modal)closeModal();});
  document.getElementById('modal-close').onmouseover=function(){this.style.background='var(--red)';this.style.color='#fff';this.style.borderColor='var(--red)';};
  document.getElementById('modal-close').onmouseout=function(){this.style.background='';this.style.color='var(--ink)';this.style.borderColor='var(--rule-2)';};

  /* tcard click → modal */
  document.querySelectorAll('.tcard[data-title]').forEach(function(card){
    card.style.cursor='pointer';
    card.addEventListener('click',function(e){
      if(e.target.tagName==='A')return;
      openModal(card);
    });
  });

  /* ── category filter ── */
  document.querySelectorAll('.filter-pill').forEach(function(pill){
    pill.addEventListener('click',function(){
      var cat=pill.dataset.cat;
      document.querySelectorAll('.filter-pill').forEach(function(p){p.classList.remove('active');});
      pill.classList.add('active');
      document.querySelectorAll('.tcard').forEach(function(c){
        if(!cat||c.dataset.category===cat||cat==='ALL'){
          c.style.opacity='1'; c.style.pointerEvents=''; c.style.transform='';
        } else {
          c.style.opacity='.2'; c.style.pointerEvents='none'; c.style.transform='scale(.97)';
        }
      });
    });
  });

  /* ── image lightbox ── */
  var overlay=document.getElementById('lightbox');
  var img=document.getElementById('lightbox-img');
  var close=document.getElementById('lightbox-close');
  document.querySelectorAll('.zoom-image').forEach(function(el){
    el.addEventListener('click',function(e){e.stopPropagation();
      img.src=''; overlay.classList.add('is-open');
      setTimeout(function(){ img.src=el.dataset.src; img.alt=el.dataset.alt||''; },20);
    });
  });
  function closeBox(){
    img.style.opacity='0'; img.style.transform='scale(0.93)';
    setTimeout(function(){ overlay.classList.remove('is-open'); img.src=''; img.style.opacity=''; img.style.transform=''; },300);
  }
  close.addEventListener('click',closeBox);
  overlay.addEventListener('click',function(e){if(e.target===overlay)closeBox();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){closeBox();closeModal();}});

  /* ── scroll fade-in: both .daily-topic and .tcard ── */
  var fadeEls=document.querySelectorAll('.daily-topic, .tcard');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-visible');io.unobserve(e.target);}});
    },{threshold:0.05,rootMargin:'0px 0px -24px 0px'});
    fadeEls.forEach(function(el){io.observe(el);});
  } else { fadeEls.forEach(function(el){el.classList.add('is-visible');}); }

  /* ── dispatch ticker ── */
  var row=document.querySelector('.dispatch');
  if(row && row.dataset.ticker!=='off'){
    var inner=row.innerHTML; row.innerHTML=inner+inner;
    var pos=0,spd=0.4;
    (function tick(){pos+=spd;if(pos>=row.scrollWidth/2)pos=0;row.scrollLeft=pos;requestAnimationFrame(tick);})();
  }
})();
</script>
"""


def _head(title, desc, css_path, fonts):
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{fonts}" rel="stylesheet">
<link rel="stylesheet" href="{css_path}" />
</head>
<body>"""


# ── INDEX PAGE ───────────────────────────────────────────────

def build_index(all_dates: list[str], today_articles: list[dict], today_str: str) -> Path:
    dt       = datetime.strptime(today_str, "%Y-%m-%d")
    issue    = str(int(dt.strftime("%m%d"))).zfill(4)
    weekday  = WEEKDAYS_EN[dt.weekday()]
    weekday_long = WEEKDAYS_LONG[dt.weekday()]
    month_en = MONTHS_EN[dt.month - 1]
    img_dir  = SITE_DIR / "assets" / "images" / today_str

    # ── dispatch bar ──
    dispatch = f"""<div class="dispatch" data-ticker="on">
  <span class="tick">VIGIL</span>
  <span class="sep">/</span>
  <span>№{issue}</span>
  <span class="sep">/</span>
  <span>{today_str}</span>
  <span class="sep">/</span>
  <span>MORNING EDITION</span>
  <span class="sep">/</span>
  <span>{len(today_articles)} ITEMS</span>
  <span class="sep">/</span>
  <span class="live"><span class="dot"></span>LIVE</span>
  <span class="sep">/</span>
  <span>CURATED BY 山中秀斗</span>
  <div class="right">
    <span class="jst"><b>07:15</b> JST</span>
    <span>{weekday}</span>
  </div>
</div>"""

    # ── nav ──
    nav = f"""<nav class="main">
  <div class="brand"><em>●</em>VIGIL</div>
  <ul>
    <li><a href="./" class="active">TODAY</a></li>
    <li><a href="#archive">ARCHIVE</a></li>
    <li><a href="#briefings">BRIEFINGS</a></li>
    <li><a href="#about">SOURCES</a></li>
    <li><a href="#about">ABOUT</a></li>
  </ul>
  <button class="subscribe" onclick="return false">SUBSCRIBE · 07:15 DAILY →</button>
</nav>"""

    # ── hero ──
    top = today_articles[0] if today_articles else {}
    top_title = top.get("title", "")
    top_lede  = top.get("lede", "")[:80] + "…" if len(top.get("lede","")) > 80 else top.get("lede","")

    unique_sources = len(set(a.get("source","") for a in today_articles))
    days_count = len(all_dates)

    hero = f"""<div class="hero-wrap">
  <div class="edition-line">
    <span>MORNING DISPATCH</span>
    <span class="sep">//</span>
    <span>{weekday_long}, {month_en} {dt.day}, {dt.year}</span>
    <span class="sep">//</span>
    <span>ISSUE N°{issue}</span>
    <span class="sep">//</span>
    <span>CURATED BY VIGIL · AI MORNING INTELLIGENCE</span>
  </div>
  <div class="hero">
    <div class="logo-block">
      <h1>VIGIL<span class="dot">.</span></h1>
      <div class="sub"><b>AI MORNING INTELLIGENCE</b> · DAILY DISPATCH</div>
      <div class="tagline">
        AI業界で<b>昨夜起きたこと</b>を、毎朝<b>07:15 JST</b>に。<br>
        ニュース・モデル発表・論文・注目のスレッドを、朝刊として一枚に。
      </div>
    </div>
    <a href="./news/{today_str}/" class="today-cta">
      <div class="ctop">
        <span>TODAY'S ISSUE</span>
        <b>● LIVE</b>
      </div>
      <h2>{dt.strftime('%m%d')}<span class="issue">MORNING EDITION · N°{issue}</span></h2>
      <div class="headline">{top_lede}</div>
      <span class="gotoday">READ TODAY'S DISPATCH →</span>
      <div class="meta-grid">
        <div><div class="k">ITEMS</div><div class="v"><em>{len(today_articles):02d}</em></div></div>
        <div><div class="k">SOURCES</div><div class="v">{unique_sources}</div></div>
        <div><div class="k">ARCHIVE</div><div class="v">{days_count}</div></div>
      </div>
    </a>
  </div>
</div>"""

    # ── stats row ──
    archive_total = sum(
        len(json.loads((SITE_DIR / "news" / d / "articles.json").read_text(encoding="utf-8")))
        if (SITE_DIR / "news" / d / "articles.json").exists() else 8
        for d in all_dates
    )
    stats = f"""<div style="max-width:1400px;margin:0 auto;padding:0 40px">
  <div class="stats-row">
    <div class="stat">
      <div class="k">TODAY</div>
      <div class="v">{len(today_articles):02d}</div>
      <div class="n">items in this issue</div>
    </div>
    <div class="stat">
      <div class="k">SOURCES</div>
      <div class="v">{unique_sources}</div>
      <div class="n">feeds monitored</div>
    </div>
    <div class="stat">
      <div class="k">ARCHIVE</div>
      <div class="v">{archive_total}</div>
      <div class="n">total articles</div>
    </div>
    <div class="stat">
      <div class="k">DAYS</div>
      <div class="v">{days_count}</div>
      <div class="n">issues published</div>
    </div>
  </div>
</div>"""

    # ── section head: today ──
    categories = list(dict.fromkeys(a.get("category","") for a in today_articles))
    pills = "".join(
        f'<span class="pill{"  red" if i==0 else ""}">{c}</span>'
        for i, c in enumerate(categories[:4])
    )
    # カテゴリフィルターボタン
    filter_btns = '<button class="filter-pill active" data-cat="ALL" style="font-family:\'JetBrains Mono\',monospace;font-size:10px;letter-spacing:.12em;padding:5px 12px;border:1px solid var(--rule-2);background:var(--ink);color:var(--paper);cursor:pointer;transition:all .15s;text-transform:uppercase;">ALL</button>'
    for cat in categories:
        filter_btns += f'<button class="filter-pill" data-cat="{cat}" style="font-family:\'JetBrains Mono\',monospace;font-size:10px;letter-spacing:.12em;padding:5px 12px;border:1px solid var(--rule-2);background:none;color:var(--ink);cursor:pointer;transition:all .15s;text-transform:uppercase;">{cat}</button>'

    section_today = f"""<div class="section-head" id="today">
  <span class="kicker">§01</span>
  <h2>Today's Dispatch</h2>
  <span class="jp">今朝の配信</span>
  <span class="count">{len(today_articles)} items</span>
  <a href="./news/{today_str}/" class="morelink">ALL {len(today_articles)} ITEMS →</a>
</div>
<div class="today-strip">
  {pills}
  <div class="bar"></div>
  <span>{today_str}</span>
</div>
<div style="max-width:1400px;margin:0 auto;padding:0 40px 20px;display:flex;gap:8px;flex-wrap:wrap;">
  {filter_btns}
</div>"""

    # ── today cards grid ──
    cards_html = _build_today_grid(today_articles, today_str, img_dir, root="./")

    # ── archive ──
    section_archive = f"""<div class="section-head" id="archive">
  <span class="kicker">§02</span>
  <h2>Archive</h2>
  <span class="jp">過去のディスパッチ</span>
  <span class="count">{days_count} issues</span>
</div>
<div class="archive">
  <div class="archive-list">"""

    for d in sorted(all_dates, reverse=True)[:30]:
        dd = datetime.strptime(d, "%Y-%m-%d")
        is_today = "today" if d == today_str else ""
        # articles.jsonから記事データ読み込み
        art_path = SITE_DIR / "news" / d / "articles.json"
        day_articles = []
        if art_path.exists():
            try:
                day_articles = json.loads(art_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        count = len(day_articles) or 8
        head = day_articles[0]["title"] if day_articles else "Morning Dispatch"
        cats = list(dict.fromkeys(a.get("category","") for a in day_articles[:3]))
        tags = "".join(f'<span>{c}</span>' for c in cats[:3])

        section_archive += f"""
    <a href="./news/{d}/" class="arow {is_today}">
      <div class="dt"><span class="day">{dd.day:02d}</span> <span class="wd">{WEEKDAYS_EN[dd.weekday()]}</span></div>
      <div class="head">{head[:60]}{"…" if len(head)>60 else ""}</div>
      <div class="items"><b>{count}</b> items</div>
      <div class="tags">{tags}</div>
      <div class="arr">→</div>
    </a>"""

    section_archive += "\n  </div>\n</div>"

    # ── about ──
    section_about = f"""<div class="section-head" id="about">
  <span class="kicker">§03</span>
  <h2>About</h2>
  <span class="jp">VIGILについて</span>
</div>
<div class="about">
  <div class="card-about">
    <h3>VIGIL — AI Morning Intelligence</h3>
    <p>毎朝07:15 JSTにAIエージェントが自律起動し、RSS・ニュースソースを収集・要約・スライド化してGitHub Pagesに自動配信。人間の介入ほぼゼロで動くモーニングディスパッチです。</p>
    <p>PIPELINE: RSS → CLAUDE HAIKU → GEMINI SLIDES → GITHUB PAGES</p>
    <div class="deliverbox">
      <div><div class="b">CURATOR</div><div class="v">山中秀斗</div></div>
      <div><div class="b">SINCE</div><div class="v">{min(all_dates) if all_dates else today_str}</div></div>
      <div><div class="b">TIME</div><div class="v">07:15 JST</div></div>
      <div><div class="b">ISSUES</div><div class="v">{days_count}</div></div>
    </div>
  </div>
  <div class="sources">
    <h3>RSS SOURCES</h3>
    <ul>
      <li><span class="dot"></span><span class="nm">OpenAI Blog</span></li>
      <li><span class="dot"></span><span class="nm">Anthropic Blog</span></li>
      <li><span class="dot"></span><span class="nm">Google AI Blog</span></li>
      <li><span class="dot"></span><span class="nm">TechCrunch AI</span></li>
      <li><span class="dot"></span><span class="nm">The Verge AI</span></li>
      <li><span class="dot"></span><span class="nm">MIT Tech Review AI</span></li>
      <li><span class="dot"></span><span class="nm">ITmedia AI</span></li>
      <li><span class="dot"></span><span class="nm">Zenn AI</span></li>
    </ul>
  </div>
</div>"""

    # ── colophon ──
    colophon = f"""<div class="colophon">
  <div class="left"><b>VIGIL</b> · AI Morning Intelligence · 山中秀斗 / TREPRO</div>
  <div class="right">{today_str} · BUILD {dt.strftime('%Y%m%d')}.0715</div>
</div>"""

    html = _head(
        "VIGIL — AI Morning Intelligence",
        "山中秀斗が毎朝整理するAI業界のモーニングディスパッチ。",
        "./assets/vigil.css",
        FONTS_VIGIL,
    ) + INDEX_CSS + f"""
{dispatch}
{nav}
{hero}
{stats}
{section_today}
{cards_html}
{section_archive}
{section_about}
{colophon}
{INTERACTIVE_JS}
</body>
</html>"""

    out_path = SITE_DIR / "index.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


def _build_today_grid(articles, date_str, img_dir, root="../../"):
    """vigil.css の .today-grid / .tcard / .tcard.lead を生成"""
    img_root = f"{root}assets/images/{date_str}"
    html = '<div class="today-grid">\n'

    for i, a in enumerate(articles, 1):
        title      = a.get("title", "")
        category   = a.get("category", "AI情報")
        source     = a.get("source", "")
        lede       = a.get("lede", "")
        detail_url = f"{root}news/{date_str}/#topic-{i}"
        slide_rel  = f"{img_root}/topic_{i}.png"
        slide_exists = (img_dir / f"topic_{i}.png").exists()

        import json as _json
        kp_json = _json.dumps(a.get("keypoints", []), ensure_ascii=False).replace('"', '&quot;')
        pull_esc = a.get("pull","").replace('"','&quot;')
        data_attrs = (
            f'data-title="{title.replace(chr(34), "&quot;")}" '
            f'data-category="{category}" '
            f'data-source="{source}" '
            f'data-lede="{lede.replace(chr(34), "&quot;")}" '
            f'data-keypoints="{kp_json}" '
            f'data-pull="{pull_esc}" '
            f'data-link="{detail_url}"'
        )

        if i == 1:
            # ── Lead card (2×2, dark background) ──
            if slide_exists:
                slide_html = f"""    <a href="{detail_url}" class="slide zoom-image" data-src="{slide_rel}" data-alt="{title}" role="button" tabindex="0" style="display:block;">
      <img src="{slide_rel}" alt="{title}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;" loading="lazy" />
      <div class="sl-inner">
        <div class="chip">VIGIL · SLIDE 01 / {len(articles):02d} <b>●</b></div>
        <div style="flex:1"></div>
        <div class="meta">{category.upper()} · {source.upper()}</div>
      </div>
    </a>"""
            else:
                slide_html = f"""    <div class="slide">
      <div class="sl-inner">
        <div class="chip">VIGIL · SLIDE 01 / {len(articles):02d} <b>●</b></div>
        <div class="bigt">{title[:24]}</div>
        <div class="meta">{category.upper()} · {source.upper()}</div>
      </div>
    </div>"""

            html += f"""  <div class="tcard lead" {data_attrs}>
    <div class="tl">
      <span class="n">01</span>
      <span class="cat">{category}</span>
      <span class="top">TOP STORY</span>
    </div>
    <h3>{title}</h3>
{slide_html}
    <p class="lede">{lede}</p>
    <div class="foot">
      <span class="src">{source}</span>
      <a href="{detail_url}" class="go">READ →</a>
    </div>
  </div>
"""
        else:
            # ── Regular card — 画像なし（vigil.css 仕様通り）──
            html += f"""  <div class="tcard" {data_attrs}>
    <div class="tl">
      <span class="n">{str(i).zfill(2)}</span>
      <span class="cat">{category}</span>
    </div>
    <h3>{title}</h3>
    <p class="lede">{lede}</p>
    <div class="foot">
      <span class="src">{source}</span>
      <a href="{detail_url}" class="go">READ →</a>
    </div>
  </div>
"""

    html += "</div>\n"
    return html


# ── DAILY DETAIL PAGE ────────────────────────────────────────

def build_daily_page(date_str: str, articles: list[dict], issue_num: int = None) -> Path:
    dt        = datetime.strptime(date_str, "%Y-%m-%d")
    issue     = str(issue_num or int(dt.strftime("%m%d"))).zfill(4)
    weekday   = WEEKDAYS_EN[dt.weekday()]
    month_en  = MONTHS_EN[dt.month - 1]

    out_dir = SITE_DIR / "news" / date_str
    out_dir.mkdir(parents=True, exist_ok=True)
    img_dir = SITE_DIR / "assets" / "images" / date_str
    img_dir.mkdir(parents=True, exist_ok=True)

    # ── dispatch ──
    dispatch = f"""<div class="dispatch">
  <span class="tick">VIGIL</span>
  <span class="sep">/</span>
  <span>№{issue}</span>
  <span class="sep">/</span>
  <span>{date_str}</span>
  <span class="sep">/</span>
  <span>MORNING EDITION</span>
  <span class="sep">/</span>
  <span>{len(articles)} ITEMS</span>
  <span class="sep">/</span>
  <span class="live"><span class="dot"></span>LIVE</span>
  <div class="right">
    <span class="jst"><b>07:15</b> JST</span>
    <span>{weekday}</span>
  </div>
</div>"""

    # ── nav ──
    nav = f"""<nav class="main">
  <div class="brand"><em>●</em>VIGIL</div>
  <ul>
    <li><a href="../../">HOME</a></li>
    <li><a href="./" class="active">TODAY</a></li>
    <li><a href="../../#archive">ARCHIVE</a></li>
    <li><a href="../../#about">ABOUT</a></li>
  </ul>
  <button class="subscribe" onclick="return false">SUBSCRIBE · 07:15 DAILY →</button>
</nav>"""

    # ── daily head ──
    daily_head = f"""<div class="hero-wrap">
  <div class="edition-line">
    MORNING DISPATCH
    <span class="sep">//</span>
    {WEEKDAYS_LONG[dt.weekday()]}, {month_en} {dt.day}, {dt.year}
    <span class="sep">//</span>
    ISSUE N°{issue}
  </div>
  <h1 class="date-huge">{dt.year}<span class="dot">.</span>{dt.strftime('%m')}<span class="dot">.</span>{dt.strftime('%d')}</h1>
  <div class="strap">
    <span><span class="count">{len(articles):02d}</span>&nbsp;ITEMS</span>
    <span>AI MORNING INTELLIGENCE</span>
  </div>
</div>"""

    # ── articles ──
    topics_html = ""
    for i, a in enumerate(articles, 1):
        slide_rel    = f"../../assets/images/{date_str}/topic_{i}.png"
        slide_exists = (img_dir / f"topic_{i}.png").exists()
        slide_html   = ""
        if slide_exists:
            slide_html = (
                f'      <div class="slide-img zoom-image" data-src="{slide_rel}" '
                f'data-alt="{a["title"]}" role="button" tabindex="0">\n'
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
        "../../assets/vigil.css",
        FONTS_VIGIL,
    ) + DAILY_CSS + f"""
{dispatch}
{nav}
{daily_head}
{topics_html}
<div class="colophon">
  <div class="left"><b>VIGIL</b> · AI Morning Intelligence · 山中秀斗 / TREPRO</div>
  <div class="right">{date_str} DISPATCH</div>
</div>
{INTERACTIVE_JS}
</body>
</html>"""

    out_path = out_dir / "index.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


# インデックスページ専用インタラクションCSS
INDEX_CSS = """
<style>
/* tcard フェードイン */
.tcard{opacity:0;transform:translateY(18px);transition:opacity .45s,transform .45s,box-shadow .2s,outline .15s;}
.tcard.is-visible{opacity:1;transform:none;}
.tcard[data-title]{cursor:pointer;}
.tcard[data-title]:hover{box-shadow:0 6px 28px rgba(0,0,0,.08);outline:2px solid var(--red);}
.tcard[data-title]:hover .go{color:var(--red);}
.tcard[data-title]:hover h3{color:var(--red);}
h3{transition:color .15s;}
/* フィルター active */
.filter-pill.active{background:var(--ink)!important;color:var(--paper)!important;border-color:var(--ink)!important;}
.filter-pill:hover{background:var(--red)!important;color:#fff!important;border-color:var(--red)!important;}
/* カテゴリ遷移 */
.tcard{transition:opacity .45s,transform .45s,box-shadow .2s,outline .15s;}
</style>"""

# vigil.css にない detail ページ専用スタイル（inline で追加）
DAILY_CSS = """
<style>
.date-huge{font-family:'JetBrains Mono',monospace;font-weight:800;font-size:clamp(48px,10vw,112px);line-height:.9;letter-spacing:-.03em;margin:8px 0 20px;}
.date-huge .dot{color:var(--red)}
.strap{display:flex;gap:28px;flex-wrap:wrap;font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute);}
.strap .count{color:var(--ink);font-weight:700}
.container{max-width:1400px;margin:0 auto;padding:0 40px}
.daily-topic{padding:52px 0;border-bottom:1px solid var(--rule);position:relative;opacity:0;transform:translateY(20px);transition:opacity .5s,transform .5s;}
.daily-topic.is-visible{opacity:1;transform:none}
.daily-topic::before{content:"";position:absolute;left:0;top:0;width:3px;height:0;background:var(--red);transition:height .4s}
.daily-topic:hover::before{height:100%}
.daily-topic .container{display:grid;grid-template-columns:72px 1fr 240px;gap:36px}
.numeral{font-family:'JetBrains Mono',monospace;font-weight:800;font-size:64px;line-height:1;color:var(--rule-2);position:relative;top:-6px;transition:color .2s}
.daily-topic:hover .numeral{color:var(--red)}
.numeral .ord{display:block;font-size:9px;letter-spacing:.16em;color:var(--mute);margin-top:8px;line-height:1.4;white-space:nowrap}
.cat-line{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--red);margin-bottom:14px}
.cat-line .sep{color:var(--mute);margin:0 8px}
.main h2{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:26px;line-height:1.3;margin:0 0 18px;letter-spacing:-.01em}
.lede{font-family:'Noto Serif JP',serif;font-size:16px;line-height:1.75;margin:0 0 24px;color:var(--ink-2)}
.main h3{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.2em;text-transform:uppercase;margin:24px 0 10px;color:var(--mute)}
.keypoints{list-style:none;padding:0;margin:0 0 24px}
.keypoints li{padding:10px 14px 10px 44px;margin-bottom:2px;background:var(--paper-2);border-left:2px solid transparent;position:relative;font-size:14px;line-height:1.6;transition:border-color .15s,transform .2s}
.keypoints li:hover{border-left-color:var(--red);transform:translateX(4px)}
.keypoints li::before{content:attr(data-i);position:absolute;left:14px;top:10px;font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--red);letter-spacing:.1em}
.pull{padding:18px 22px;border-left:3px solid var(--red);background:var(--paper-2);font-size:14px;line-height:1.7;color:var(--ink-2);font-style:italic;margin-top:24px;transition:border-left-width .2s,padding-left .2s}
.pull:hover{border-left-width:6px;padding-left:19px}
.slide-img{margin:20px 0;border:1px solid var(--rule-2);overflow:hidden;cursor:zoom-in;position:relative;transition:border-color .2s}
.slide-img:hover{border-color:var(--red)}
.slide-img img{width:100%;display:block;transition:transform .5s}
.slide-img:hover img{transform:scale(1.02)}
.side{font-size:13px}
.side dl{margin:0}
.side dt{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.18em;text-transform:uppercase;color:var(--mute);margin:18px 0 4px}
.side dt:first-child{margin-top:0}
.side dd{margin:0;word-break:break-all}
.side dd a:hover{color:var(--red)}
.likes{font-family:'JetBrains Mono',monospace;font-weight:700;font-size:28px;color:var(--red)}
.likes-label{font-size:11px;color:var(--mute);letter-spacing:.1em;text-transform:uppercase}
.lightbox-overlay{display:flex;align-items:center;justify-content:center;position:fixed;inset:0;padding:24px;background:rgba(14,13,11,0);z-index:1000;pointer-events:none;transition:background .3s}
.lightbox-overlay.is-open{background:rgba(14,13,11,.93);pointer-events:auto}
.lightbox-overlay img{max-width:100%;max-height:90vh;object-fit:contain;opacity:0;transform:scale(.93);transition:opacity .35s,transform .35s}
.lightbox-overlay.is-open img{opacity:1;transform:scale(1)}
.lightbox-close{position:absolute;top:20px;right:24px;font-family:'JetBrains Mono',monospace;font-size:12px;color:#F7F5F2;cursor:pointer;background:none;border:1px solid rgba(247,245,242,.3);padding:6px 14px;transition:background .2s}
.lightbox-close:hover{background:var(--red)}
@media(max-width:900px){.daily-topic .container{grid-template-columns:1fr}.numeral{font-size:36px}.side{border-top:1px solid var(--rule);padding-top:20px}}
</style>"""


# ── CLI テスト ────────────────────────────────────────────────

if __name__ == "__main__":
    today = "2026-04-23"
    art_path = SITE_DIR / "news" / today / "articles.json"
    if art_path.exists():
        articles = json.loads(art_path.read_text(encoding="utf-8"))
        print(f"articles.json から {len(articles)} 件読み込み")
    else:
        articles = [
            {"title":"OpenAIがワークスペースエージェント機能をChatGPTに導入","category":"ツール更新","source":"OpenAI Blog","lede":"ChatGPTにCodex駆動のワークスペースエージェントが統合され、複雑なワークフロー自動化とクラウド実行によるチーム作業の効率化が実現。","keypoints":["Codex駆動エージェントがワークフロー自動化を実現","複数ツール連携でチーム作業をスケール"],"pull":"エージェント時代の到来により企業の生産性向上が加速。"},
        ] * 3

    p1 = build_daily_page(today, articles)
    print(f"daily: {p1}")
    p2 = build_index([today], articles, today)
    print(f"index: {p2}")
