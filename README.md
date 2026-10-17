# Utkarsh Anand — Lumen Portfolio

A **distinct, light-themed** portfolio website made for Utkarsh Anand. Built as a static site: no frameworks, JavaScript packages, remote fonts, advertising, analytics, form processors, cookies, or APIs.

**Status:** A complete local review build. **Not published or independently audited.** Separate from the existing dark Netlify portfolio, which is not changed by these files.

## What's inside

- Premium light editorial design using warm ivory, deep teal, and pastel accents.
- Responsive homepage with a real, local-only three-mode interactive chart illustration.
- Four-category, keyboard-operable interactive skills view.
- Filterable/searchable collection of 15 project case studies and individual detail pages.
- Direct links to the GitHub profile and both supplied LinkedIn addresses.
- Résumé-informed education and Tata Steel internship summary; internship dates deliberately omitted due to conflicting source résumés.
- Project details distinguish publicly linked repositories from results reported in résumés.
- Privacy page and a custom 404 page.

## The folder structure

```
assets/       CSS, local JavaScript, favicon
site_data.py  project data, public profile links
build.py      Python standard-library-only static generator
dist/         generated website — created by `python3 build.py`
tools/        local tests (optional Playwright + BeautifulSoup)
previews/     review screenshots, not used by the website
```

## Preview

The separate `utkarsh-lumen-portfolio-deploy.zip` archive contains the ready-made website. Unzip it and open `index.html` in Safari. The HTML uses relative links, and all assets are local.

For the source ZIP: unzip, then execute `python3 build.py` from its root folder; this generates `dist`. Open `dist/index.html` or serve `dist` from a local web server. Python 3.10+ is recommended; no external packages are needed to build.

## Edit

- Edit titles, sources, project evidence, and profile URLs in `site_data.py`.
- Edit page templates and illustrations in `build.py`.
- Edit design in `assets/style.css` and behavior in `assets/app.js`.
- Run `python3 build.py` to regenerate `dist`.
- Do not edit generated `dist/` directly; the next build overwrites it.

## Codeberg Pages deployment planning — **not done yet**

Codeberg Pages' current `git-pages` documentation explains two routes: webhooks on a public `pages` branch, or deployment from Forgejo Actions. A user website normally uses a public repository named `pages`, a `pages` branch, and a properly configured Forgejo webhook. Published root address depends on the eventual Codeberg username. See <https://docs.codeberg.org/codeberg-pages/>.

**Policy checkpoint before uploading:** Codeberg changed its policy on projects created or maintained with heavy use of LLMs. This project was substantially AI-assisted; it may be ineligible for Codeberg hosting. Obtain permission or clarification from Codeberg before uploading. Do not misrepresent the development history. If the project is not permitted, use another static host instead. See <https://blog.codeberg.org/protecting-our-floss-commons-from-llms.html>.

If hosting is approved, a dedicated `pages` branch containing the **contents of `dist/` at branch root** can be used with the documented webhook method. A Forgejo Actions workflow would need to be configured separately for automatic builds; nothing in this archive automatically deploys or bypasses Codeberg's rules.

## Privacy and security design

- No visitor contact forms, client-side network requests, tracker scripts, analytics cookies, fingerprinting, or remote dependencies.
- Accessible labels, visible keyboard focus, navigation control, reduced motion support, descriptive alt text, and responsive layouts down to 320 CSS px.
- HTML declares a restrictive `Content-Security-Policy` through a `<meta>` element; HTTP security headers must be configured at the real host. A meta CSP is not a substitute for a complete HTTP header policy.
- External profile links open with `rel="noopener noreferrer"`.
- Static-only structure reduces attack surface but does not guarantee the host does not log IP addresses. There is no third-party website audit.
- All illustrations and charts are decorative illustrations, **not live business metrics**.
- Personal phone numbers and email addresses that appear in supplied PDFs have **not** been embedded in site files.

## Testing

Generated page/asset integrity and local in-memory browser checks have been run. The visual browser test uses in-memory HTML+CSS+JS because this environment blocks local URL navigation. Deployment-specific behavior, host headers, Codeberg Pages compatibility, and independent security validation must be checked after publishing.

Optional tests, if Playwright, Chromium, and BeautifulSoup are available:

```
python3 tools/test_site.py
```

## Scope of factual claims

The code uses supplied résumé details and certain GitHub repository links already verified earlier in the conversation. Figures marked as résumé reported are **not independently reproduced**. Different résumé versions disagree on Tata Steel internship dates, so those dates are omitted. No assumption is made about current employment, both LinkedIn pages' ownership beyond the user's supplied links, or the production-readiness of open-source extensions.

## License

MIT license for original website code. Third-party names, marks, datasets, and project material linked externally remain with their respective owners. Independent third-party audits have **not** been performed.
