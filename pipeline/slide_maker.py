"""
VIGIL — Slide Maker
Gemini 3.1 Flash Image Preview APIで各記事のスライド画像を生成する
nano-banana v3 Flashを流用
"""
import os
import base64
import requests
import time
from pathlib import Path

API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_ID = "gemini-3.1-flash-image-preview"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

SLIDE_PROMPT_TEMPLATE = """
Create a 16:9 editorial news card slide for the following AI news article.

ARTICLE:
Title: {title}
Category: {category}
Source: {source}
Summary: {summary}
Key Points:
{keypoints}

DESIGN REQUIREMENTS:
- Style: Clean editorial / newspaper-inspired
- Background: Warm white/cream (#F7F5F2)
- Accent color: TREPRO Red (#F10903) for highlights and borders
- Typography: Bold headline, clear hierarchy, no decorative fonts
- Layout: Title prominent at top, key points as visual elements
- Include category label and source badge
- Brand mark: "VIGIL" in small monospace font, top-right corner
- NO dark backgrounds
- Clean minimal professional look
- Japanese text rendered clearly if present
- Image size: 16:9, high quality
"""


def generate_slide(
    title: str,
    category: str,
    source: str,
    summary: str,
    keypoints: list[str],
    output_path: Path,
    size: str = "2K",
) -> bool:
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY が未設定です")

    kp_text = "\n".join(f"- {kp}" for kp in keypoints[:5])
    prompt = SLIDE_PROMPT_TEMPLATE.format(
        title=title, category=category, source=source,
        summary=summary[:300], keypoints=kp_text,
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": "16:9",
                "imageSize": size,
            },
            "thinkingConfig": {
                "thinkingLevel": "High",
                "includeThoughts": False,
            },
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        ],
    }

    url = f"{API_BASE}/{MODEL_ID}:generateContent?key={API_KEY}"

    for attempt in range(3):
        try:
            resp = requests.post(url, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()

            for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
                if "inlineData" in part:
                    img_bytes = base64.b64decode(part["inlineData"]["data"])
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_bytes(img_bytes)
                    return True

        except Exception as e:
            print(f"  [attempt {attempt+1}/3] Gemini error: {e}")
            if attempt < 2:
                time.sleep(5 * (attempt + 1))

    return False


if __name__ == "__main__":
    out = Path("/tmp/test_slide.png")
    ok = generate_slide(
        title="OpenAI Codex 4M MAU突破",
        category="ツール更新",
        source="@sama",
        summary="CodexのMAUが400万人に到達。わずか2週間で3Mから4Mへ急増。",
        keypoints=["MAU 400万人到達", "2週間で100万人増", "レートリミット緩和を即時発表"],
        output_path=out,
    )
    print(f"生成: {ok} → {out}")
