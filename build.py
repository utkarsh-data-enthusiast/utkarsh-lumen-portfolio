
#!/usr/bin/env python3
"""Build a light-first, Codeberg-ready static portfolio using Python's standard library."""

from pathlib import Path
from html import escape
from urllib.parse import urlparse
import shutil
import re

from site_data import PROJECTS, SOCIAL


ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'

GITHUB = SOCIAL[0][1]
LINKEDIN_A = SOCIAL[1][1]
LINKEDIN_B = SOCIAL[2][1]

THEMES = {
	'lime': 'theme-green',
	'green': 'theme-green',
	'purple': 'theme-purple',
	'blue': 'theme-sky',
	'orange': 'theme-orange'
}


def esc(v):
	return escape(str(v), quote=True)


def relative(prefix, tail):
	return prefix + tail


def svg_art(project, label=''):
	group = project['group']
	slug = project['slug']

	# Abstract editorial illustrations are generated locally,
	# without third-party assets.

	if group == 'Open source':
		inner = '''<rect x="77" y="18" width="278" height="175" rx="18" fill="#fffefa" stroke="#285952" stroke-width="2"/><path d="M78 56 H355" stroke="#285952" stroke-width="1.5"/><circle cx="100" cy="37" r="5" fill="#eea585"/><circle cx="118" cy="37" r="5" fill="#cbe9a6"/><circle cx="136" cy="37" r="5" fill="#afd8ed"/><path d="M112 93 L92 111 L112 129 M139 93 L159 111 L139 129" fill="none" stroke="#0d7867" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><path d="M192 93 H308 M192 111 H266 M192 130 H290 M95 158 H190 M201 158 H271" fill="none" stroke="#a8beb2" stroke-width="6" stroke-linecap="round"/><circle cx="318" cy="157" r="26" fill="#d1f09f" stroke="#285952" stroke-width="1.6"/><path d="M305 158 L315 168 L332 146" fill="none" stroke="#285952" stroke-width="4" stroke-linecap="round"/>'''

	elif group == 'Machine learning':
		inner = '''<rect x="64" y="22" width="302" height="177" rx="19" fill="#fffefa" stroke="#285952" stroke-width="1.7"/><path d="M97 167 H333 M97 167 V51" stroke="#9abdb5" stroke-width="2"/><path d="M101 145 C128 140 139 117 160 131 S214 98 237 107 S294 53 329 59" stroke="#087a67" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M100 156 C156 151 174 122 214 136 S281 114 332 107" stroke="#e6a47d" stroke-width="3.6" fill="none" stroke-dasharray="8 9"/><circle cx="329" cy="59" r="10" fill="#b7e68d" stroke="#285952" stroke-width="2"/>'''

	elif group == 'Natural language':
		inner = '''<rect x="79" y="22" width="273" height="175" rx="19" fill="#fffefa" stroke="#285952" stroke-width="1.8"/><rect x="105" y="47" width="66" height="15" rx="7" fill="#cfeab2"/><path d="M105 84 H322 M105 106 H300 M105 128 H320 M105 150 H261" stroke="#aec9bd" stroke-width="9" stroke-linecap="round"/><rect x="183" y="73" width="79" height="20" rx="7" fill="#e2d6f6" opacity=".9"/><rect x="126" y="117" width="64" height="19" rx="6" fill="#c1e7f2" opacity=".8"/><circle cx="315" cy="159" r="27" fill="#f5e5a5" stroke="#285952" stroke-width="1.7"/><path d="M303 159 L312 168 L329 149" fill="none" stroke="#285952" stroke-width="4"/>'''

	elif group == 'Deep learning':
		inner = '''<g fill="none" stroke="#65978f" stroke-width="2"> <path d="M101 45L203 64L310 36 M101 45L203 125L310 36 M101 112L203 64L310 101 M101 112L203 125L310 101 M101 174L203 64L310 169 M101 174L203 125L310 169"/></g><g stroke="#285952" stroke-width="2"><circle cx="101" cy="45" r="21" fill="#fffefa"/><circle cx="101" cy="112" r="21" fill="#fffefa"/><circle cx="101" cy="174" r="21" fill="#fffefa"/><circle cx="203" cy="64" r="24" fill="#b7e68d"/><circle cx="203" cy="125" r="24" fill="#c1e7f2"/><circle cx="310" cy="36" r="21" fill="#fffefa"/><circle cx="310" cy="101" r="21" fill="#fffefa"/><circle cx="310" cy="169" r="21" fill="#fffefa"/></g>'''

	else:
		inner = '''<rect x="75" y="21" width="280" height="175" rx="18" fill="#fffefa" stroke="#285952" stroke-width="1.7"/><path d="M111 166 H320" stroke="#8db7ab" stroke-width="2"/><rect x="116" y="97" width="33" height="69" rx="5" fill="#a6d8d2"/><rect x="165" y="66" width="33" height="100" rx="5" fill="#b6e48f"/><rect x="214" y="117" width="33" height="49" rx="5" fill="#f6caa7"/><rect x="263" y="46" width="33" height="120" rx="5" fill="#b9afe9"/><path d="M110 71 C146 29 192 74 239 38 S297 37 315 32" fill="none" stroke="#087a67" stroke-width="4" stroke-linecap="round"/><circle cx="315" cy="32" r="7" fill="#087a67"/>'''

	return f'<svg viewBox="0 0 430 219" role="img" aria-label="Abstract illustration representing {esc(project["kind"])}"><circle cx="210" cy="115" r="102" fill="#ffffff" opacity=".27"/><circle cx="60" cy="30" r="7" fill="#285952" opacity=".38"/>{inner}<path d="M30 185 l20 -17 m-20 0 l20 17" stroke="#285952" stroke-width="2" fill="none" opacity=".5"/></svg>'


def head(title, description, prefix=''):
	# Relative URLs support the Codeberg root and subdirectories.
	# style.css provides the light theme.
	# theme.css adds the optional dark theme.

	return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="referrer" content="strict-origin-when-cross-origin"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"><meta name="description" content="{esc(description)}"><meta name="color-scheme" content="light dark"><meta name="theme-color" content="#fafaf5"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:type" content="website"><link rel="icon" href="{prefix}assets/icon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/style.css"><link rel="stylesheet" href="{prefix}assets/theme.css"><script defer src="{prefix}assets/app.js"></script><title>{esc(title)}</title></head><body><a class="skip" href="#main">Skip to content</a>'''


def header(prefix=''):
	return f'''<header class="site-header"><div class="container nav"><a class="brand" href="{prefix}index.html" aria-label="Utkarsh Anand — Home"><span class="brand-icon" aria-hidden="true">UA<span class="brand-dot">.</span></span><span><span class="brand-name">Utkarsh Anand</span><span class="brand-label">Data · AI · Open source</span></span></a><nav class="nav-menu" id="primary-navigation" data-nav-menu aria-label="Primary navigation"><a href="{prefix}index.html#work">Selected work</a><a href="{prefix}projects/index.html">All projects</a><a href="{prefix}index.html#expertise">Expertise</a><a href="{prefix}index.html#about">About</a><a href="{prefix}index.html#connect">Connect</a></nav><a class="nav-cta" href="{prefix}projects/index.html">Explore projects <span aria-hidden="true">↗</span></a><button type="button" class="theme-toggle" data-theme-toggle aria-label="Switch to dark theme" aria-pressed="false"><span class="theme-icon" data-theme-icon aria-hidden="true">☾</span><span class="theme-label" data-theme-label>Dark</span></button><button type="button" class="hamburger" aria-controls="primary-navigation" aria-expanded="false" data-menu-toggle>Menu ☰</button></div></header>'''


def footer(prefix=''):
	return f'''<footer class="footer"><div class="container footer-inner"><span>© 2026 Utkarsh Anand · Designed with intention.</span><span><a href="{prefix}privacy.html">Privacy &amp; Security</a> &nbsp; · &nbsp; <a href="{GITHUB}" target="_blank" rel="noopener noreferrer">GitHub ↗</a> &nbsp; · &nbsp; No cookies. No tracking.</span></div></footer></body></html>'''


def card(project, prefix='', featured=False):
	theme = THEMES.get(project['tone'], 'theme-green')
	url = prefix + 'projects/' + project['slug'] + '.html'

	tags = ''.join(
		f'<span class="tag">{esc(t)}</span>'
		for t in project['stack'][:4]
	)

	search = esc(' '.join((
		project['title'],
		project['lead'],
		project['group'],
		project['kind'],
		' '.join(project['stack'])
	))).lower()

	evidence = (
		'Code available'
		if project['repo']
		else 'Résumé case study'
	)

	return f'''<article class="feature-card reveal" data-project-card data-group="{esc(project['group'])}" data-search="{search}"><a href="{url}" aria-label="Read case study: {esc(project['title'])}"><div class="feature-visual {theme}">{svg_art(project)}</div></a><div class="feature-copy"><div class="card-meta"><span>{esc(project['group'])} · {esc(project['kind'])}</span><span class="number">{esc(project['number'])}</span></div><h3><a href="{url}">{esc(project['title'])}</a></h3><p>{esc(project['lead'])}</p><div class="tags">{tags}</div><a class="link-line" href="{url}">Read the case study <span aria-hidden="true">↗</span></a></div></article>'''


ATLAS = '''<div class="hero-art"><div class="art-halo" aria-hidden="true"></div><div class="side-note" aria-hidden="true">Eureka!</div><div class="atlas-card" data-atlas><div class="atlas-card-header"><span class="atlas-brand">THE CURIOSITY LAB / 001</span><span class="atlas-live"><i aria-hidden="true"></i> INTERACTIVE EXPLORER</span></div><div class="atlas-body"><span class="atlas-kicker" data-atlas-kicker>01 / DATA EXPLORATION</span><h2 class="atlas-title" data-atlas-title>Find the signal.</h2><p class="atlas-description" aria-live="polite" data-atlas-desc>From raw data to useful patterns: cleaned, measured, explained.</p><svg class="atlas-svg" viewBox="0 0 390 220" role="img" aria-label="Stylized sample trend chart illustrating three areas of work; not live or project data"><defs><pattern id="atlas-grid" width="34" height="34" patternUnits="userSpaceOnUse"><path d="M34 0H0V34" fill="none" stroke="#cfdfd3" stroke-width="1"/></pattern></defs><rect x="0" y="0" width="390" height="220" fill="url(#atlas-grid)" opacity=".85"/><g class="atlas-shape"><path d="M24 194 C73 174 93 141 127 150 S198 90 234 101 S314 71 365 42 L365 217 L24 217Z" fill="#c0e9c9" opacity=".35"/><path data-atlas-path d="M24 194 C73 174 93 141 127 150 S198 90 234 101 S314 71 365 42" fill="none" stroke="#087a67" stroke-width="5" stroke-linecap="round"/><circle cx="365" cy="42" r="10" fill="#ffe1ae" stroke="#087a67" stroke-width="2"/><path d="M0 198H390" stroke="#789c8d" stroke-width="1" stroke-dasharray="3 5"/></g></svg></div><div class="atlas-controls" role="group" aria-label="Explore types of work"><button type="button" class="atlas-tab" aria-pressed="true" data-atlas-tab>01 Data</button><button type="button" class="atlas-tab" aria-pressed="false" data-atlas-tab>02 Models</button><button type="button" class="atlas-tab" aria-pressed="false" data-atlas-tab>03 Tools</button></div></div><div class="atlas-tag" aria-hidden="true">Ideas → useful things</div></div>'''


def homepage():
	featured = [
		p for p in PROJECTS
		if p['slug'] in [
			'nova-jupyter-bridge',
			'customer-churn',
			'kpmg-customer-analytics',
			'cifar10-classification'
		]
	]

	featured_order = [
		'nova-jupyter-bridge',
		'customer-churn',
		'kpmg-customer-analytics',
		'cifar10-classification'
	]

	featured.sort(
		key=lambda p: featured_order.index(p['slug'])
	)

	cards = ''.join(card(p) for p in featured)

	return (
		head(
			'Utkarsh Anand · Data, AI & Open Source',
			'An independently styled, project-first portfolio exploring data science, machine learning and open-source developer tools.'
		)
		+ header()
		+ f'''<main id="main"><section class="hero"><div class="container hero-grid"><div><span class="eyebrow">Hello, I'm Utkarsh · Curious by nature</span><h1 class="hero-headline">Turning <em>questions</em> into clarity.</h1><p class="hero-copy">I work across <strong>data, machine learning and open-source software</strong>—turning complex problems into insights, experiments, and tools worth sharing.</p><div class="hero-buttons"><a class="btn btn-primary" href="#work">Explore my work <span aria-hidden="true">↗</span></a><a class="btn btn-light" href="#connect">Let's connect <span aria-hidden="true">↗</span></a></div><p class="hero-footnote"><span class="line" aria-hidden="true"></span> Project-led. Evidence-aware. Open to good questions.</p></div>{ATLAS}</div></section><div class="ticker"><div class="ticker-inner"><span>Data science</span><b>✳</b><span>Machine learning</span><b>✳</b><span>Developer tools</span><b>✳</b><span>Open source</span><b>✳</b><span>Designing for clarity</span></div></div><section class="section white-section" id="work"><div class="container"><div class="section-heading reveal"><div><span class="eyebrow">01 / A selection of work</span><h2 class="section-title">Proof is in<br>the <em>projects.</em></h2></div><p class="section-description">No vague buzzwords. Explore the problem, the approach, and the result behind each project.</p></div><div class="feature-grid">{cards}</div><div class="explore-band reveal"><div><strong>There's more beneath the surface.</strong><p>Explore all {len(PROJECTS)} case studies, from notebooks and NLP to open-source developer tools.</p></div><a class="btn" href="projects/index.html">Open project library <span aria-hidden="true">↗</span></a></div></div></section><section class="section" id="expertise"><div class="container"><div class="section-heading reveal"><div><span class="eyebrow">02 / How I think & build</span><h2 class="section-title">The toolkit<br>behind the <em>thinking.</em></h2></div><p class="section-description">Explore how the different areas of my work connect. Select a discipline to see the tools and techniques.</p></div><div class="skills-panel" data-skill-switcher><div class="skills-rail" role="tablist" aria-label="Skill disciplines"><button class="skill-selector" role="tab" aria-selected="true" tabindex="0" data-skill-button>01 · Data & analytics <span>↗</span></button><button class="skill-selector" role="tab" aria-selected="false" tabindex="-1" data-skill-button>02 · Machine intelligence <span>↗</span></button><button class="skill-selector" role="tab" aria-selected="false" tabindex="-1" data-skill-button>03 · Building tools <span>↗</span></button><button class="skill-selector" role="tab" aria-selected="false" tabindex="-1" data-skill-button>04 · Ways of working <span>↗</span></button></div><div class="skills-display" role="tabpanel"><span class="small-label">Selected discipline</span><h3 data-skill-title>Exploring and explaining data</h3><p data-skill-description>Structured analysis, decision-focused visualizations, and reproducible data workflows.</p><div class="skills-cloud" data-skill-cloud><span class="skill-chip">Python</span><span class="skill-chip">Pandas</span><span class="skill-chip">NumPy</span><span class="skill-chip">SQL / MySQL</span><span class="skill-chip">Power BI</span><span class="skill-chip">DAX</span><span class="skill-chip">Excel</span><span class="skill-chip">ETL</span><span class="skill-chip">Data cleaning</span></div></div></div><p class="skills-foot">These are areas of experience, not fabricated proficiency scores.</p><div class="impact-strip reveal"><div><div class="impact-value">{len(PROJECTS):02d}</div><p class="impact-desc">Curated case studies covering analysis, modelling, and development.</p></div><div><div class="impact-value">03</div><p class="impact-desc">Highlighted open-source developer-tool projects.</p></div><div><div class="impact-value">01</div><p class="impact-desc">Idea that ties them together: make complex things understandable.</p></div></div></div></section><section class="section white-section" id="about"><div class="container"><div class="about-columns"><div class="reveal"><span class="eyebrow">03 / A little about me</span><h2 class="about-pitch">An analytical mind.<br>An <em>open-source</em> spirit.</h2><p class="about-text">I'm Utkarsh Anand, a computer science graduate working at the intersection of data and practical software. My interests include analytics, machine learning, dashboards, local-first notebook tooling, and thoughtful developer experiences.</p><p class="about-text">I value reproducible work, transparent results, good documentation, and asking the right questions before choosing a technology.</p><a class="link-line" href="projects/index.html">Browse my complete work <span aria-hidden="true">↗</span></a></div><div class="journey reveal"><div class="journey-item"><div class="journey-year">2025</div><div><h3>B.Tech · Computer Science & Engineering</h3><p>Kalinga Institute of Industrial Technology (KIIT), Bhubaneswar.</p></div></div><div class="journey-item"><div class="journey-year">2025</div><div><h3>Data Science with AI</h3><p>Professional certification training through Internshala Trainings / Scholiverse Educare.</p></div></div><div class="journey-item"><div class="journey-year">Experience</div><div><h3>Tata Steel · Data / Business Analyst internship</h3><p>Python-based log analysis, cleaning, reporting automation, and visualizations. Dates intentionally omitted pending résumé reconciliation.</p></div></div><div class="journey-item"><div class="journey-year">Ongoing</div><div><h3>Independent open-source projects</h3><p>Developing and documenting notebook and Python debugging workflows for Nova and JupyterLab.</p></div></div></div></div></div></section><section class="section connect" id="connect"><div class="container connect-grid"><div><span class="eyebrow">04 / Good things start with a conversation</span><h2>Have a question?<br><em>Let's talk.</em></h2><p>Connect through my public professional profiles. This website doesn't collect visitor information or submit contact forms.</p></div><div class="socials"><a class="social-row" href="{GITHUB}" target="_blank" rel="noopener noreferrer">GitHub · View source and projects <span aria-hidden="true">↗</span></a><a class="social-row" href="{LINKEDIN_A}" target="_blank" rel="noopener noreferrer">LinkedIn · Data Enthusiast <span aria-hidden="true">↗</span></a><a class="social-row" href="{LINKEDIN_B}" target="_blank" rel="noopener noreferrer">LinkedIn · Data Scientist <span aria-hidden="true">↗</span></a></div></div></section></main>'''
		+ footer()
	)


def allprojects():
	groups = [
		'All',
		'Open source',
		'Machine learning',
		'Analytics & BI',
		'Natural language',
		'Deep learning'
	]

	buttons = ''.join(
		f'<button class="filter-btn" type="button" data-filter="{esc(g)}" aria-pressed="{str(g == "All").lower()}">{esc(g)}</button>'
		for g in groups
	)

	return (
		head(
			'All Projects · Utkarsh Anand',
			'Search and filter 15 original project case studies and open-source work.',
			'../'
		)
		+ header('../')
		+ f'''<main id="main"><section class="page-hero"><div class="container"><span class="eyebrow">Project atlas / {len(PROJECTS)} pieces of work</span><h1>Ideas into <em>action.</em></h1><p>Open-source extensions, machine learning explorations, analytical dashboards, and stories in data. Browse them by discipline—or search for a tool or topic.</p></div></section><section class="container" data-project-library><div class="library-tools"><div class="filters" role="group" aria-label="Filter by discipline">{buttons}</div><label class="search"><span aria-hidden="true">⌕</span><span class="small-label" class="sr-only">Search projects</span><input type="search" data-search placeholder="Search projects..." aria-label="Search projects" autocomplete="off"></label></div><p class="count-line" data-result-count aria-live="polite">{len(PROJECTS)} projects shown</p><div class="project-grid">{''.join(card(p, '../') for p in PROJECTS)}<div class="empty-state" data-empty><h3>No matching projects.</h3><p>Try another term or choose a different category.</p></div></div></section></main>'''
		+ footer('../')
	)


def project_page(project, index):
	prefix = '../'
	theme = THEMES.get(project['tone'], 'theme-green')
	next_project = PROJECTS[(index + 1) % len(PROJECTS)]

	stack = ', '.join(project['stack'][:5])

	evidence = (
		'Public repository linked'
		if project['repo']
		else 'Résumé-documented project'
	)

	repo_action = (
		f'<a class="btn btn-primary" href="{esc(project["repo"])}" target="_blank" rel="noopener noreferrer">View source on GitHub ↗</a>'
		if project['repo']
		else ''
	)

	return (
		head(
			f'{project["title"]} · Utkarsh Anand',
			project['lead'],
			prefix
		)
		+ header(prefix)
		+ f'''<main id="main"><div class="container"><div class="case-top"><div><span class="eyebrow">{esc(project['group'])} / {esc(project['kind'])}</span><h1>{esc(project['title'])}</h1><p class="deck">{esc(project['lead'])}</p><div class="hero-buttons"><a class="btn btn-light" href="../projects/index.html">← All projects</a>{repo_action}</div></div><div class="case-visual {theme}">{svg_art(project)}</div></div><div class="case-baseline"><div><small>Category</small><span>{esc(project['kind'])}</span></div><div><small>Project focus</small><span>{esc(project['metric'])} · {esc(project['metriclabel'])}</span></div><div><small>Evidence</small><span>{esc(evidence)}</span></div></div><div class="case-body"><div><span class="eyebrow">01 / What it's about</span><h2>Understanding the problem.</h2><p>{esc(project['description'])}</p><h2>What came out of it?</h2><p>{esc(project['result'])}</p><div class="source-note"><strong>Evidence & scope.</strong><br>{esc(project['source'])} The description presents a portfolio case study, not an independently audited model or production system.</div></div><div><span class="eyebrow">02 / Inside the work</span><h2>Approach & tools.</h2><ol>{''.join(f'<li>{esc(a)}</li>' for a in project['approach'])}</ol><div class="tags">{''.join(f'<span class="tag">{esc(x)}</span>' for x in project['stack'])}</div></div></div><div class="next-work"><span class="eyebrow">More to discover</span><a href="{next_project['slug']}.html">{esc(next_project['title'])}<span aria-hidden="true">↗</span></a></div></div></main>'''
		+ footer(prefix)
	)


def privacy():
	return (
		head(
			'Privacy & Security · Utkarsh Anand',
			'A clear explanation of this portfolio website’s privacy practices and security measures.'
		)
		+ header()
		+ '''<main id="main"><section class="page-hero"><div class="container"><span class="eyebrow">Privacy &amp; Security</span><h1>Built with <em>care.</em></h1><p>No analytics, advertising pixels, contact forms, newsletter widgets, or third-party fonts. Just the work.</p></div></section><section class="container privacy-content"><h2>What this website collects</h2><p>The website’s own code does not intentionally collect personal information from visitors. It contains no tracking cookies, analytics scripts, browser fingerprinting, or forms. Most interactive controls operate entirely inside your browser without retaining information. The theme switch stores only your light/dark preference locally in your browser, when browser storage is available. This preference is not transmitted by the website code.</p><h2>What the hosting provider may process</h2><p>The server that hosts this website may see IP addresses, URLs requested, and technical request details to deliver pages and operate its infrastructure. Hosting-provider policies and logging settings are separate from this website’s code. Public hosting is not the same as complete anonymity.</p><h2>External links</h2><p>Links to GitHub and LinkedIn take you to third-party services. Their own data practices apply once you visit them. These external profiles are not embedded into this website.</p><h2>Security measures and limitations</h2><p>This is a static site with no visitor accounts, database, or contact form. The site declares a restrictive browser Content Security Policy and uses local files for JavaScript, CSS, fonts, and illustrations. HTTPS and additional security response headers depend on the hosting provider and must be verified on the published domain. The website has not received an independent third-party security audit.</p><h2>Changes</h2><p>This page describes the current source. It should be reviewed when adding integrations or changing hosts.</p><p><a class="link-line" href="index.html">← Back to portfolio</a></p></section></main>'''
		+ footer()
	)


def build():
	if DIST.exists():
		shutil.rmtree(DIST)

	DIST.mkdir()
	shutil.copytree(ROOT / 'assets', DIST / 'assets')

	(DIST / 'projects').mkdir()

	(DIST / 'index.html').write_text(
		homepage(),
		encoding='utf-8'
	)

	(DIST / 'projects' / 'index.html').write_text(
		allprojects(),
		encoding='utf-8'
	)

	for i, p in enumerate(PROJECTS):
		(DIST / 'projects' / f'{p["slug"]}.html').write_text(
			project_page(p, i),
			encoding='utf-8'
		)

	(DIST / 'privacy.html').write_text(
		privacy(),
		encoding='utf-8'
	)

	(DIST / 'robots.txt').write_text(
		'User-agent: *\nAllow: /\n',
		encoding='utf-8'
	)

	(DIST / '404.html').write_text(
		head(
			'Not found · Utkarsh Anand',
			'This page does not exist.'
		)
		+ header()
		+ '''<main id="main"><section class="page-hero"><div class="container"><span class="eyebrow">404 / Lost a thread?</span><h1>Not this <em>page.</em></h1><p>The page you requested wasn't found. Here's a safe way back.</p><a class="btn btn-primary" href="index.html">Return home ↗</a></div></section></main>'''
		+ footer(),
		encoding='utf-8'
	)

	print(
		f'Built {len(list(DIST.rglob("*.html")))} HTML pages at {DIST}'
	)


if __name__ == '__main__':
	build()
