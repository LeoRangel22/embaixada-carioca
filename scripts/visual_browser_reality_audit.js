#!/usr/bin/env node
/*
  Real browser visual audit — Embaixada Carioca
  Opens the main pages in Chromium, captures screenshots and validates computed styles.
*/
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const REPORT_DIR = path.join(ROOT, '_audit_reports');
const SHOT_DIR = path.join(REPORT_DIR, 'visual_browser_screenshots');
const REPORT_MD = path.join(REPORT_DIR, 'visual_browser_reality_audit_report.md');
const REPORT_JSON = path.join(REPORT_DIR, 'visual_browser_reality_audit_report.json');

const pages = [
  { label: 'index', route: '/index.html' },
  { label: 'cardapio', route: '/cardapio.html' },
  { label: 'almoco', route: '/almoco.html' },
  { label: 'cafe-da-manha', route: '/cafe-da-manha.html' },
  { label: 'como-chegar', route: '/como-chegar.html' },
  { label: 'eventos', route: '/eventos.html' },
  { label: 'guia-do-rio', route: '/guia-do-rio.html' },
];

const viewports = [
  { name: 'desktop', width: 1440, height: 1100 },
  { name: 'mobile', width: 390, height: 844 },
];

function contentType(file) {
  const ext = path.extname(file).toLowerCase();
  return {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.webp': 'image/webp',
    '.ico': 'image/x-icon',
  }[ext] || 'application/octet-stream';
}

function startServer() {
  const server = http.createServer((req, res) => {
    const url = new URL(req.url, 'http://127.0.0.1');
    let safePath = decodeURIComponent(url.pathname);
    if (safePath === '/') safePath = '/index.html';
    safePath = safePath.replace(/\.\./g, '');
    const filePath = path.join(ROOT, safePath);
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
        res.end('Not found');
        return;
      }
      res.writeHead(200, { 'content-type': contentType(filePath) });
      res.end(data);
    });
  });
  return new Promise(resolve => {
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({ server, baseUrl: `http://127.0.0.1:${port}` });
    });
  });
}

function okColor(actual, expected) {
  return String(actual).replace(/\s+/g, '').toLowerCase() === expected.replace(/\s+/g, '').toLowerCase();
}

async function inspectPage(page, route, label, viewportName) {
  const result = await page.evaluate(() => {
    const q = sel => document.querySelector(sel);
    const color = sel => {
      const el = q(sel);
      return el ? getComputedStyle(el).color : null;
    };
    const rect = sel => {
      const el = q(sel);
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return { width: Math.round(r.width), height: Math.round(r.height), top: Math.round(r.top), left: Math.round(r.left) };
    };
    const doc = document.documentElement;
    return {
      title: document.title,
      h1: q('h1') ? q('h1').innerText.trim() : '',
      bodyTextLength: document.body.innerText.trim().length,
      navPresent: !!q('nav.top'),
      heroPresent: !!q('header.hero, header.page-hero, .hero, .page-hero'),
      reserveCtaPresent: Array.from(document.querySelectorAll('a')).some(a => /tagme|reserv/i.test(a.href + ' ' + a.innerText)),
      horizontalOverflowPx: Math.max(0, doc.scrollWidth - doc.clientWidth),
      topNavRect: rect('nav.top'),
      heroRect: rect('header.hero, header.page-hero, .hero, .page-hero'),
      menuNameColor: color('.menu-item-name'),
      menuDescColor: color('.menu-item-desc'),
      menuPriceColor: color('.menu-item-price'),
      menuItemCount: document.querySelectorAll('.menu-item').length,
    };
  });

  const checks = [];
  checks.push(['nav presente', result.navPresent]);
  checks.push(['hero presente', result.heroPresent]);
  checks.push(['h1 presente', !!result.h1]);
  checks.push(['CTA reserva presente', result.reserveCtaPresent]);
  checks.push(['sem overflow horizontal relevante', result.horizontalOverflowPx <= 5]);
  checks.push(['texto visível suficiente', result.bodyTextLength > 500]);

  if (label === 'cardapio') {
    checks.push(['cardápio tem itens', result.menuItemCount > 0]);
    checks.push(['nome prato #335d4a', okColor(result.menuNameColor, 'rgb(51, 93, 74)')]);
    checks.push(['descrição #485156', okColor(result.menuDescColor, 'rgb(72, 81, 86)')]);
    checks.push(['preço #9a6500', okColor(result.menuPriceColor, 'rgb(154, 101, 0)')]);
  }

  return { route, label, viewportName, ...result, checks };
}

(async () => {
  fs.mkdirSync(SHOT_DIR, { recursive: true });
  const { server, baseUrl } = await startServer();
  const browser = await chromium.launch();
  const results = [];

  try {
    for (const vp of viewports) {
      const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: 1 });
      const page = await context.newPage();
      for (const spec of pages) {
        const url = `${baseUrl}${spec.route}`;
        await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
        await page.screenshot({ path: path.join(SHOT_DIR, `${spec.label}-${vp.name}.png`), fullPage: true });
        results.push(await inspectPage(page, spec.route, spec.label, vp.name));
      }
      await context.close();
    }
  } finally {
    await browser.close();
    server.close();
  }

  const failures = [];
  for (const r of results) {
    for (const [name, pass] of r.checks) {
      if (!pass) failures.push(`${r.label} / ${r.viewportName}: ${name}`);
    }
  }

  const lines = [];
  lines.push('# Visual Browser Reality Audit');
  lines.push('');
  lines.push('## Veredito');
  lines.push(`- Páginas auditadas: ${pages.length}`);
  lines.push(`- Viewports: ${viewports.map(v => v.name).join(', ')}`);
  lines.push(`- Status: ${failures.length ? 'FAIL' : 'PASS'}`);
  lines.push(`- Falhas: ${failures.length}`);
  lines.push('');
  lines.push('## Checks por página');
  for (const r of results) {
    lines.push(`\n### ${r.label} — ${r.viewportName}`);
    lines.push(`- H1: ${r.h1 || '(sem h1)'}`);
    lines.push(`- Overflow horizontal: ${r.horizontalOverflowPx}px`);
    if (r.label === 'cardapio') {
      lines.push(`- Nome prato: ${r.menuNameColor}`);
      lines.push(`- Descrição: ${r.menuDescColor}`);
      lines.push(`- Preço: ${r.menuPriceColor}`);
    }
    for (const [name, pass] of r.checks) {
      lines.push(`- ${pass ? 'PASS' : 'FAIL'} — ${name}`);
    }
  }
  lines.push('');
  lines.push('## Screenshots');
  lines.push(`Gerados em: _audit_reports/visual_browser_screenshots/`);
  if (failures.length) {
    lines.push('');
    lines.push('## Falhas');
    failures.forEach(f => lines.push(`- ${f}`));
  }

  fs.writeFileSync(REPORT_MD, lines.join('\n'), 'utf8');
  fs.writeFileSync(REPORT_JSON, JSON.stringify({ failures, results }, null, 2), 'utf8');

  console.log(lines.join('\n'));
  if (failures.length) process.exit(1);
})();
