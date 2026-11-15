/* Besa Goods shared script: language switching, cookie consent, ad tags.
   Loaded with `defer` on every page except the Stripe purchase thank-you pages. */
(function () {
  'use strict';

  // ── CONFIG: the only place IDs live ───────────────────────────────────────
  var CONFIG = {
    adsId: 'AW-18368007697',      // Google Ads account (existing)
    extraGoogleTagIds: [],        // e.g. ['GT-5R4G63DN'] if you want that tag on the site too
    adsLeadLabel: '',             // Google Ads "Lead" conversion label, e.g. 'AbC1dEfGhIjK'
    metaPixelId: ''               // Meta pixel ID, e.g. '123456789012345'
  };
  var LANGS = ['en', 'sq', 'de'];
  var LANG_KEY = 'besa_lang';
  var CONSENT_KEY = 'besa_consent';
  var root = document.documentElement;

  function store(key, val) { try { localStorage.setItem(key, val); } catch (e) {} }
  function read(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }

  // ── LANGUAGE ──────────────────────────────────────────────────────────────
  function currentLang() { return LANGS.indexOf(root.lang) >= 0 ? root.lang : 'en'; }

  function swapAttr(attr, apply, lang) {
    document.querySelectorAll('[data-' + attr + '-en]').forEach(function (el) {
      var v = el.getAttribute('data-' + attr + '-' + lang);
      if (v == null) v = el.getAttribute('data-' + attr + '-en');
      apply(el, v);
    });
  }

  function applyLang(lang, save) {
    if (LANGS.indexOf(lang) < 0) lang = 'en';
    root.lang = lang;

    // Show English when a block has no translation in the chosen language.
    document.querySelectorAll('.en').forEach(function (el) {
      var p = el.parentElement;
      var has = lang === 'en' || (p && p.querySelector(':scope > .' + lang));
      el.classList.toggle('lang-fallback', !has);
    });

    swapAttr('t', function (el, v) { el.textContent = v; }, lang);            // text (title, <option>)
    swapAttr('ph', function (el, v) { el.placeholder = v; }, lang);           // placeholders
    swapAttr('al', function (el, v) { el.setAttribute('aria-label', v); }, lang);
    swapAttr('alt', function (el, v) { el.alt = v; }, lang);                   // image alt text
    swapAttr('content', function (el, v) { el.setAttribute('content', v); }, lang); // meta description

    document.querySelectorAll('[data-set-lang]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-set-lang') === lang));
    });

    if (!root.hasAttribute('data-fixed-lang')) {
      var url = new URL(location.href);
      if (lang === 'en') url.searchParams.delete('lang'); else url.searchParams.set('lang', lang);
      if (url.href !== location.href) history.replaceState(history.state, '', url.href);
      var canon = document.querySelector('link[rel="canonical"]');
      if (canon && canon.hasAttribute('data-base')) {
        canon.href = canon.getAttribute('data-base') + (lang === 'en' ? '' : '?lang=' + lang);
      }
    }
    if (save) store(LANG_KEY, lang);
    document.dispatchEvent(new CustomEvent('besa:lang', { detail: lang }));
  }

  // ── CONSENT + TAGS ────────────────────────────────────────────────────────
  // Nothing from Google or Meta loads until the visitor clicks Accept.
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  var tagsLoaded = false;
  var waiting = [];

  function loadTags() {
    if (tagsLoaded) return;
    tagsLoaded = true;
    gtag('consent', 'default', {
      ad_storage: 'granted', ad_user_data: 'granted',
      ad_personalization: 'granted', analytics_storage: 'granted'
    });
    gtag('js', new Date());
    gtag('config', CONFIG.adsId);
    CONFIG.extraGoogleTagIds.forEach(function (id) { gtag('config', id); });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + CONFIG.adsId;
    document.head.appendChild(s);

    if (CONFIG.metaPixelId) {
      /* Standard Meta pixel loader */
      !function (f, b, e, v, n, t, u) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; u = b.getElementsByTagName(e)[0]; u.parentNode.insertBefore(t, u); }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
      fbq('init', CONFIG.metaPixelId);
      fbq('track', 'PageView');
    }
    waiting.splice(0).forEach(function (fn) { try { fn(); } catch (e) {} });
  }

  function revokeTags() {
    if (!tagsLoaded) return;
    gtag('consent', 'update', {
      ad_storage: 'denied', ad_user_data: 'denied',
      ad_personalization: 'denied', analytics_storage: 'denied'
    });
    if (window.fbq) fbq('consent', 'revoke');
  }

  var banner;
  function buildBanner() {
    banner = document.createElement('div');
    banner.className = 'cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-live', 'polite');
    banner.setAttribute('aria-label', 'Cookies');
    banner.hidden = true;
    banner.innerHTML =
      '<p>' +
      '<span class="en">We use cookies from Google and Meta to measure our ads, only if you accept. The site works fully without them. <a href="privacy.html#cookies">Privacy policy</a></span>' +
      '<span class="sq">Përdorim cookies nga Google dhe Meta për të matur reklamat tona, vetëm nëse pranoni. Faqja funksionon plotësisht edhe pa to. <a href="privacy.html#cookies-sq">Politika e privatësisë</a></span>' +
      '<span class="de">Wir verwenden Cookies von Google und Meta, um unsere Werbung zu messen – nur wenn Sie zustimmen. Die Seite funktioniert auch ohne sie vollständig. <a href="privacy.html#cookies-de">Datenschutzerklärung</a></span>' +
      '</p>' +
      '<div class="cookie-actions">' +
      '<button type="button" class="btn btn-outline" data-consent="denied"><span class="en">Reject</span><span class="sq">Refuzo</span><span class="de">Ablehnen</span></button>' +
      '<button type="button" class="btn btn-primary" data-consent="granted"><span class="en">Accept</span><span class="sq">Prano</span><span class="de">Akzeptieren</span></button>' +
      '</div>';
    banner.addEventListener('click', function (e) {
      var b = e.target.closest('[data-consent]');
      if (!b) return;
      var v = b.getAttribute('data-consent');
      store(CONSENT_KEY, v);
      if (v === 'granted') loadTags(); else revokeTags();
      hideBanner();
    });
    document.body.appendChild(banner);
  }
  function showBanner() {
    if (!banner) buildBanner();
    banner.hidden = false;
    document.body.classList.add('cookie-open');
  }
  function hideBanner() {
    if (banner) banner.hidden = true;
    document.body.classList.remove('cookie-open');
  }

  // ── PUBLIC API ────────────────────────────────────────────────────────────
  window.besa = {
    config: CONFIG,
    lang: currentLang,
    setLang: function (l) { applyLang(l, true); },
    // Run fn once the visitor has accepted cookies (now, or later on this page).
    whenConsented: function (fn) { if (tagsLoaded) fn(); else waiting.push(fn); },
    // Fired on the request thank-you pages. A request is a lead, not a purchase.
    trackLead: function () {
      gtag('event', 'generate_lead', { currency: 'EUR' });
      if (CONFIG.adsLeadLabel) {
        gtag('event', 'conversion', { send_to: CONFIG.adsId + '/' + CONFIG.adsLeadLabel });
      }
      if (window.fbq) fbq('track', 'Lead');
    },
    // Outbound click on a "Shop on Amazon" button. Sent only if the visitor has
    // already accepted cookies; never queued for later.
    trackAmazonClick: function (productName, url) {
      if (!tagsLoaded) return;
      var lang = currentLang();
      gtag('event', 'amazon_click', {
        product_name: productName, language: lang, link_url: url, outbound: true,
        transport_type: 'beacon'
      });
      if (window.fbq) fbq('trackCustom', 'AmazonClick', { product_name: productName, language: lang });
    }
  };

  // English product name for reports, whatever language the page is shown in.
  function amazonProductName(a) {
    var card = a.closest('.product');
    var el = card && (card.querySelector('.product-name .en') || card.querySelector('.product-name'));
    return el ? el.textContent.trim() : (a.getAttribute('data-product') || 'unknown');
  }

  function init() {
    applyLang(currentLang(), false);
    document.addEventListener('click', function (e) {
      var l = e.target.closest('[data-set-lang]');
      if (l) { applyLang(l.getAttribute('data-set-lang'), true); return; }
      if (e.target.closest('[data-cookie-settings]')) { e.preventDefault(); showBanner(); return; }
      var amz = e.target.closest('a[href*="amzn.to/"], a[href*="amazon."]');
      if (amz) window.besa.trackAmazonClick(amazonProductName(amz), amz.href);
    });
    var c = read(CONSENT_KEY);
    if (c === 'granted') loadTags();
    else if (c !== 'denied') showBanner();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
