"""Read-only regressions for home visit CTAs and factual hero content.

Run: python scripts/test_home_visit_experience.py
Layout screenshots and interaction checks must complement these source checks.
"""
import json
import re
import unittest
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
HOMES = {
    'index.html': ('/cardapio.html', '/como-chegar.html'),
    'en/index.html': ('/en/cardapio.html', '/en/how-to-get-there.html'),
    'es/index.html': ('/es/cardapio.html', '/es/como-llegar.html'),
}

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs))

class HomeVisitTest(unittest.TestCase):
    def test_homes(self):
        for file, (menu, directions) in HOMES.items():
            with self.subTest(page=file):
                source = (ROOT / file).read_text(encoding='utf-8')
                hero = re.search(r'<header class="hero ec-home-flow"[\s\S]*?</header>', source).group()
                self.assertNotIn('hero-logo', hero)
                self.assertNotIn('sunset-time', source)
                self.assertNotRegex(hero, r'17h44|17:44|5:44 PM|Math.sin')
                self.assertIn('Academia da Cachaça', hero)
                self.assertIn('2017', hero)
                self.assertIn('2025/2026', hero)
                self.assertNotRegex(source, r'<div[^>]+class="wa-preview"')
                parser = Links(); parser.feed(hero)
                hrefs = [a.get('href') for a in parser.links]
                self.assertIn(menu, hrefs)
                self.assertIn(directions, hrefs)
                self.assertTrue((ROOT / menu.lstrip('/')).is_file())
                self.assertTrue((ROOT / directions.lstrip('/')).is_file())
                self.assertIn('https://go.tagme.com.br/embaixadacarioca', hrefs)
                self.assertIn('id="wa-btn"', source)
                for raw in re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>([\s\S]*?)</script>', source):
                    json.loads(raw)

if __name__ == '__main__':
    unittest.main()
