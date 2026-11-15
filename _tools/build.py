#!/usr/bin/env python3
"""Build the static per-language pages of besagoods.com.

Sources live in _src/ and contain every string three times (class="en" /
"sq" / "de"). This script writes one clean page per language:

    /index.html  /essentials.html  /privacy.html         (English, x-default)
    /de/index.html  /de/essentials.html  /de/privacy.html
    /sq/index.html  /sq/essentials.html  /sq/privacy.html
    /de/albanischer-bergtee/index.html                   (German ads landing page)
    /sitemap.xml (+ /besa-sitemap.xml copy)

For each page it removes the other languages, sets <html lang>, the title,
meta description, placeholders and alt text, writes canonical + hreflang +
og:url/locale, turns the EN/SQ/DE buttons into links between the language
versions, and (home page only) writes the JSON-LD.

Folders starting with "_" are not published by GitHub Pages (Jekyll), so
_src/ and _tools/ never go live. Run from the repo root, no dependencies:

    python3 _tools/build.py
"""
import datetime
import html
import json
import os
import re
from html.parser import HTMLParser

SITE = 'https://besagoods.com'
LANGS = ['en', 'de', 'sq']
OG_LOCALE = {'en': 'en_GB', 'de': 'de_DE', 'sq': 'sq_AL'}

# source file, output file name, path as served by GitHub Pages, languages
PAGES = [
    ('index.html', 'index.html', '', LANGS),
    ('essentials.html', 'essentials.html', 'essentials', LANGS),
    ('privacy.html', 'privacy.html', 'privacy', LANGS),
    ('albanischer-bergtee.html', 'albanischer-bergtee/index.html', 'albanischer-bergtee/', ['de']),
]
SITEMAP_PRIORITY = {'': '1.0', 'albanischer-bergtee/': '0.8', 'essentials': '0.7', 'privacy': '0.2'}


def page_url(lang, path):
    return f"{SITE}/{'' if lang == 'en' else lang + '/'}{path}"


def local_href(lang, out_name):
    """Link used inside the site (works on GitHub Pages and a local server)."""
    prefix = '/' if lang == 'en' else f'/{lang}/'
    return prefix if out_name == 'index.html' else prefix + out_name.replace('index.html', '')


# ── tiny lossless HTML tree ─────────────────────────────────────────────────
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta',
        'source', 'track', 'wbr'}


class Node:
    def __init__(self, tag=None, attrs=None, raw='', parent=None):
        self.tag, self.raw, self.parent = tag, raw, parent
        self.attrs = list(attrs or [])
        self.children, self.end, self.dirty = [], '', False

    def get(self, name):
        for k, v in self.attrs:
            if k == name:
                return v
        return None

    def set(self, name, value):
        for i, (k, _) in enumerate(self.attrs):
            if k == name:
                self.attrs[i] = (name, value)
                break
        else:
            self.attrs.append((name, value))
        self.dirty = True

    def drop(self, pred):
        before = len(self.attrs)
        self.attrs = [(k, v) for k, v in self.attrs if not pred(k)]
        self.dirty = self.dirty or len(self.attrs) != before

    def classes(self):
        return (self.get('class') or '').split()


class TreeParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.root = Node('#root')
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.get_starttag_text(), self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.get_starttag_text(), self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is self.root:          # stray end tag: keep it verbatim
            self.cur.children.append(Node(raw=f'</{tag}>'))
            return
        n.end = f'</{tag}>'
        self.cur = n.parent

    def handle_data(self, d): self.cur.children.append(Node(raw=d))
    def handle_entityref(self, name): self.handle_data(f'&{name};')
    def handle_charref(self, name): self.handle_data(f'&#{name};')
    def handle_comment(self, d): self.handle_data(f'<!--{d}-->')
    def handle_decl(self, d): self.handle_data(f'<!{d}>')
    def handle_pi(self, d): self.handle_data(f'<?{d}>')


def start_tag(n):
    if not n.dirty:
        return n.raw
    parts = [n.tag]
    for k, v in n.attrs:
        parts.append(k if v is None else f'{k}="{html.escape(v, quote=True)}"')
    return '<' + ' '.join(parts) + '>'


def render(n):
    if n.tag is None:
        return n.raw
    inner = ''.join(render(c) for c in n.children)
    return inner if n.tag == '#root' else start_tag(n) + inner + n.end


def walk(n):
    yield n
    for c in n.children:
        yield from walk(c)


def find(n, pred):
    return next((x for x in walk(n) if x.tag and pred(x)), None)


# ── per-language transforms ────────────────────────────────────────────────
def strip_other_languages(n, lang):
    others = [l for l in LANGS if l != lang]
    n.children = [c for c in n.children
                  if not (c.tag and any(o in c.classes() for o in others))]
    for c in n.children:
        strip_other_languages(c, lang)


def bake_translated_attributes(root, lang):
    """data-t-xx -> text, data-content-xx -> content, data-ph-xx -> placeholder,
    data-alt-xx -> alt, data-al-xx -> aria-label; then drop all data-*-xx."""
    pat = re.compile(r'^data-(t|content|ph|alt|al)-(en|sq|de)$')
    for n in walk(root):
        if not n.tag or not any(pat.match(k) for k, _ in n.attrs):
            continue
        for kind, target in (('t', None), ('content', 'content'), ('ph', 'placeholder'),
                             ('alt', 'alt'), ('al', 'aria-label')):
            v = n.get(f'data-{kind}-{lang}')
            if v is None:
                v = n.get(f'data-{kind}-en')
            if v is None:
                continue
            if target:
                n.set(target, v)
            else:
                n.children = [Node(raw=html.escape(v, quote=False))]
        n.drop(lambda k: bool(pat.match(k)))


def language_links(root, lang, out_name, langs):
    toggle = find(root, lambda x: 'lang-toggle' in x.classes())
    if not toggle:
        return
    links = []
    for l in ['en', 'sq', 'de']:
        href = local_href(l, out_name) if l in langs else local_href(l, 'index.html')
        cur = ' aria-current="page"' if l == lang else ''
        links.append(f'<a class="lang-btn" href="{href}" hreflang="{l}" lang="{l}"{cur}>{l.upper()}</a>')
    toggle.children = [Node(raw='\n        ' + '\n        '.join(links) + '\n      ')]


def text_of(n):
    return html.unescape(''.join(render(c) for c in n.children)).strip()


def json_ld(lang):
    name = {
        'en': 'Çaj Mali — Albanian mountain tea, 50 g',
        'de': 'Çaj Mali — albanischer Bergtee, 50 g',
        'sq': 'Çaj Mali — çaj mali shqiptar, 50 g',
    }[lang]
    desc = {
        'en': 'Wild-harvested Albanian mountain tea from the Albanian Alps, naturally dried, no additives. '
              'Sourced to order: request it online, we confirm price and shipping by email, '
              'and you pay only once your order is confirmed.',
        'de': 'Wild geernteter albanischer Bergtee aus den albanischen Alpen, natürlich getrocknet, ohne Zusatzstoffe. '
              'Auf Bestellung: online anfragen, wir bestätigen Preis und Versand per E-Mail, '
              'bezahlt wird erst nach der Bestätigung.',
        'sq': 'Çaj mali shqiptar i mbledhur i egër në Alpet Shqiptare, i tharë natyrshëm, pa aditivë. '
              'Sipas porosisë: e kërkoni online, ne konfirmojmë çmimin dhe transportin me email, '
              'dhe paguani vetëm pasi porosia të konfirmohet.',
    }[lang]
    home = page_url(lang, '')
    data = {
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'Organization', '@id': f'{SITE}/#organization', 'name': 'Besa Goods',
             'url': f'{SITE}/', 'email': 'besasonos@gmail.com',
             'address': {'@type': 'PostalAddress', 'addressLocality': 'Madrid', 'addressCountry': 'ES'}},
            {'@type': 'WebSite', '@id': f'{SITE}/#website', 'url': f'{SITE}/', 'name': 'Besa Goods',
             'inLanguage': ['en', 'de', 'sq'], 'publisher': {'@id': f'{SITE}/#organization'}},
            {'@type': 'Product', '@id': f'{home}#caj-mali', 'name': name, 'description': desc,
             'inLanguage': lang, 'sku': 'BGMT-001',
             'brand': {'@type': 'Brand', 'name': 'Besa Goods'},
             'image': f'{SITE}/images/caj-mali-square.jpg',
             # Not purchasable directly: sourced to order, paid after confirmation.
             # BackOrder = can be ordered, not in stock. Price excludes shipping.
             'offers': {'@type': 'Offer', 'url': f'{home}#request', 'price': '12.90',
                        'priceCurrency': 'EUR', 'availability': 'https://schema.org/BackOrder',
                        'itemCondition': 'https://schema.org/NewCondition',
                        'seller': {'@id': f'{SITE}/#organization'}}},
        ],
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=1) + '\n</script>')


# Old URLs used ?lang=sq|de. English pages send those (and visitors who chose a
# language before) to the right language version. Crawlers have no storage, so
# they only ever follow the explicit ?lang= redirect.
REDIRECT_JS = """<script>(function(){try{var q=new URLSearchParams(location.search).get('lang'),s=localStorage.getItem('besa_lang'),l=(q==='de'||q==='sq')?q:(!q&&(s==='de'||s==='sq')?s:null);if(!l)return;var m={'/':'','/index.html':'','/essentials':'essentials.html','/essentials.html':'essentials.html','/privacy':'privacy.html','/privacy.html':'privacy.html'},p=m[location.pathname];if(p===undefined)return;location.replace('/'+l+'/'+p+location.hash);}catch(e){}})();</script>"""


def build_page(src, out_name, path, langs):
    source = open(os.path.join('_src', src), encoding='utf-8').read()
    written = []
    for lang in langs:
        p = TreeParser()
        p.feed(source)
        p.close()
        root = p.root
        strip_other_languages(root, lang)
        bake_translated_attributes(root, lang)
        language_links(root, lang, out_name, langs)
        html_el = find(root, lambda x: x.tag == 'html')
        html_el.set('lang', lang)
        html_el.set('data-fixed-lang', None)
        title_el = find(root, lambda x: x.tag == 'title')
        desc_el = find(root, lambda x: x.tag == 'meta' and x.get('name') == 'description')
        title, desc = text_of(title_el), desc_el.get('content')
        out = render(root)

        # head: drop the runtime language switcher, old canonical/hreflang/og:url
        out = re.sub(r"<script>\(function\(\)\{var L=\['en','sq','de'\].*?</script>\n?", '', out, flags=re.S)
        out = re.sub(r'<link rel="(canonical|alternate)"[^>]*>\n?', '', out)
        out = re.sub(r'<meta property="og:(url|locale|locale:alternate)"[^>]*>\n?', '', out)
        out = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(title), out)
        out = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(desc), out)

        head = [f'<link rel="canonical" href="{page_url(lang, path)}">']
        head += [f'<link rel="alternate" hreflang="{l}" href="{page_url(l, path)}">' for l in langs]
        if 'en' in langs:
            head.append(f'<link rel="alternate" hreflang="x-default" href="{page_url("en", path)}">')
        head.append(f'<meta property="og:url" content="{page_url(lang, path)}">')
        head.append(f'<meta property="og:locale" content="{OG_LOCALE[lang]}">')
        head += [f'<meta property="og:locale:alternate" content="{OG_LOCALE[l]}">' for l in langs if l != lang]
        if lang == 'en' and len(langs) > 1:
            head.insert(0, REDIRECT_JS)
        out = re.sub(r'(<meta name="description"[^>]*>\n)', lambda m: m.group(1) + '\n'.join(head) + '\n', out, count=1)

        if src == 'index.html':
            out = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: json_ld(lang), out, count=1, flags=re.S)

        banner = '<!-- Generated by _tools/build.py from _src/' + src + '. Edit the source, then rebuild. -->\n'
        out = out.replace('<!DOCTYPE html>\n', '<!DOCTYPE html>\n' + banner, 1)
        target = out_name if lang == 'en' else os.path.join(lang, out_name)
        os.makedirs(os.path.dirname(target) or '.', exist_ok=True)
        with open(target, 'w', encoding='utf-8') as f:
            f.write(out)
        written.append((lang, target, title, desc))
    return written


def sitemap():
    today = datetime.date.today().isoformat()
    rows = []
    for src, _, path, langs in PAGES:
        if not os.path.exists(os.path.join('_src', src)):
            continue
        for lang in langs:
            alts = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{page_url(l, path)}"/>' for l in langs)
            if 'en' in langs:
                alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url("en", path)}"/>'
            rows.append(f'  <url>\n    <loc>{page_url(lang, path)}</loc>\n    <lastmod>{today}</lastmod>'
                        f'\n    <priority>{SITEMAP_PRIORITY.get(path, "0.5")}</priority>{alts}\n  </url>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(rows) + '\n</urlset>\n')
    for name in ('sitemap.xml', 'besa-sitemap.xml'):   # old name kept for existing Search Console entry
        with open(name, 'w', encoding='utf-8') as f:
            f.write(xml)
    return len(rows)


if __name__ == '__main__':
    titles = {}
    for src, out_name, path, langs in PAGES:
        if not os.path.exists(os.path.join('_src', src)):
            print('skip (no source yet):', src)
            continue
        for lang, target, title, desc in build_page(src, out_name, path, langs):
            print(f'{target:40} {lang}  {title}')
            if title in titles:
                raise SystemExit(f'Duplicate title on {target} and {titles[title]}')
            titles[title] = target
    print('sitemap urls:', sitemap())
