#!/usr/bin/env python3
"""Fix cardapio base readability colors.

This script removes ambiguity between early base CSS and the final
Visual Readability Reality Fix by aligning the first .menu-item rules
with the final browser-validated colors:
- dish name: #335d4a
- description: #485156
- price: #9a6500
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDAPIO = ROOT / "cardapio.html"

REPLACEMENTS = {
    """  .menu-item-name {\n    font-family: \"Catamaran\", sans-serif;\n    font-weight: 700; font-size: 18px;\n    color: var(--azul1); margin: 0;\n  }""": """  .menu-item-name {\n    font-family: \"Catamaran\", sans-serif;\n    font-weight: 900; font-size: 18px;\n    color: #335d4a; margin: 0;\n  }""",
    """  .menu-item-desc {\n    font-size: 14.5px; color: var(--cinza1);\n    line-height: 1.5; margin: 0;\n  }""": """  .menu-item-desc {\n    font-size: 14.5px; color: #485156;\n    line-height: 1.5; margin: 0;\n  }""",
    """  .menu-item-price {\n    font-family: \"JetBrains Mono\", monospace;\n    font-size: 13px; font-weight: 500;\n    color: var(--verde); margin-top: 8px;\n  }""": """  .menu-item-price {\n    font-family: \"JetBrains Mono\", monospace;\n    font-size: 13px; font-weight: 900;\n    color: #9a6500; margin-top: 8px;\n  }""",
}


def main() -> int:
    text = CARDAPIO.read_text(encoding="utf-8")
    changed = text
    missing: list[str] = []

    for old, new in REPLACEMENTS.items():
        if old not in changed:
            missing.append(old.split("\n", 1)[0].strip())
        changed = changed.replace(old, new, 1)

    if missing:
        print("WARN: some expected blocks were not found:")
        for item in missing:
            print(f"- {item}")

    if changed != text:
        CARDAPIO.write_text(changed, encoding="utf-8")
        print("Updated cardapio.html base menu readability colors.")
    else:
        print("No changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
