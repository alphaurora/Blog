from pathlib import Path
import html, json, re, sys
sys.path.insert(0, str(Path(__file__).parent / 'work/python'))
import markdown
import yaml
from datetime import date, datetime
from urllib.parse import quote

ROOT = Path(__file__).parent
OUT = ROOT / 'dist'
OUT.mkdir(exist_ok=True)
config = json.loads((ROOT / 'site.json').read_text())
esc = html.escape
posts = []
for path in (ROOT / 'content').glob('*.md'):
    source = path.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', source, re.S)
    if not match: raise ValueError(f'Missing front matter: {path}')
    meta = yaml.safe_load(match[1])
    if not isinstance(meta, dict): raise ValueError(f'Invalid front matter: {path}')
    draft = meta.get('draft', False)
    if not isinstance(draft, bool): raise ValueError(f'draft must be true or false: {path}')
    if draft: continue
    for key in ['title', 'date', 'category', 'description']:
        if key not in meta: raise ValueError(f'Missing {key}: {path}')
    for key in ['title', 'category', 'description']:
        if not isinstance(meta[key], str) or not meta[key].strip(): raise ValueError(f'Invalid {key}: {path}')
    value = meta['date']
    if isinstance(value, datetime): value = value.date()
    if isinstance(value, date): value = value.isoformat()
    meta['date'] = date.fromisoformat(str(value)).isoformat()
    meta.update(slug=quote(path.stem, safe=''), filename=path.stem, body=markdown.markdown(match[2], extensions=['extra', 'sane_lists']), minutes=max(1, round(len(match[2])/350)))
    posts.append(meta)
posts.sort(key=lambda p: p['date'], reverse=True)

def page(title, description, body, prefix=''):
    favicon="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%231d1d1f'/%3E%3Ctext x='32' y='45' text-anchor='middle' font-family='Arial' font-size='44' fill='white'%3Ea%3C/text%3E%3C/svg%3E"
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · {esc(config['name'])}</title><meta name="description" content="{esc(description)}"><link rel="icon" href="{favicon}" type="image/svg+xml"><script src="{prefix}theme.js"></script><link rel="stylesheet" href="{prefix}style.css"></head><body><a class="skip" href="#main">跳到正文</a><header><nav aria-label="主导航"><a class="brand" href="{prefix}index.html">{esc(config['name'])}<span>Journal</span></a><div class="navlinks"><button type="button" class="theme-toggle" aria-label="切换深色模式" aria-pressed="false">深色</button><a href="{prefix}index.html#articles">文章</a><a href="{prefix}admin/">写作</a><a href="{esc(config['github'])}">GitHub ↗</a></div></nav></header>{body}<footer><span>© 2026 {esc(config['name'])}. 记录，思考，创造。</span><span>Stay curious.</span></footer></body></html>'''

def meta(p, featured=False):
    label = '精选 · ' if featured else ''
    return f'<div class="meta"><span class="tag">{label}{esc(p["category"])}</span><time datetime="{p["date"]}">{p["date"].replace("-", ".")}</time><span>{p["minutes"]} 分钟阅读</span></div>'

feature='<div class="feature"><h2>新的记录，正在酝酿。</h2><p>稍后再来读读吧。</p></div>'
if posts:
    p=posts[0]
    feature=f'<a class="feature" href="posts/{p["slug"]}.html">{meta(p, True)}<h2>{esc(p["title"])}</h2><p>{esc(p["description"])}</p><span class="read">阅读全文 <span aria-hidden="true">↗</span></span></a>'
cards=''.join(f'<a class="post" href="posts/{p["slug"]}.html">{meta(p)}<h3>{esc(p["title"])}</h3><p>{esc(p["description"])}</p><span class="read">继续阅读 <span aria-hidden="true">↗</span></span></a>' for p in posts[1:])
body=f'<main id="main"><section class="intro"><p class="eyebrow">THE PERSONAL JOURNAL</p><h1>{esc(config["title"])}</h1><p>{esc(config["description"])}</p></section><section id="articles" aria-label="文章">{feature}<div class="section-head"><h2>更多记录。</h2><span>{len(posts)} 篇文章</span></div><div class="posts">{cards}</div></section></main>'
(OUT/'index.html').write_text(page('个人博客',config['description'],body),encoding='utf-8')
(OUT/'posts').mkdir(exist_ok=True)
for generated in (OUT/'posts').glob('*.html'):
    generated.unlink()
for p in posts:
    body=f'<main id="main" class="article"><a class="back" href="../index.html#articles">← 全部文章</a><article><div class="article-top">{meta(p)}<h1>{esc(p["title"])}</h1><p class="lede">{esc(p["description"])}</p></div><div class="prose">{p["body"]}</div></article><p class="endnote">写于 {p["date"].replace("-", ".")} · {esc(config["name"])}<br><a class="read" href="../index.html#articles">回到文章列表 →</a></p></main>'
    (OUT/'posts'/f'{p["filename"]}.html').write_text(page(p['title'],p['description'],body,'../'),encoding='utf-8')
print(f'Built {len(posts)} articles and homepage in dist/')
