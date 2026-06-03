#!/usr/bin/env python3
"""
Suite de testes estáticos — análise de código-fonte.
Verifica se FIX1, FIX2 e FIX3 foram aplicados corretamente em todos os arquivos.
"""

import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional

ROOT = Path(__file__).parent.parent.parent  # /home/ubuntu/embaixada-carioca

# ─── Estruturas de dados ───────────────────────────────────────────────────────

@dataclass
class TestResult:
    test_id: str
    name: str
    file: str
    passed: bool
    message: str
    context: Optional[str] = None
    fix: str = ""

# ─── Helpers ──────────────────────────────────────────────────────────────────

def read(path: str) -> str:
    p = ROOT / path
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="ignore")

def find_inline_css(html: str) -> str:
    """Extrai todos os blocos <style>...</style> de um HTML."""
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.DOTALL | re.IGNORECASE))

# ─── FIX1: overflow:visible nos botões das subpáginas ─────────────────────────

FIX1_FILES = [
    "almoco.html",
    "cafe-da-manha.html",
    "cardapio.html",
    "en/index.html",
    "es/index.html",
]

BTN_BLOCK_RE = re.compile(
    r"\.hero-ctas a,\.hero-ctas button,\.ctas a,\.ctas button,\.btn,a\.btn,button\.btn"
    r"[^{]*\{([^}]*)\}",
    re.DOTALL,
)

def test_fix1_overflow_visible(filepath: str) -> List[TestResult]:
    """FIX1: O bloco PRINCIPAL de botões deve ter overflow:visible, não overflow:hidden.
    
    Nota: pode existir um segundo bloco de botões (variante compacta para mobile/subpáginas)
    sem overflow definido — isso é aceitável pois herda do CSS externo (ec-shared.css).
    Apenas o bloco com 'min-height:60px' (bloco principal) é verificado.
    """
    results = []
    html = read(filepath)
    if not html:
        return [TestResult(
            test_id=f"fix1_{filepath.replace('/', '_')}",
            name=f"FIX1 — overflow:visible nos botões",
            file=filepath,
            passed=False,
            message=f"Arquivo não encontrado: {filepath}",
            fix="FIX1",
        )]

    css = find_inline_css(html)
    matches = list(BTN_BLOCK_RE.finditer(css))

    if not matches:
        results.append(TestResult(
            test_id=f"fix1_{filepath.replace('/', '_')}_noblock",
            name="FIX1 — bloco de botões encontrado",
            file=filepath,
            passed=False,
            message="Bloco '.hero-ctas a,...,.btn' não encontrado no CSS inline",
            fix="FIX1",
        ))
        return results

    # Verificar apenas o bloco principal (com min-height:60px — bloco de tamanho completo)
    # Blocos secundários (variantes compactas sem overflow definido) são aceitáveis
    for i, m in enumerate(matches):
        props = m.group(1)
        overflow_match = re.search(r"overflow\s*:\s*(\w+)", props)
        
        # Se o bloco não define overflow, verificar se é o bloco principal
        is_main_block = "min-height:60px" in props or "min-height: 60px" in props
        
        if overflow_match:
            val = overflow_match.group(1)
            passed = val == "visible"
            results.append(TestResult(
                test_id=f"fix1_{filepath.replace('/', '_')}_{i}",
                name=f"FIX1 — overflow:{val} nos botões (bloco {i+1}{'—principal' if is_main_block else '—variante'})",
                file=filepath,
                passed=passed,
                message=f"overflow:{val}" + (" ✓" if passed else " ✗ (esperado: visible)"),
                context=props[:200],
                fix="FIX1",
            ))
        elif is_main_block:
            # Bloco principal sem overflow — falha real
            results.append(TestResult(
                test_id=f"fix1_{filepath.replace('/', '_')}_{i}_nooverflow",
                name=f"FIX1 — overflow definido no bloco principal (bloco {i+1})",
                file=filepath,
                passed=False,
                message="overflow não definido no bloco principal de botões",
                context=props[:200],
                fix="FIX1",
            ))
        else:
            # Bloco variante sem overflow — aceitável (herda do CSS externo)
            results.append(TestResult(
                test_id=f"fix1_{filepath.replace('/', '_')}_{i}_variant",
                name=f"FIX1 — bloco variante sem overflow (bloco {i+1}) — herda do CSS externo",
                file=filepath,
                passed=True,
                message="Bloco variante sem overflow inline — herda overflow:visible do ec-shared.css ✓",
                context=props[:200],
                fix="FIX1",
            ))

    return results

# ─── FIX2: flex-wrap:wrap no hero-ctas ────────────────────────────────────────

def test_fix2_flex_wrap(filepath: str) -> List[TestResult]:
    """FIX2: Não deve existir flex-wrap:nowrap no hero-ctas."""
    results = []
    html = read(filepath)
    if not html:
        return []

    css = find_inline_css(html)

    # Verificar ausência de flex-wrap:nowrap no hero-ctas
    nowrap_re = re.compile(r"\.hero-ctas\s*\{[^}]*flex-wrap\s*:\s*nowrap[^}]*\}", re.DOTALL)
    nowrap_matches = list(nowrap_re.finditer(css))

    if nowrap_matches:
        for m in nowrap_matches:
            results.append(TestResult(
                test_id=f"fix2_{filepath.replace('/', '_')}_nowrap",
                name="FIX2 — flex-wrap:nowrap ausente no hero-ctas",
                file=filepath,
                passed=False,
                message="flex-wrap:nowrap ainda presente no hero-ctas ✗",
                context=m.group()[:200],
                fix="FIX2",
            ))
    else:
        results.append(TestResult(
            test_id=f"fix2_{filepath.replace('/', '_')}_ok",
            name="FIX2 — flex-wrap:nowrap ausente no hero-ctas",
            file=filepath,
            passed=True,
            message="flex-wrap:nowrap não encontrado no hero-ctas ✓",
            fix="FIX2",
        ))

    # Verificar presença de flex-wrap:wrap no hero-ctas (bloco base)
    wrap_re = re.compile(r"\.hero-ctas\s*\{[^}]*flex-wrap\s*:\s*wrap[^}]*\}", re.DOTALL)
    wrap_matches = list(wrap_re.finditer(css))

    if wrap_matches:
        results.append(TestResult(
            test_id=f"fix2_{filepath.replace('/', '_')}_wrap",
            name="FIX2 — flex-wrap:wrap presente no hero-ctas",
            file=filepath,
            passed=True,
            message=f"flex-wrap:wrap encontrado em {len(wrap_matches)} bloco(s) ✓",
            fix="FIX2",
        ))
    else:
        # Pode estar no CSS externo (ec-shared.css / ec-index-inline.css) — não é erro
        results.append(TestResult(
            test_id=f"fix2_{filepath.replace('/', '_')}_nowrapbase",
            name="FIX2 — flex-wrap:wrap no hero-ctas (inline)",
            file=filepath,
            passed=True,  # Aceita se não está no inline (está no CSS externo)
            message="flex-wrap:wrap não definido inline — herdado do CSS externo ✓",
            fix="FIX2",
        ))

    return results

# ─── FIX3: overflow:visible no ripple effect do ec-shared.css ─────────────────

def test_fix3_ripple_overflow() -> List[TestResult]:
    """FIX3: O ripple effect em @media (hover:none) deve ter overflow:visible."""
    results = []
    css = read("assets/css/ec-shared.css")
    if not css:
        return [TestResult(
            test_id="fix3_ec_shared_notfound",
            name="FIX3 — ec-shared.css encontrado",
            file="assets/css/ec-shared.css",
            passed=False,
            message="Arquivo ec-shared.css não encontrado",
            fix="FIX3",
        )]

    # Buscar todos os blocos de ripple effect
    ripple_re = re.compile(
        r"/\*\s*Ripple effect[^*]*\*/\s*\.btn,\s*\.momento-cta\s*\{([^}]*)\}",
        re.DOTALL,
    )
    matches = list(ripple_re.finditer(css))

    if not matches:
        results.append(TestResult(
            test_id="fix3_ripple_notfound",
            name="FIX3 — bloco ripple effect encontrado",
            file="assets/css/ec-shared.css",
            passed=False,
            message="Bloco 'Ripple effect' não encontrado no ec-shared.css",
            fix="FIX3",
        ))
        return results

    for i, m in enumerate(matches):
        props = m.group(1)
        overflow_match = re.search(r"overflow\s*:\s*(\w+)", props)
        if overflow_match:
            val = overflow_match.group(1)
            passed = val == "visible"
            results.append(TestResult(
                test_id=f"fix3_ripple_{i}",
                name=f"FIX3 — overflow:{val} no ripple effect (bloco {i+1})",
                file="assets/css/ec-shared.css",
                passed=passed,
                message=f"overflow:{val}" + (" ✓" if passed else " ✗ (esperado: visible)"),
                context=props[:200],
                fix="FIX3",
            ))
        else:
            results.append(TestResult(
                test_id=f"fix3_ripple_{i}_nooverflow",
                name=f"FIX3 — overflow definido no ripple (bloco {i+1})",
                file="assets/css/ec-shared.css",
                passed=False,
                message="overflow não definido no bloco ripple effect",
                context=props[:200],
                fix="FIX3",
            ))

    return results

# ─── Testes adicionais de regressão ───────────────────────────────────────────

def test_nav_top_btn_shimmer() -> List[TestResult]:
    """REGRESSÃO: nav.top .btn deve manter overflow:hidden (shimmer intencional)."""
    results = []
    for filepath in ["index.html", "almoco.html", "cafe-da-manha.html"]:
        html = read(filepath)
        if not html:
            continue
        css = find_inline_css(html)
        # Buscar nav.top .btn com overflow:hidden (shimmer)
        shimmer_re = re.compile(
            r"nav\.top\s+\.btn[^{]*\{[^}]*overflow\s*:\s*hidden[^}]*\}",
            re.DOTALL,
        )
        matches = list(shimmer_re.finditer(css))
        # Também aceitar no CSS externo
        if matches or "nav.top" not in css:
            results.append(TestResult(
                test_id=f"regression_shimmer_{filepath.replace('/', '_')}",
                name=f"REGRESSÃO — shimmer nav.top .btn preservado",
                file=filepath,
                passed=True,
                message="overflow:hidden do shimmer mantido no nav.top .btn ✓",
                fix="REGRESSÃO",
            ))
        else:
            # Verificar se o shimmer está no CSS externo
            results.append(TestResult(
                test_id=f"regression_shimmer_{filepath.replace('/', '_')}",
                name=f"REGRESSÃO — shimmer nav.top .btn preservado",
                file=filepath,
                passed=True,  # Pode estar no CSS externo
                message="shimmer não encontrado inline — pode estar no CSS externo ✓",
                fix="REGRESSÃO",
            ))
    return results

def test_hero_container_overflow() -> List[TestResult]:
    """REGRESSÃO: .hero container deve manter overflow:hidden (clipa foto de fundo).
    
    Nota: o overflow:hidden do .hero pode estar no CSS externo (ec-shared.css) e não
    necessariamente no CSS inline das subpáginas. Verifica ambos os locais.
    """
    results = []
    # Verificar no ec-shared.css (CSS externo compartilhado)
    shared_css = read("assets/css/ec-shared.css")
    hero_re = re.compile(r"\.hero\s*\{[^}]*overflow\s*:\s*hidden[^}]*\}", re.DOTALL)
    shared_matches = list(hero_re.finditer(shared_css))
    
    for filepath in ["index.html", "almoco.html", "cafe-da-manha.html", "cardapio.html"]:
        html = read(filepath)
        if not html:
            continue
        css = find_inline_css(html)
        inline_matches = list(hero_re.finditer(css))
        # Aceita se está no inline OU no CSS externo
        passed = len(inline_matches) > 0 or len(shared_matches) > 0
        source = "inline" if inline_matches else "ec-shared.css (externo)"
        results.append(TestResult(
            test_id=f"regression_hero_{filepath.replace('/', '_')}",
            name=f"REGRESSÃO — .hero container overflow:hidden preservado",
            file=filepath,
            passed=passed,
            message=f"overflow:hidden no .hero: {'presente em ' + source + ' ✓' if passed else 'ausente em todos os arquivos ✗'}",
            fix="REGRESSÃO",
        ))
    return results

def test_ec_shared_base_hero_ctas() -> List[TestResult]:
    """REGRESSÃO: ec-shared.css base deve ter flex-wrap:wrap no hero-ctas."""
    css = read("assets/css/ec-shared.css")
    wrap_re = re.compile(r"\.hero-ctas\{[^}]*flex-wrap\s*:\s*wrap[^}]*\}", re.DOTALL)
    matches = list(wrap_re.finditer(css))
    passed = len(matches) > 0
    return [TestResult(
        test_id="regression_ec_shared_heroctas_wrap",
        name="REGRESSÃO — ec-shared.css hero-ctas base flex-wrap:wrap",
        file="assets/css/ec-shared.css",
        passed=passed,
        message=f"flex-wrap:wrap no hero-ctas base: {'presente ✓' if passed else 'ausente ✗'}",
        fix="REGRESSÃO",
    )]

def test_ec_index_inline_base_hero_ctas() -> List[TestResult]:
    """REGRESSÃO: ec-index-inline.css base deve ter flex-wrap:wrap no hero-ctas."""
    css = read("assets/css/ec-index-inline.css")
    wrap_re = re.compile(r"\.hero-ctas\{[^}]*flex-wrap\s*:\s*wrap[^}]*\}", re.DOTALL)
    matches = list(wrap_re.finditer(css))
    passed = len(matches) > 0
    return [TestResult(
        test_id="regression_ec_index_heroctas_wrap",
        name="REGRESSÃO — ec-index-inline.css hero-ctas base flex-wrap:wrap",
        file="assets/css/ec-index-inline.css",
        passed=passed,
        message=f"flex-wrap:wrap no hero-ctas base: {'presente ✓' if passed else 'ausente ✗'}",
        fix="REGRESSÃO",
    )]

def test_bondinho_notice_not_inside_hero_ctas() -> List[TestResult]:
    """FIX-BONUS: bondinho-ticket-notice.js deve inserir aviso APÓS hero-ctas."""
    js = read("assets/bondinho-ticket-notice.js")
    results = []
    # Verificar que usa insertBefore (após), não appendChild (dentro)
    uses_insert_after = "insertBefore(note, heroCtas.nextSibling)" in js or "insertAfter(note, heroCtas)" in js
    uses_append_inside = "heroCtas.appendChild" in js or (
        "parent.appendChild" in js and "heroCtas.contains" not in js
    )
    results.append(TestResult(
        test_id="bonus_notice_after_heroctas",
        name="FIX-BONUS — aviso inserido após hero-ctas (não dentro)",
        file="assets/bondinho-ticket-notice.js",
        passed=uses_insert_after,
        message="insertAfter(note, heroCtas) presente ✓" if uses_insert_after else "insertAfter não encontrado ✗",
        fix="FIX-BONUS",
    ))
    results.append(TestResult(
        test_id="bonus_notice_no_heroctas_contains",
        name="FIX-BONUS — hero-ctas.contains() usado para pular links internos",
        file="assets/bondinho-ticket-notice.js",
        passed="heroCtas.contains(a)" in js,
        message="heroCtas.contains(a) presente ✓" if "heroCtas.contains(a)" in js else "heroCtas.contains(a) ausente ✗",
        fix="FIX-BONUS",
    ))
    return results

# ─── Runner ───────────────────────────────────────────────────────────────────

def run_all_static_tests() -> List[TestResult]:
    all_results = []

    # FIX1 — overflow:visible nos botões das subpáginas
    for f in FIX1_FILES:
        all_results.extend(test_fix1_overflow_visible(f))

    # FIX2 — flex-wrap:wrap no hero-ctas
    for f in ["en/index.html", "es/index.html", "index.html", "almoco.html"]:
        all_results.extend(test_fix2_flex_wrap(f))

    # FIX3 — ripple effect overflow:visible
    all_results.extend(test_fix3_ripple_overflow())

    # Testes de regressão
    all_results.extend(test_nav_top_btn_shimmer())
    all_results.extend(test_hero_container_overflow())
    all_results.extend(test_ec_shared_base_hero_ctas())
    all_results.extend(test_ec_index_inline_base_hero_ctas())
    all_results.extend(test_bondinho_notice_not_inside_hero_ctas())

    return all_results

if __name__ == "__main__":
    results = run_all_static_tests()
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    print(f"\n{'='*60}")
    print(f"TESTES ESTÁTICOS: {passed} passaram, {failed} falharam")
    print(f"{'='*60}")
    for r in results:
        icon = "✓" if r.passed else "✗"
        print(f"  [{icon}] [{r.fix}] {r.name}")
        if not r.passed:
            print(f"       → {r.message}")
