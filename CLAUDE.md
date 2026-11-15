# Besa Goods — besagoods.com

Static site, no build step, no framework, no package.json. HTML pages with
page-specific inline CSS/JS plus two shared files in `assets/`. Hosted on
GitHub Pages.

Sells Albanian mountain tea (Çaj Mali) on a **request-first** basis and
recommends teaware / Albanian coffee accessories through Amazon affiliate
links. Audience: Albanian diaspora and tourists, mainly UK and Germany.
Business base: Madrid.

## Rules for working here

- **`main` deploys live** (GitHub Pages, branch `main`, path `/`). Never commit to
  `main` directly; work on a branch and merge via PR.
- Never commit secrets. The Stripe `pk_live_…` publishable key and the Formspree
  form ID in the HTML are public by design; secret keys (`sk_…`, webhook
  secrets, API tokens) must never appear in this repo.
- Do not change prices, product claims, shipping terms or availability wording
  without the owner's approval. Do not add social-proof numbers, ratings or
  testimonials that are not real.
- Keep the visual design: tokens in `assets/besa.css` `:root`, Poppins, the
  forest-green / bark / gold palette.
- Every user-facing string needs EN, SQ and DE versions.

## File structure

| File | What it is |
|---|---|
| `index.html` | Home: header, hero, trust bar, shop grid with category filters (`#shop`), how ordering works (`#how`), the two teas (`#teas`), origin, **tea request form** (`#request`), about / shipping & returns / contact, sticky mobile CTA, footer. |
| `essentials.html` | Teapots + coffee tools (Amazon), brewing guide, tea CTA. Served at `/essentials`. |
| `privacy.html` | Privacy policy + cookie table, EN/SQ/DE in one page. Served at `/privacy`. |
| `request-thank-you.html`, `-sq`, `-de` | Shown after a tea request. Fire **Lead** events. `noindex`. |
| `thank-you.html` / `thank-you-de.html` | Stripe purchase success pages. Fire the Google Ads **Purchase** conversion when `?session_id=` is present. Not linked anywhere now; kept for when Stripe checkout or payment links redirect there. Do not reuse for requests. |
| `assets/besa.css` | Shared tokens, header, buttons, product cards, footer, cookie banner, language visibility rules. |
| `assets/besa.js` | Language switching, cookie consent, Google Ads / Meta loading, `besa.trackLead()`. **All tag IDs live in its `CONFIG` block.** |
| `images/` | Optimised JPEGs used by the site. The original PNGs in the repo root are no longer referenced and can be deleted once nothing external links to them. |
| `besa-sitemap.xml` | Sitemap with hreflang alternates. |
| `CNAME`, `google490ef79068abc80c.html` | Custom domain; Search Console verification (keep). |

## Languages (EN / SQ / DE)

- Every translated string exists as sibling elements with class `en`, `sq`,
  `de`. CSS in `besa.css` shows only the one matching `<html lang>`.
- An inline script at the top of `<head>` picks the language before paint:
  `?lang=` → `localStorage['besa_lang']` → browser language → `en`.
- `besa.js` then: sets `aria-pressed` on `[data-set-lang]` buttons, rewrites
  the URL to `?lang=xx` (English has no param), updates `<link rel=canonical>`
  (from `data-base`), and swaps attributes from `data-t-*` (text, used for
  `<title>` and `<option>`), `data-content-*` (meta description), `data-ph-*`
  (placeholders), `data-alt-*` (img alt), `data-al-*` (aria-label).
- If a block lacks a translation, its `.en` sibling is shown as a fallback.
- Pages with one fixed language use `<html lang="xx" data-fixed-lang>`.
- hreflang: `/`, `/?lang=sq`, `/?lang=de` (same for `/essentials`, `/privacy`).

## Tea request flow (no stock, no payment up front)

1. Visitor fills `#request-form` on `index.html`: name, email, country, tea,
   quantity, reply language, notes, required GDPR consent checkbox.
2. JS posts it as FormData to Formspree (`action` on the form; currently the
   existing contact form ID `xpwzgjgv`) with a `_subject` like
   `Tea request: 3 × Caj Mali 50 g – Name (Country)`, sets
   `sessionStorage.besa_request_sent`, and redirects to the request thank-you
   page in the current language.
3. The owner replies by email with price + shipping, then sends a Stripe
   payment link. Payment completes the purchase; delivery up to 5 days after.
- The Stripe Buy Button markup is kept in `<template id="stripe-checkout">`
  inside `#request`: inert, not rendered, script not loaded. Move its contents
  out of the template to re-enable direct checkout.

## Amazon affiliate products

- 7 products (3 teapots, cezve, grinder, cups, tray), each an `amzn.to/…` link
  with `target="_blank" rel="nofollow sponsored"`, on both `index.html` (shop
  grid, `data-cat` for filters) and `essentials.html`.
- Affiliate disclosure under each product list and in every footer.
- Prices are hard-coded and labelled indicative. No Amazon star ratings, review
  counts or sales figures (Amazon Associates rules).

## Analytics, tags and consent

- Nothing from Google Ads or Meta loads until the visitor clicks **Accept** in
  the cookie banner (`besa.js`). Choice stored in `localStorage['besa_consent']`;
  "Cookie settings" buttons (`[data-cookie-settings]`) reopen the banner;
  Reject after Accept sends a consent `denied` update.
- On accept: `gtag.js` for **`AW-18368007697`**, plus any IDs in
  `CONFIG.extraGoogleTagIds` (e.g. `GT-5R4G63DN`, not added yet), plus the Meta
  pixel if `CONFIG.metaPixelId` is set.
- **Lead** (request thank-you pages): `generate_lead` always; Google Ads
  conversion if `CONFIG.adsLeadLabel` is set; Meta `Lead` if the pixel is set.
  Fires only after a real submission (sessionStorage flag) and with consent.
- **Purchase** (`thank-you*.html`): unchanged, still loads gtag directly and
  uses the placeholder label `YOUR_CONVERSION_LABEL`.
- No Google Tag Manager container is used.

## Deployment

GitHub Pages, legacy build (no Actions workflow), source `main` / root. Custom
domain `besagoods.com` via `CNAME`; `www` 301-redirects to the apex, so all
canonical/hreflang/sitemap URLs use `https://besagoods.com`. Pushing to `main`
publishes within a minute or two.

Local preview: `python3 -m http.server 4180` in the repo root, then open
`http://localhost:4180/`. Links use `essentials.html` / `privacy.html` so they
work locally; Pages also serves them at `/essentials` and `/privacy`.
