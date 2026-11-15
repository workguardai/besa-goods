# German content plan (draft, not published)

Folder `_docs/` is not published by GitHub Pages. Nothing here is live.

## Goal

Rank in German search for the mountain-tea topic cluster and send readers to
the **tea request form** (`/de/#request`) and the **on-site shop**
(`/de/#shop`, `/de/essentials.html`). Articles never link straight to Amazon;
the essentials page carries the Amazon links and the disclosure.

## Ground rules for every article

- **No health or medical claims.** Sideritis is widely marketed with health
  promises; under the EU Health Claims Regulation (1924/2006) there are no
  approved claims for it. Talk about origin, taste, tradition, brewing,
  culture. "Naturally caffeine-free" is fine (it's a fact we already state).
- **Facts to verify before publishing:** which Sideritis species our Çaj Mali
  is, and any botanical or geographic statement. Don't publish species names
  until the supplier confirms them.
- Same claims as the shop: wild harvested above 1,200 m, no additives,
  sourced to order, pay after confirmation, delivery up to 5 days after
  payment, shipping cost confirmed before payment.
- Each article ends with the same CTA box: Çaj Mali 50 g, €12.90 + shipping,
  "Unverbindlich anfragen" → `/de/#request`, plus "Zum Shop" → `/de/#shop`.
- Keyword volumes below are **not measured**. Check them in Google Ads
  Keyword Planner (Germany, Austria, Switzerland) before writing.
  "griechischer Bergtee" and "Sideritis" are crowded by Greek-tea shops; our
  angle is Albanian origin and the diaspora.

## Where the pages live

```
/de/ratgeber/                          hub page listing all articles
/de/ratgeber/<slug>/                   one folder per article
```

Built like the other pages: add a German-only source to `_src/` and a line to
`PAGES` in `_tools/build.py` (same pattern as `albanischer-bergtee.html`), so
each gets its canonical URL, hreflang `de` and a sitemap entry automatically.
Link the hub from the German footer and from the landing page.

## The six pages

### 1. Albanischer Bergtee: Herkunft, Ernte und Tradition
- **URL:** `/de/ratgeber/albanischer-bergtee-herkunft/`
- **Keywords:** albanischer Bergtee, Çaj Mali, Bergtee aus Albanien, çaj mali kaufen
- **Title:** Albanischer Bergtee (Çaj Mali): Herkunft & Ernte | Besa Goods
- **Outline:** Was ist Çaj Mali? · Die albanischen Alpen (Lage, Höhe, Landschaft) · Wie und wann geerntet wird · Çaj Mali im albanischen Alltag · So kommt er zu Ihnen (Anfrage → Bestätigung → Zahlung → Lieferung)
- **Links:** CTA box → `/de/#request`; "So funktioniert's" → `/de/#how`; landing page
- **Length:** ~900 words, 2 photos (alps banner, dried tea)

### 2. Bergtee richtig zubereiten: Schritt für Schritt
- **URL:** `/de/ratgeber/bergtee-zubereiten/`
- **Keywords:** Bergtee zubereiten, griechischer Bergtee Zubereitung, Sideritis Tee zubereiten, Çaj Mali zubereiten
- **Title:** Bergtee zubereiten: Menge, Temperatur & Ziehzeit | Besa Goods
- **Outline:** Was Sie brauchen · Menge pro Tasse (1 gehäufter TL, as on the site) · Ziehzeit 5–7 Min. · Aufgießen in der Kanne vs. kurz aufkochen (traditional way) · Mit Honig, ohne Milch · Kalt genießen im Sommer · Häufige Fehler
- **Links:** CTA box; "Passende Teekannen" → `/de/essentials.html#teapots`
- **Length:** ~700 words, step photos if available

### 3. Griechischer oder albanischer Bergtee: Was ist der Unterschied?
- **URL:** `/de/ratgeber/griechischer-albanischer-bergtee/`
- **Keywords:** griechischer Bergtee, albanischer Bergtee Unterschied, Bergtee Balkan
- **Title:** Griechischer vs. albanischer Bergtee: Der Unterschied | Besa Goods
- **Outline:** Gemeinsamkeiten (Bergkräuter des Balkans, Sideritis) · Herkunft und Anbaugebiete · Geschmack (only our own tasting notes: earthy, floral, honey) · Wild gesammelt vs. angebaut (only what we can verify) · Woran man Qualität erkennt (ganze Stängel, Blüten, Duft)
- **Links:** CTA box; article 4
- **Note:** needs the species/origin facts verified first

### 4. Sideritis einfach erklärt: die Pflanze hinter dem Bergtee
- **URL:** `/de/ratgeber/sideritis/`
- **Keywords:** Sideritis, Sideritis Tee, Gliedkraut, Bergtee Pflanze
- **Title:** Sideritis: Die Pflanze hinter dem Bergtee | Besa Goods
- **Outline:** Name und Herkunft des Namens · Wo die Pflanze wächst (Gebirge des Mittelmeerraums und Balkans) · Aussehen und Blüte · Warum wilde Bestände geschützt werden müssen (sustainable harvesting, if the supplier confirms practices) · Vom Feld in die Tasse
- **Links:** CTA box; articles 1 and 3
- **Strictly no health claims**, including "traditionally used for…" phrasing

### 5. Geschenkideen aus Albanien: Bergtee, Teekannen & Kaffee
- **URL:** `/de/ratgeber/geschenkideen-albanien/`
- **Keywords:** Geschenk aus Albanien, albanische Geschenke, Geschenk für Teeliebhaber, Mitbringsel Albanien
- **Title:** Geschenkideen aus Albanien für Teeliebhaber | Besa Goods
- **Outline:** Für die Familie (Çaj Mali) · Für Teeliebhaber (tea + cast-iron teapot) · Für Kaffeetrinker (cezve + cups, "Kaffee wie in Albanien") · Timing tip: request early because the tea is sourced to order
- **Links:** CTA box; `/de/essentials.html` for teapots and coffee (on-site page, Amazon links live there with the disclosure); landing page for the community angle
- **Length:** ~600 words, product photos from `/images/`

### 6. Teekannen-Ratgeber: welche Kanne für Bergtee?
- **URL:** `/de/ratgeber/teekanne-bergtee/`
- **Keywords:** Teekanne Gusseisen, Teekanne für Kräutertee, Teekanne mit Sieb
- **Title:** Welche Teekanne für Bergtee? Gusseisen, Glas, Keramik | Besa Goods
- **Outline:** Was Bergtee braucht (whole stems, space, steady heat) · Gusseisen: Vor- und Nachteile, Pflege · Glas: man sieht die Blüten · Keramik · Sieb oder lose · Unsere drei Empfehlungen (short, link to essentials)
- **Links:** `/de/essentials.html#teapots`; CTA box for the tea
- **Note:** the essentials prices are hand-typed; don't repeat prices in the article

## Order to write them

1, 2, 5 first (closest to buying intent and safest on facts), then 6,
then 3 and 4 once the species and origin facts are confirmed.
