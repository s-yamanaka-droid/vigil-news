"""
VIGIL — Deploy
生成したHTMLをGitHubにpushしてPages公開する
"""
import subprocess
import os
from pathlib import Path

SITE_DIR = Path(__file__).parent.parent / "site"
REPO_DIR = Path(__file__).parent.parent


def git_push(commit_msg: str) -> bool:
    cmds = [
        ["git", "-C", str(REPO_DIR), "add", "docs/"],
        ["git", "-C", str(REPO_DIR), "commit", "-m", commit_msg],
        ["git", "-C", str(REPO_DIR), "push", "origin", "main"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            # commitが空の場合はスキップ
            if "nothing to commit" in result.stdout + result.stderr:
                print("  変更なし、スキップ")
                return True
            print(f"  エラー: {result.stderr}")
            return False
    return True


if __name__ == "__main__":
    from datetime import datetime
    date_str = datetime.now().strftime("%Y-%m-%d")
    ok = git_push(f"dispatch: {date_str} morning edition")
    print(f"デプロイ: {'成功' if ok else '失敗'}")
