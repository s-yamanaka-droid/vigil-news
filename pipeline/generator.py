"""
VIGIL — Generator v2
元記事本文をHaikuに渡してファクトグラウンドな要約を生成する
"""
import json
import anthropic

client = anthropic.Anthropic()

SYSTEM = """あなたはAI業界ニュースの専門編集者です。
与えられた記事の【元記事本文】を一次情報として使い、ニュースサイト掲載用データをJSON配列で返してください。

出力形式（JSON配列）:
[
  {
    "title": "見出し（日本語・40字以内）",
    "category": "カテゴリ（業界動向/ツール更新/新モデル発表/研究/その他）",
    "source": "ソース名",
    "lede": "リード文（日本語・100字以内・核心を一文で）",
    "keypoints": ["要点1（30字以内）", "要点2", "要点3", "要点4"],
    "pull": "プルクォート（60字以内・本質的な洞察を）",
    "links": ["元記事URL"],
    "likes": 0
  }
]

厳守ルール：
- 上位8件を重要度順で選ぶ
- 全て日本語
- 【元記事本文】に書かれていない事実・数字・固有名詞は絶対に追加しない
- 本文が空の場合はタイトルとRSS要約だけを根拠にする
- 重複記事はまとめる
- ビジネスパーソン向けに簡潔に"""


def generate_articles(raw_articles: list[dict]) -> list[dict]:
    # 記事ごとに元本文を含めた情報を構築
    blocks = []
    for a in raw_articles[:24]:
        body_part = f"\n【元記事本文】\n{a['body'][:1500]}" if a.get("body") else ""
        blocks.append(
            f"[{a['source']}] {a['title']}\n"
            f"RSS要約: {a['summary'][:200]}\n"
            f"URL: {a.get('link','')}"
            f"{body_part}"
        )
    digest = "\n\n---\n\n".join(blocks)

    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4000,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"今日のAI関連記事:\n\n{digest}"}],
    )

    text = msg.content[0].text.strip()
    start = text.find("[")
    end   = text.rfind("]") + 1
    return json.loads(text[start:end])


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.home() / "agents/cmo/x_agent"))
    from researcher import fetch_latest
    raw = fetch_latest(max_per_feed=3, fetch_body=True)
    articles = generate_articles(raw)
    print(json.dumps(articles, ensure_ascii=False, indent=2))
