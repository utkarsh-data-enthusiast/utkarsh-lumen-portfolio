"""Local privacy, link, accessibility-smoke and viewport tests. No internet required."""
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import re

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
PAGES=list(DIST.rglob('*.html'))
assert len(PAGES)==19, f'Expected 19 HTML pages, saw {len(PAGES)}'
for p in PAGES:
    doc=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    assert len(doc.select('h1'))==1, (p,'h1')
    for tag in doc.select('[href],[src]'):
        link=tag.get('href') or tag.get('src')
        if not link or link.startswith(('#','http:','https:','mailto:','data:')): continue
        path=(p.parent/link.split('#')[0]).resolve()
        assert path.is_file(),(p,link)
    for a in doc.select('a[target="_blank"]'):
        assert {'noopener','noreferrer'}.issubset(set(a.get('rel',[]))),p
    for value in ['7854918108','utk108@icloud.com','patriotu1008@gmail.com']:
        assert value not in p.read_text(),(p,value)
    assert not doc.select('iframe'),p
    assert not doc.select('[style]'), ('inline style',p)
    assert not doc.select('script:not([src])'),p
assert not re.search(r'\b(fetch\(|sendBeacon\(|localStorage|sessionStorage|XMLHttpRequest|document\.cookie)\b',(DIST/'assets/app.js').read_text())
print('PASS links, 19 pages, no inline style/script, no published personal contact details')

def render(page, path):
    doc=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    for node in doc.select('meta[http-equiv="Content-Security-Policy"],link[rel="stylesheet"],script[src]'):
        node.decompose()
    page.set_content(str(doc), wait_until='load')
    page.add_style_tag(content=(DIST/'assets/style.css').read_text())
    page.add_script_tag(content=(DIST/'assets/app.js').read_text())

with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    for width,height in [(1440,920),(820,1050),(390,844),(320,780)]:
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        render(page,DIST/'index.html')
        page.wait_for_timeout(350)
        print(width,'overflow',page.evaluate('document.documentElement.scrollWidth - innerWidth'),'heading',page.locator('h1').inner_text()[:50], 'errors',errors)
        assert not errors
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),width
        assert page.locator('.site-header').is_visible()
        page.locator('[data-atlas-tab]').nth(1).click()
        assert page.locator('[data-atlas-title]').inner_text() == 'Measure the model.'
        page.locator('[data-skill-button]').nth(2).click()
        assert 'Tools for people' in page.locator('[data-skill-title]').inner_text()
        if width<741:
            page.locator('[data-menu-toggle]').click(); assert page.locator('[data-nav-menu]').is_visible()
            page.locator('[data-menu-toggle]').click()
        if width==1440:
            page.screenshot(path=str(ROOT/'previews'/'desktop-light.png'),full_page=True)
        if width==390:
            page.screenshot(path=str(ROOT/'previews'/'mobile-light.png'),full_page=True)
        render(page,DIST/'projects'/'index.html')
        assert page.locator('[data-project-card]:visible').count()==15
        page.locator('[data-filter="Open source"]').click()
        assert page.locator('[data-project-card]:visible').count()==3
        page.locator('input[data-search]').fill('nova')
        assert page.locator('[data-project-card]:visible').count()==2
        page.locator('input[data-search]').fill('NO SUCH PROJECT')
        assert page.locator('[data-project-card]:visible').count()==0
        page.locator('[data-filter="All"]').click();page.locator('input[data-search]').fill('');
        assert page.locator('[data-project-card]:visible').count()==15
        if width==1440:page.screenshot(path=str(ROOT/'previews'/'project-library.png'),full_page=True)
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
        render(page,DIST/'projects'/'nova-jupyter-bridge.html')
        assert page.locator('h1').inner_text()=='Nova Jupyter Bridge'
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
        if width==1440:page.screenshot(path=str(ROOT/'previews'/'project-detail.png'),full_page=True)
        page.close()
    browser.close()
print('PASS desktop, tablet, mobile and narrow mobile UI interactions')
