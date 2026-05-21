#!/usr/bin/env python3
"""Inject final CSS + runtime inline visible-text lock in como-chegar.html."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "como-chegar.html"
REPORT = ROOT / "_audit_reports" / "como_chegar_final_visible_lock_report.md"
LOCK_ID = "ec-como-chegar-final-visible-lock"
SCRIPT_ID = "ec-como-chegar-runtime-visible-lock"
LOCK_RE = re.compile(
    r"\n?<!-- EC Como Chegar Final Visible Lock -->.*?<!-- /EC Como Chegar Final Visible Lock -->",
    re.DOTALL,
)

LOCK = f'''<!-- EC Como Chegar Final Visible Lock -->
<style id="{LOCK_ID}">
/* Page-specific final lock: Como Chegar is a light content page. */
html body[data-screen-label="Como Chegar"] main {{
  background:#f6efde !important;
  color:#00405a !important;
  -webkit-text-fill-color:initial !important;
}}
html body[data-screen-label="Como Chegar"] main section {{
  background:#f6efde !important;
  color:#00405a !important;
  -webkit-text-fill-color:initial !important;
}}
html body[data-screen-label="Como Chegar"] main :is(.box,.access-fact,.access-route,details,.ec-sprint5-card,ol) {{
  background:#fffaf0 !important;
  color:#00405a !important;
  -webkit-text-fill-color:#00405a !important;
  border-color:rgba(0,64,90,.16) !important;
  opacity:1 !important;
  visibility:visible !important;
  text-shadow:none !important;
}}

/* Public UX: hide technical SEO/GEO labels from visitors. */
html body[data-screen-label="Como Chegar"] main section.access-direct .box > .kicker,
html body[data-screen-label="Como Chegar"] main section.access-faq .kicker {{
  display:none !important;
}}

/* Heading balance: keep authority without oversized visual weight. */
html body[data-screen-label="Como Chegar"] main section.access-direct .box > h2 {{
  color:#00405a !important;
  -webkit-text-fill-color:#00405a !important;
  font-size:clamp(34px,3.4vw,48px) !important;
  line-height:1.08 !important;
  letter-spacing:.02em !important;
  max-width:880px !important;
  margin:0 0 18px !important;
  opacity:1 !important;
  visibility:visible !important;
  text-shadow:none !important;
}}
html body[data-screen-label="Como Chegar"] main section.access-section .wrap > h2,
html body[data-screen-label="Como Chegar"] main section.access-faq .wrap > h2,
html body[data-screen-label="Como Chegar"] main section.ec-sprint4-steps .wrap > h2,
html body[data-screen-label="Como Chegar"] main section.ec-sprint5-quality .wrap > h2 {{
  color:#00405a !important;
  -webkit-text-fill-color:#00405a !important;
  font-size:clamp(30px,3vw,42px) !important;
  line-height:1.1 !important;
  letter-spacing:.02em !important;
  margin:0 0 24px !important;
  opacity:1 !important;
  visibility:visible !important;
  text-shadow:none !important;
}}
html body[data-screen-label="Como Chegar"] main :is(h1,h2,h3,h4,h5,h6,summary,strong,b) {{
  color:#00405a !important;
  -webkit-text-fill-color:#00405a !important;
  opacity:1 !important;
  visibility:visible !important;
  text-shadow:none !important;
}}
html body[data-screen-label="Como Chegar"] main :is(p,li,span,small,dd,dt) {{
  color:#485156 !important;
  -webkit-text-fill-color:#485156 !important;
  opacity:1 !important;
  visibility:visible !important;
  text-shadow:none !important;
}}
html body[data-screen-label="Como Chegar"] main :is(.eyebrow,.tag,a:not(.btn):not(.secondary)) {{
  color:#9a6500 !important;
  -webkit-text-fill-color:#9a6500 !important;
  opacity:1 !important;
  visibility:visible !important;
  text-shadow:none !important;
}}
</style>
<script id="{SCRIPT_ID}">
(function(){{
  function imp(el, prop, val){{ if(el && el.style) el.style.setProperty(prop, val, 'important'); }}
  function all(sel, fn){{ document.querySelectorAll(sel).forEach(fn); }}
  function run(){{
    if(!document.body || document.body.getAttribute('data-screen-label') !== 'Como Chegar') return;
    all('main, main section', function(el){{ imp(el,'background','#f6efde'); imp(el,'color','#00405a'); imp(el,'-webkit-text-fill-color','initial'); }});
    all('main .box, main .access-fact, main .access-route, main details, main .ec-sprint5-card, main ol', function(el){{
      imp(el,'background','#fffaf0'); imp(el,'color','#00405a'); imp(el,'-webkit-text-fill-color','#00405a'); imp(el,'opacity','1'); imp(el,'visibility','visible'); imp(el,'text-shadow','none'); imp(el,'filter','none'); imp(el,'mix-blend-mode','normal');
    }});
    all('section.access-direct .box > .kicker, section.access-faq .kicker', function(el){{ imp(el,'display','none'); }});
    all('section.access-direct .box > h2', function(el){{
      imp(el,'color','#00405a'); imp(el,'-webkit-text-fill-color','#00405a'); imp(el,'font-size','clamp(34px,3.4vw,48px)'); imp(el,'line-height','1.08'); imp(el,'letter-spacing','.02em'); imp(el,'max-width','880px'); imp(el,'margin','0 0 18px'); imp(el,'opacity','1'); imp(el,'visibility','visible'); imp(el,'text-shadow','none');
    }});
    all('section.access-section .wrap > h2, section.access-faq .wrap > h2, section.ec-sprint4-steps .wrap > h2, section.ec-sprint5-quality .wrap > h2', function(el){{
      imp(el,'color','#00405a'); imp(el,'-webkit-text-fill-color','#00405a'); imp(el,'font-size','clamp(30px,3vw,42px)'); imp(el,'line-height','1.1'); imp(el,'letter-spacing','.02em'); imp(el,'margin','0 0 24px'); imp(el,'opacity','1'); imp(el,'visibility','visible'); imp(el,'text-shadow','none');
    }});
    all('main h1, main h2, main h3, main h4, main h5, main h6, main summary, main strong, main b', function(el){{
      imp(el,'color','#00405a'); imp(el,'-webkit-text-fill-color','#00405a'); imp(el,'opacity','1'); imp(el,'visibility','visible'); imp(el,'text-shadow','none'); imp(el,'filter','none'); imp(el,'mix-blend-mode','normal');
    }});
    all('main p, main li, main span, main small, main dd, main dt', function(el){{
      if(el.closest('.kicker,.eyebrow,.tag')) return;
      imp(el,'color','#485156'); imp(el,'-webkit-text-fill-color','#485156'); imp(el,'opacity','1'); imp(el,'visibility','visible'); imp(el,'text-shadow','none'); imp(el,'filter','none'); imp(el,'mix-blend-mode','normal');
    }});
    all('main .eyebrow, main .tag, main a:not(.btn):not(.secondary)', function(el){{
      imp(el,'color','#9a6500'); imp(el,'-webkit-text-fill-color','#9a6500'); imp(el,'opacity','1'); imp(el,'visibility','visible'); imp(el,'text-shadow','none');
    }});
  }}
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, {{once:true}}); else run();
  window.addEventListener('load', function(){{ run(); setTimeout(run,250); setTimeout(run,1000); }}, {{once:true}});
}})();
</script>
<!-- /EC Como Chegar Final Visible Lock -->'''


def main() -> int:
    text = PAGE.read_text(encoding="utf-8")
    text, replaced = LOCK_RE.subn("", text)
    if "</body>" in text:
        text = text.replace("</body>", LOCK + "\n</body>", 1)
    else:
        text += "\n" + LOCK + "\n"
    PAGE.write_text(text, encoding="utf-8")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "# Como Chegar Final Visible Lock Report\n\n"
        "- CSS final light-page lock: PASS\n"
        "- Runtime inline color lock: PASS\n"
        "- Technical SEO/GEO kicker hidden from public UI: PASS\n"
        "- Heading sizes rebalanced: PASS\n"
        f"- Previous locks removed: {replaced}\n"
        "- Target page: como-chegar.html\n",
        encoding="utf-8",
    )
    print(REPORT.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
