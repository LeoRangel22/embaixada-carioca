#!/usr/bin/env python3
"""Superholistic Design/UX/SEO/GEO/AIO/SXO audit for Embaixada Carioca."""
from __future__ import annotations

import csv, json, re
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_audit_reports"
MD = OUT / "superholistic_design_ux_seo_geo_audit.md"
CSV = OUT / "superholistic_design_ux_seo_geo_audit.csv"
JS = OUT / "superholistic_design_ux_seo_geo_audit.json"
THRESHOLD = 90
EXCLUDE = {".git", ".github", "node_modules", "_audit_reports", "dist", "build", "coverage"}
UTILITY = {"404.html", "offline.html", "home-preview.html"}

DIMENSIONS = ["Design", "UX", "Copydesk", "SEO", "GEO", "AEO", "AIO", "SXO", "Marketing", "R2D2", "Schema", "Performance"]
PRIORITY_KEYWORDS = [
    "restaurante pão de açúcar", "restaurante morro da urca", "restaurante no pão de açúcar",
    "av pasteur 520 urca rio de janeiro", "restaurante pao de acucar", "restaurante no morro da urca",
    "cafe da manha na urca", "restaurante no pao de acucar rj",
]
LOCAL_TERMS = ["Morro da Urca", "Pão de Açúcar", "Parque Bondinho", "Praia Vermelha", "Av. Pasteur", "520", "Urca", "Rio de Janeiro"]
CONVERSION_TERMS = ["reservar", "reserva", "TagMe", "WhatsApp", "eventos", "cardápio", "como chegar", "café da manhã"]
EAT_TERMS = ["Veja Rio", "Prazeres da Mesa", "melhor chope", "Heineken", "feijoada premiada", "caipirinha", "Magnífica", "picanha", "desde 2010"]
QUESTION_TERMS = ["onde", "como", "qual", "quanto", "tem", "fica", "horário", "ingresso", "precisa"]

RE_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
RE_DESC = re.compile(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', re.I)
RE_CAN = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', re.I)
RE_H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.I | re.S)
RE_H2 = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.I | re.S)
RE_A = re.compile(r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", re.I | re.S)
RE_JSONLD = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S)
RE_TAG = re.compile(r"<[^>]+>")
RE_HIDDEN = re.compile(r"<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>", re.I | re.S)
RE_SPACE = re.compile(r"\s+")

ACCENT = str.maketrans({"á":"a","à":"a","ã":"a","â":"a","é":"e","ê":"e","í":"i","ó":"o","õ":"o","ô":"o","ú":"u","ç":"c"})

def norm(s: str) -> str:
    return s.lower().translate(ACCENT)

def strip(s: str) -> str:
    return RE_SPACE.sub(" ", RE_TAG.sub(" ", s)).strip()

def visible(html: str) -> str:
    return RE_SPACE.sub(" ", RE_TAG.sub(" ", RE_HIDDEN.sub(" ", html))).strip()

def words(text: str) -> int:
    return len(re.findall(r"\b[\wÀ-ÿ]{2,}\b", text))

def hits(textn: str, terms: list[str]) -> int:
    return sum(1 for t in terms if norm(t) in textn)

def has_any(textn: str, terms: list[str]) -> bool:
    return any(norm(t) in textn for t in terms)

def pages() -> list[Path]:
    return sorted([p for p in ROOT.rglob("*.html") if not any(part in EXCLUDE for part in p.parts)], key=lambda p: p.relative_to(ROOT).as_posix())

def json_blocks(html: str) -> list[Any]:
    out=[]
    for raw in RE_JSONLD.findall(html):
        try: out.append(json.loads(raw.strip()))
        except Exception: out.append({"__parse_error__": raw[:160]})
    return out

def walk(v: Any):
    if isinstance(v, dict):
        yield v
        for x in v.values(): yield from walk(x)
    elif isinstance(v, list):
        for x in v: yield from walk(x)

def types(blocks: list[Any]) -> list[str]:
    out=[]
    for b in blocks:
        for n in walk(b):
            if not isinstance(n, dict): continue
            t=n.get("@type")
            if isinstance(t,str): out.append(t)
            elif isinstance(t,list): out += [str(x) for x in t]
    return out

def faq_count(html: str, blocks: list[Any]) -> int:
    counts=[len(re.findall(r"faq-item|faq-question", html, re.I))]
    for b in blocks:
        for n in walk(b):
            if isinstance(n, dict) and n.get("@type") == "FAQPage" and isinstance(n.get("mainEntity"), list):
                counts.append(len(n["mainEntity"]))
    return max(counts) if counts else 0

def link_counts(html: str) -> tuple[int,int]:
    internal=cta=0
    for href,label in RE_A.findall(html):
        l=norm(strip(label)); h=norm(href)
        if href.startswith("/") or href.endswith(".html") or href.startswith("#") or "embaixadacarioca.com" in href: internal+=1
        if any(x in l or x in h for x in ["reserv", "tagme", "whatsapp", "cardapio", "como chegar", "evento"]): cta+=1
    return internal, cta

@dataclass
class Dim:
    dimension: str
    score: int
    findings: list[str]=field(default_factory=list)
@dataclass
class Result:
    page: str
    status: str
    score: int
    word_count: int
    h1_count: int
    h2_count: int
    faq_count: int
    internal_links: int
    cta_links: int
    jsonld_types: list[str]
    dimensions: list[Dim]

def dim(name: str, penalties: list[tuple[int,str]]) -> Dim:
    return Dim(name, max(0, 100-sum(p for p,_ in penalties)), [m for _,m in penalties])

def audit(path: Path) -> Result:
    html=path.read_text(encoding="utf-8", errors="ignore")
    text=visible(html); textn=norm(text); wc=words(text)
    h1=[strip(x) for x in RE_H1.findall(html) if strip(x)]
    h2=[strip(x) for x in RE_H2.findall(html) if strip(x)]
    blocks=json_blocks(html); ts=types(blocks); fq=faq_count(html, blocks); internal, cta=link_counts(html)
    file=path.name
    utility=file in UTILITY
    dims=[]

    p=[]
    if "#f6efde" in html and "color:#f6efde" in html: p.append((6,"Risco de texto creme em fundo claro."))
    if "#00405a" in html and "background:#00405a" in html and "color:#00405a" in html: p.append((8,"Risco de texto azul em fundo azul."))
    if "opacity:." in html or "opacity: ." in html: p.append((4,"Opacity baixa detectada; validar texto real."))
    if "ec-stabilization-base.css" not in html and "ec-contrast-hotfix.css" not in html: p.append((6,"Sem CSS global de estabilização/contraste."))
    if len(re.findall(r"<style\b", html, re.I)) > 30: p.append((6,"Excesso de blocos style."))
    dims.append(dim("Design", p))

    p=[]
    if len(h1) != 1: p.append((10,f"H1 deveria ser único; encontrado {len(h1)}."))
    if len(h2) < 2 and not utility: p.append((6,"Poucos H2 para boa escaneabilidade."))
    if cta < 1 and not utility: p.append((12,"Sem CTA claro."))
    if internal < 3 and not utility: p.append((6,"Poucos links internos."))
    if "skip-nav" not in html: p.append((3,"Sem skip-nav detectado."))
    dims.append(dim("UX", p))

    p=[]
    if wc < 450 and not utility: p.append((12,f"Conteúdo curto: {wc} palavras."))
    if not has_any(textn,["vista","morro da urca","pao de acucar","carioca"]) and not utility: p.append((8,"Diferencial turístico/carioca pouco claro."))
    if "?" not in text and not has_any(textn, QUESTION_TERMS) and not utility: p.append((5,"Poucas perguntas/respostas explícitas."))
    if has_any(textn,["lorem ipsum","placeholder","em breve"]): p.append((25,"Placeholder detectado."))
    dims.append(dim("Copydesk", p))

    p=[]
    title=RE_TITLE.search(html); desc=RE_DESC.search(html); can=RE_CAN.search(html)
    if not title: p.append((18,"Sem title."))
    else:
        tl=len(strip(title.group(1)))
        if tl<18 or tl>72: p.append((5,f"Title fora da faixa ideal: {tl}."))
    if not desc: p.append((16,"Sem meta description."))
    else:
        dl=len(desc.group(1).strip())
        if dl<70 or dl>180: p.append((5,f"Meta description fora da faixa ideal: {dl}."))
    if not can: p.append((12,"Sem canonical."))
    elif "https://www.embaixadacarioca.com" not in can.group(1): p.append((12,"Canonical fora do domínio oficial."))
    if "hreflang" not in html: p.append((4,"Sem hreflang."))
    dims.append(dim("SEO", p))

    p=[]
    lh=hits(textn, LOCAL_TERMS)
    if lh<4 and not utility: p.append((12,f"Baixa cobertura local/GEO: {lh}/{len(LOCAL_TERMS)}."))
    if not has_any(textn,["como chegar","av pasteur","praia vermelha","bondinho"]) and not utility: p.append((10,"Falta bloco forte de acesso/endereço."))
    if "GeoCoordinates" not in html and "latitude" not in html and not utility: p.append((7,"Sem GeoCoordinates."))
    dims.append(dim("GEO", p))

    p=[]
    if fq<4 and not utility: p.append((14,f"FAQ baixo para AEO: {fq}."))
    if "FAQPage" not in html and fq>0: p.append((8,"FAQ visual sem FAQPage JSON-LD."))
    if not has_any(textn,["onde fica","como chegar","qual o horario","tem restaurante","precisa de ingresso"]) and not utility: p.append((8,"Faltam respostas diretas transacionais."))
    dims.append(dim("AEO", p))

    p=[]
    if hits(textn, PRIORITY_KEYWORDS)==0 and not utility: p.append((10,"Sem cobertura literal das keywords prioritárias AIO."))
    if fq<4 and not utility: p.append((10,"Poucas FAQs para IA."))
    if "VideoObject" not in ts and has_any(textn,["cafe da manha","restaurante morro da urca","experiencia"]): p.append((5,"Sem VideoObject em página de experiência/produto."))
    if "@graph" not in html and "application/ld+json" in html: p.append((3,"Schema sem @graph."))
    dims.append(dim("AIO", p))

    p=[]
    if cta<1 and not utility: p.append((15,"Sem CTA de decisão."))
    if internal<3 and not utility: p.append((6,"Pouca navegação contextual."))
    if not has_any(textn,["preco","horario","endereco","ingresso","reserva","cardapio"]) and not utility: p.append((10,"Faltam dados de decisão rápida."))
    dims.append(dim("SXO", p))

    p=[]
    if hits(textn, CONVERSION_TERMS)<3 and not utility: p.append((10,"Baixa presença de termos de conversão."))
    if not has_any(textn,["premiado","melhor","vista","experiencia","todos os dias","evento"]) and not utility: p.append((8,"Faltam provas/diferenciais comerciais."))
    dims.append(dim("Marketing", p))

    p=[]
    checks={"Receita":["reserva","reservar","evento","cardapio","menu","whatsapp"],"Relevância":["pao de acucar","morro da urca","bondinho","urca","rio de janeiro"],"Decisão":["horario","preco","ingresso","endereco","todos os dias","capacidade"],"Direção":["como chegar","av pasteur","praia vermelha","rota","acesso"]}
    for name,terms in checks.items():
        if not has_any(textn,terms) and not utility: p.append((7,f"R2D2 fraco em {name}."))
    dims.append(dim("R2D2", p))

    p=[]
    if not blocks: p.append((18,"Sem JSON-LD."))
    if any(isinstance(b,dict) and "__parse_error__" in b for b in blocks): p.append((25,"JSON-LD inválido."))
    if not any(t in ts for t in ["Restaurant","LocalBusiness","FoodEstablishment","WebPage","FAQPage"]): p.append((10,"Schema sem tipo útil para local/conteúdo."))
    ag=sum(1 for b in blocks for n in walk(b) if isinstance(n,dict) and "aggregateRating" in n)
    if ag>1: p.append((20,f"Múltiplos aggregateRating: {ag}."))
    dims.append(dim("Schema", p))

    p=[]
    if len(re.findall(r"rel=[\"']preload[\"']", html, re.I))>8: p.append((6,"Preloads em excesso."))
    if len(re.findall(r"<style\b", html, re.I))>30: p.append((8,"Muitos blocos style."))
    if len(re.findall(r"<script\b", html, re.I))>40: p.append((8,"Muitos scripts."))
    if len(re.findall(r"<img\b", html, re.I))>4 and "loading=\"lazy\"" not in html: p.append((4,"Muitas imagens sem lazy loading."))
    dims.append(dim("Performance", p))

    score=round(sum(d.score for d in dims)/len(dims))
    status="PASS" if score>=THRESHOLD and all(d.score>=75 for d in dims) else "FAIL"
    return Result(path.relative_to(ROOT).as_posix(), status, score, wc, len(h1), len(h2), fq, internal, cta, sorted(set(ts)), dims)

def write(results: list[Result]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    min_score=min((r.score for r in results), default=0); avg=round(sum(r.score for r in results)/len(results),1) if results else 0
    status="PASS" if min_score>=THRESHOLD and all(r.status=="PASS" for r in results) else "FAIL"
    JS.write_text(json.dumps({"status":status,"threshold":THRESHOLD,"average_score":avg,"min_score":min_score,"dimensions":DIMENSIONS,"priority_keywords":PRIORITY_KEYWORDS,"results":[asdict(r) for r in results]}, ensure_ascii=False, indent=2), encoding="utf-8")
    with CSV.open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f, fieldnames=["page","status","score","dimension","dimension_score","findings","word_count","h1_count","h2_count","faq_count","internal_links","cta_links","jsonld_types"]); w.writeheader()
        for r in results:
            for d in r.dimensions:
                w.writerow({"page":r.page,"status":r.status,"score":r.score,"dimension":d.dimension,"dimension_score":d.score,"findings":" | ".join(d.findings),"word_count":r.word_count,"h1_count":r.h1_count,"h2_count":r.h2_count,"faq_count":r.faq_count,"internal_links":r.internal_links,"cta_links":r.cta_links,"jsonld_types":" | ".join(r.jsonld_types)})
    bydim={}
    for r in results:
        for d in r.dimensions: bydim.setdefault(d.dimension,[]).append(d.score)
    lines=["# Superholistic Design/UX/SEO/GEO/AIO/SXO Audit","",f"Status geral: **{status}**",f"Score médio: **{avg}**",f"Score mínimo: **{min_score}**",f"Threshold: **{THRESHOLD}**",f"Páginas auditadas: **{len(results)}**","","## Dimensões auditadas"]
    for name in DIMENSIONS:
        vals=bydim.get(name,[]); lines.append(f"- **{name}** — média {round(sum(vals)/len(vals),1) if vals else 0}, mínimo {min(vals) if vals else 0}")
    lines += ["","## Páginas abaixo de 90"]
    low=[r for r in results if r.score<THRESHOLD]
    if low:
        for r in sorted(low,key=lambda x:x.score)[:80]:
            weak=", ".join(f"{d.dimension}:{d.score}" for d in r.dimensions if d.score<90)
            lines.append(f"- `{r.page}` — score {r.score} — {weak}")
    else: lines.append("Nenhuma página abaixo de 90.")
    lines += ["","## Findings por página"]
    for r in sorted(results,key=lambda x:x.score)[:120]:
        fs=[d for d in r.dimensions if d.findings]
        if not fs: continue
        lines.append(f"### `{r.page}` — {r.score}")
        for d in fs:
            lines.append(f"- **{d.dimension} ({d.score})**")
            for item in d.findings[:4]: lines.append(f"  - {item}")
        lines.append("")
    lines += ["## Arquivos gerados", f"- `{MD.relative_to(ROOT)}`", f"- `{CSV.relative_to(ROOT)}`", f"- `{JS.relative_to(ROOT)}`", ""]
    MD.write_text("\n".join(lines), encoding="utf-8")

def main() -> int:
    results=[audit(p) for p in pages()]
    write(results)
    min_score=min((r.score for r in results), default=0); avg=round(sum(r.score for r in results)/len(results),1) if results else 0
    print(f"Superholistic audit: pages={len(results)} avg_score={avg} min_score={min_score}")
    return 0 if min_score>=THRESHOLD and all(r.status=="PASS" for r in results) else 1
if __name__ == "__main__":
    raise SystemExit(main())
