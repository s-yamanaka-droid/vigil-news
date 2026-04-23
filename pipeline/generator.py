"""
VIGIL — Generator
RSS記事からClaude Haikuでニュースカード用データを生成する
"""
import json
import anthropic

client = anthropic.Anthropic()

SYSTEM = """あなたはAI業界ニュースの専門編集者です。
与えられた記事情報をもとに、ニュースサイト掲載用のデータをJSON形式で返してください。

出力形式（JSON配列）:
[
  {
    "title": "見出し（日本語・40字以内）",
    "category": "カテゴリ（業界動向/ツール更新/新モデル発表/研究/その他）",
    "source": "ソース名",
    "lede": "リード文（日本語・100字以内・核心を一文で）",
    "keypoints": ["要点1（30字以内）", "要点2", "要点3", "要点4"],
    "pull": "プルクォート（60字以内・本質的な洞察を）",
    "links": ["URL1"],
    "likes": 0
  }
]

ルール：
- 上位8件を選ぶ（重要度順）
- 全て日本語
- ビジネスパーソン向けに簡潔に
- 重複記事はまとめる"""


def generate_articles(raw_articles: list[dict]) -> list[dict]:
    digest = "\n\n".join(
        f"[{a['source']}] {a['title']}\n{a['summary'][:200]}\nURL: {a.get('link','')}"
        for a in raw_articles[:20]
    )

    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=3000,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"今日のAI関連記事:\n\n{digest}"}],
    )

    text = msg.content[0].text.strip()
    start = text.find("[")
    end = text.rfind("]") + 1
    return json.loads(text[start:end])


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent.parent / "agents/cmo/x_agent"))
    from researcher import fetch_latest
    raw = fetch_latest(max_per_feed=4)
    articles = generate_articles(raw)
    print(json.dumps(articles, ensure_ascii=False, indent=2))
