# Besa Goods — besagoods.com

Static site, no build step, no framework, no package.json. Every page is a single
self-contained HTML file with inline CSS and inline JS. Hosted on GitHub Pages.

Sells Albanian mountain tea (Çaj Mali) directly and recommends teaware / Albanian
coffee accessories through Amazon affiliate links. Audience: Albanian diaspora and
tourists, mainly UK and Germany. Business base: Madrid.

## Rules for working here

- **`main` deploys live** (GitHub Pages, branch `main`, path `/`). Never commit to
  `main` directly; work on a branch and merge via PR.
- Never commit secrets. The Stripe `pk_live_…` publishable key and the Mailchimp /
  Formspree form IDs in the HTML are public by design; secret keys (`sk_…`,
  webhook secrets, API tokens) must never appear in this repo.
- Do not change prices, product claims, shipping terms or availability wording
  without the owner's approval.
- Keep the visual design: colour tokens in `:root`, Poppins font, the
  forest-green / bark / gold palette.

## File structure

| File | What it is |
|---|---|
| `index.html` | Home page (~1,370 lines). Teapot + coffee Amazon showcases at the top, then hero with Mailchimp signup + Stripe Buy Button, "How it works", two teas (Çaj Mali available, Bari i Malit "coming later 2026"), origin section, second Mailchimp + Stripe CTA (`#preorder`), About / Returns / Contact, footer, scripts. |
| `essentials.html` | "Brew Essentials" page: 3 teapot cards + 4 coffee cards, all Amazon affiliate links, brewing tips, affiliate disclosure. Served at `/essentials` (GitHub Pages resolves the extension-less URL). |
| `thank-you.html` / `thank-you-de.html` | Stripe success pages. Fire the Google Ads purchase conversion when `?session_id=` is present. No SQ version. `noindex`. |
| `besa-sitemap.xml` | Sitemap (lists `/` with en/sq/it/de alternates and `/essentials`). Note: lists an `it` alternate that does not exist. |
| `CNAME` | `besagoods.com` |
| `google490ef79068abc80c.html` | Google Search Console verification — do not delete. |
| `*.png` | Product and hero images (≈10 MB total, unoptimised; `besa-tea-portrait.png` is actually a JPEG). |

## Languages (EN / SQ / DE)

Client-side only, all three languages live in the same HTML file:

- Each translatable string is duplicated in sibling elements with class `en`,
  `sq` or `de`; non-English ones start with `style="display:none"`.
- `setLang(lang)` (inline `<script>` at the bottom of each page) hides every
  `.en/.sq/.de` element, shows the chosen class, and falls back to showing `.en`
  when a parent has no translation for that language. Choice saved in
  `localStorage['besa_lang']`, shared between pages.
- `index.html` wraps `setLang` again to swap contact-form placeholders from
  `data-placeholder-en|sq|de`.
- **Known gaps:** many strings have no `de` (or no `sq`) sibling, so they fall
  back to English; some have duplicate `de` siblings. The hreflang tags point to
  `/?lang=sq` and `/?lang=de`, but no code reads the `lang` URL parameter, so
  those URLs serve English to users and crawlers. `<html lang>`, `<title>` and
  meta description never change with language.

## Amazon affiliate products

- 3 teapots + 4 coffee items, each a card with image, badge, hard-coded price
  text, name and a "Shop on Amazon →" link to an `amzn.to/…` short link with
  `target="_blank" rel="nofollow sponsored"`. Same 7 products appear in both
  `index.html` (inline-styled showcase sections) and `essentials.html` (`.card`
  classes for teapots, inline styles for coffee).
- Affiliate disclosure exists only at the bottom of `essentials.html`; the home
  page has none.
- `essentials.html` shows Amazon star ratings / review counts and "300+ sold last
  month" as static text, plus static prices.

## Payments (Stripe) and email capture

- **Stripe Buy Button** (`js.stripe.com/v3/buy-button.js`,
  `buy-button-id="buy_btn_1TEeFaD9VgNxznDq7m4FqdVV"`, live publishable key) is
  embedded twice in `index.html`: in the hero (`.stripe-wrap`) and in the
  `#preorder` CTA. Product: Çaj Mali 50 g, €12.90. The success redirect to
  `thank-you.html?session_id=…` is configured in the Stripe dashboard, not here.
- **Mailchimp** "Notify me" forms (hero `#hero-form` and `#cta-form`) post to
  `besagoods.us5.list-manage.com` in a new tab; JS then fakes a success message.
- **Contact form** (`#contact-form`, `sendContact()`) POSTs JSON to Formspree
  `https://formspree.io/f/xpwzgjgv`, falling back to `mailto:besasonos@gmail.com`.
  Bug: it reads an undefined variable `_lang`, which throws before the request,
  so the form currently never submits.

## Analytics and tags

- `index.html` and both thank-you pages load **gtag.js for Google Ads
  `AW-18368007697`** and call `gtag('config', 'AW-18368007697')` unconditionally
  (no consent banner, no consent mode). `essentials.html` loads no tags.
- Purchase conversion (thank-you pages): `gtag('event','conversion',
  {send_to:'AW-18368007697/YOUR_CONVERSION_LABEL', value:12.90, currency:'EUR',
  transaction_id: session_id})`. **The label is still the placeholder**, so this
  conversion does not currently record in Google Ads.
- `GT-5R4G63DN` and Google Tag Manager are **not present** in any file, despite
  a commit message mentioning GTM. If they are configured, it is only in the
  Google tag / Ads UI.
- No Meta pixel, no GA4 config, no cookie banner, no privacy policy page.

## Deployment

GitHub Pages, legacy build (no Actions workflow), source `main` / root. Custom
domain `besagoods.com` via `CNAME`; certificate covers apex and `www`. "Enforce
HTTPS" is currently **off** in the Pages settings. Pushing to `main` publishes
within a minute or two. To preview locally: `python3 -m http.server 8000` in the
repo root (note `/essentials` needs `/essentials.html` locally).
