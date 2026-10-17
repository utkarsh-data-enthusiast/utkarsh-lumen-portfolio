# Security and privacy notes

This is a static portfolio. It does not provide visitor login, a backend, third-party embeds, or contact forms. No secrets should be placed in the repository, HTML, or frontend JavaScript.

Security controls present in source:
- Local JavaScript/CSS; no external scripts or remote fonts.
- Page-level meta Content Security Policy: default and scripts/styles/images self-only, no connection endpoints or forms. Note that CSP via meta does **not** support all directives and is not equal to a response-header policy.
- noreferrer + noopener on external links.
- No external network calls or visitor storage in site JavaScript.

Before public deployment:
1. Confirm the hosting platform permits the development method and usage (especially Codeberg's updated rules).
2. Configure and verify HTTPS, HSTS, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, and an HTTP `Content-Security-Policy` through the host if supported.
3. Verify the site has no missing assets at its final URL (root or subpath).
4. Confirm any publishable résumé details, job dates, and contact information with the site owner.
5. Verify repository dependencies/branch permissions and enable MFA for accounts.
6. Arrange an external audit before ever claiming the site was independently audited.

Please report any concerns through the owner's public professional profile; no automatic collection channel exists on the website.
