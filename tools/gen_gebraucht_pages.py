# -*- coding: utf-8 -*-
"""Generates the individual used-vehicle pages (verkauf/gebraucht/<slug>.html)
from tools/gebraucht_vespino.py. Run: python3 tools/gen_gebraucht_pages.py
"""
import os, sys, json

sys.path.insert(0, os.path.dirname(__file__))
import sales_chrome
from model_page_lib import esc, chf, trust_block_html, SITE
from gebraucht_vespino import (
    UNITS, BRAND, MODEL, BATTERY_VOLTAGE, BATTERY_CAPACITY, RANGE_TEXT,
    WARRANTY, PRICE_RAPPEN, LOCATION, SERVICE_TEXT,
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "verkauf", "gebraucht")

RANGE_DISCLAIMER = (
    "Die tatsächliche Reichweite hängt unter anderem vom Zustand der Batterie, "
    "Fahrergewicht, Strecke, Temperatur und Fahrweise ab. Die Angabe ist keine "
    "Zusicherung einer bei dieser Occasion gemessenen Reichweite."
)

SERVICE_BLOCK_TITLE = "Vollständiger Service bereits durchgeführt"
SERVICE_BLOCK_TEXT = (
    "Bei diesem Fahrzeug wurde ein vollständiger mechanischer und elektronischer Service "
    "durchgeführt. Sie kaufen einen gebrauchten E-Roller mit durchgeführtem Service und "
    "6 Monaten Garantie – mit persönlicher Betreuung durch E-Suero."
)


def media_html(unit):
    if unit.get("image"):
        return (
            f'<div class="product-media model-media">'
            f'<img src="../../assets/images/products/{unit["image"]}" alt="{esc(unit["alt"])}" '
            f'width="{unit.get("image_width", 1200)}" height="{unit.get("image_height", 900)}" loading="eager"></div>'
        )
    return (
        '<div class="product-media model-media photo-pending">'
        '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 11.5 5 7h14l2 4.5M4 11.5h16v7a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-7Z" stroke="currentColor" stroke-width="1.4"/><circle cx="7.5" cy="15" r="1.4" stroke="currentColor" stroke-width="1.3"/><circle cx="16.5" cy="15" r="1.4" stroke="currentColor" stroke-width="1.3"/></svg>'
        '<span>Foto folgt in Kürze</span>'
        '</div>'
    )


def build_jsonld(unit):
    canonical = f"{SITE}/verkauf/gebraucht/{unit['slug']}.html"
    product = {
        "@context": "https://schema.org", "@type": "Product",
        "name": f"E-Suero {unit['title']}",
        "description": unit["meta_description"],
        "category": "E-Roller",
        "brand": {"@type": "Brand", "name": BRAND},
        "model": MODEL,
        "itemCondition": "https://schema.org/UsedCondition",
    }
    if unit.get("image"):
        product["image"] = f"{SITE}/assets/images/products/{unit['image']}"
    product["offers"] = {
        "@type": "Offer", "priceCurrency": "CHF",
        "price": "{:.2f}".format(PRICE_RAPPEN / 100),
        "itemCondition": "https://schema.org/UsedCondition",
        "availability": "https://schema.org/InStock" if unit["available"] else "https://schema.org/OutOfStock",
        "url": canonical,
        "seller": {"@type": "Organization", "name": "E-Suero", "url": f"{SITE}/index.html"},
    }
    # No sku/gtin invented, no shippingDetails/hasMerchantReturnPolicy (no published
    # per-unit terms), no review/aggregateRating (see tools/QUELLEN-PRODUKTDATEN.md).
    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "E-Suero", "item": f"{SITE}/index.html"},
            {"@type": "ListItem", "position": 2, "name": "Alle Fahrzeuge", "item": f"{SITE}/verkauf/index.html"},
            {"@type": "ListItem", "position": 3, "name": "Gebraucht & Geprüft", "item": f"{SITE}/verkauf/gebraucht-geprueft.html"},
            {"@type": "ListItem", "position": 4, "name": unit["title"], "item": canonical},
        ],
    }
    return json.dumps([product, breadcrumb], ensure_ascii=False, indent=2)


PAGE_TMPL = """<!doctype html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{seo_title}</title>
<meta name="description" content="{meta_description}">
<meta name="theme-color" content="#050505">
<link rel="icon" href="../../assets/icons/favicon.png" type="image/png">
<link rel="icon" href="../../assets/icons/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="../../assets/icons/apple-touch-icon.png">
<link rel="manifest" href="../../manifest.json">
<script>window.__PAGE_META__={{title:"{seo_title_js}",desc:"{meta_description_js}"}};</script>
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="product">
<meta property="og:site_name" content="E-Suero">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{seo_title}">
<meta property="og:description" content="{meta_description}">
<meta property="og:image" content="{og_image}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{seo_title}">
<meta name="twitter:description" content="{meta_description}">
<meta name="twitter:image" content="{og_image}">

<link rel="preload" href="../../assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../../assets/fonts/space-grotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../../assets/fonts/fonts.css?v=20260808">
<link rel="stylesheet" href="../../styles.css?v=20261104">
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>
<a class="skip-link" href="#main" data-i18n="skip_to_content">Zum Inhalt springen</a>

<div class="splash" aria-hidden="true">
  <div class="splash-inner">
    <img class="splash-mark" src="../../assets/images/logo-mark-160.png" srcset="../../assets/images/logo-mark-320.png 2x" alt="" width="48" height="48">
    <div class="splash-logo"><b>E</b>-SUERO</div>
  </div>
</div>

{header}

{mobile_nav}

<main id="main">

<section class="section-tight">
  <div class="container">
    <nav aria-label="Breadcrumb" class="breadcrumb">
      <a href="../../index.html">E-Suero</a> ›
      <a href="../../verkauf/index.html" data-i18n="nav_all_vehicles">Alle Fahrzeuge</a> ›
      <a href="../gebraucht-geprueft.html">Gebraucht &amp; Geprüft</a> ›
      <a href="../gebraucht-geprueft.html#/e-roller" data-i18n="nav_e_roller">E-Roller</a> ›
      <span aria-current="page">{title}</span>
    </nav>

    <div class="model-hero reveal">
      <div class="model-gallery">
        {media}
      </div>
      <div class="model-info">
        <span class="eyebrow">E-Roller · Occasion</span>
        <h1>{title}</h1>
        <div class="catalog-badges" style="margin:.9rem 0">
          <span class="badge">Occasion</span>
          <span class="badge ok">Mechanischer &amp; elektronischer Service durchgeführt</span>
          <span class="badge ok">6 Monate Garantie</span>
        </div>
        <span class="price" style="font-size:2rem;display:block;margin:.6rem 0 1rem">CHF 1'500.–</span>
        <p style="color:var(--c-mute);max-width:56ch">{intro}</p>
        <div style="margin:1.2rem 0">
          <ul class="check-list" style="grid-template-columns:1fr">
            <li><svg viewBox="0 0 24 24" fill="none"><path d="M4 12.5l4.5 4.5L20 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>48 V / 23 Ah</li>
            <li><svg viewBox="0 0 24 24" fill="none"><path d="M4 12.5l4.5 4.5L20 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Bis zu 60 km Reichweite</li>
          </ul>
        </div>
        <div class="trust-block reveal" style="margin:1.2rem 0">
          <div class="trust-block-head">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 12.5l2 2 4-4.5M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6l7-3Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>
            <div>
              <h3>{service_block_title}</h3>
              <p>{service_block_text}</p>
            </div>
          </div>
        </div>
        <div style="display:flex;gap:.8rem;margin-top:1.4rem;flex-wrap:wrap">
          <a href="#kontakt" data-reason="probefahrt" class="btn btn-primary magnetic">Besichtigung &amp; Probefahrt anfragen</a>
          <a href="tel:+41796689088" class="btn btn-ghost magnetic">Jetzt anrufen</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Technische Daten</span>
      <h2>Angaben zu diesem Fahrzeug.</h2>
    </div>
    <dl class="spec-list reveal">
      <dt>Marke</dt><dd>{brand}</dd>
      <dt>Modell</dt><dd>{model}</dd>
      <dt>Zustand</dt><dd>Occasion / gebraucht</dd>
      <dt>Farbe</dt><dd>{color}</dd>
      <dt>Akkuspannung</dt><dd>{battery_voltage}</dd>
      <dt>Akkukapazität</dt><dd>{battery_capacity}</dd>
      <dt>Angegebene Reichweite</dt><dd>{range_text}</dd>
      <dt>Service</dt><dd>{service_text}</dd>
      <dt>Garantie</dt><dd>{warranty}</dd>
      <dt>Preis</dt><dd>CHF 1'500.– pro Fahrzeug</dd>
      <dt>Standort</dt><dd>{location}</dd>
    </dl>
    <p style="color:var(--c-mute-2);font-size:.82rem;margin-top:1rem;max-width:72ch">{range_disclaimer}</p>
  </div>
</section>

{trust_block}

<section id="kontakt" class="section-tight">
  <div class="container contact-wrap">
    <div>
      <span class="eyebrow">Kontakt</span>
      <h2>Anfrage zum {title}.</h2>
      <p style="color:var(--c-mute);margin-top:1rem">Beratung, Besichtigung oder Probefahrt — wir melden uns in der Regel innerhalb eines Werktags.</p>
      <form data-sales-form data-model="{title_attr}" class="contact-form" style="margin-top:1.6rem" novalidate>
        <input type="text" name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px;top:-9999px" aria-hidden="true">
        <div class="field" data-field="model-display" hidden>
          <label>Modell</label>
          <input type="text" disabled>
        </div>
        <div class="form-row">
          <div class="field">
            <label for="sf-name-{slug}">Name</label>
            <input id="sf-name-{slug}" name="name" type="text" required>
          </div>
          <div class="field">
            <label for="sf-reason-{slug}">Anliegen</label>
            <select id="sf-reason-{slug}" name="reason">
              <option value="beratung">Beratung</option>
              <option value="probefahrt">Probefahrt</option>
              <option value="angebot">Angebot</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="field">
            <label for="sf-phone-{slug}">Telefon</label>
            <input id="sf-phone-{slug}" name="phone" type="tel">
          </div>
          <div class="field">
            <label for="sf-email-{slug}">E-Mail</label>
            <input id="sf-email-{slug}" name="email" type="email">
          </div>
        </div>
        <div class="field" data-field="preferred_date" hidden>
          <label for="sf-date-{slug}">Wunschtermin (optional)</label>
          <input id="sf-date-{slug}" name="preferred_date" type="date">
        </div>
        <div class="field">
          <label for="sf-message-{slug}">Nachricht (optional)</label>
          <textarea id="sf-message-{slug}" name="message"></textarea>
        </div>
        <button type="submit" class="btn btn-primary magnetic">Anfrage senden</button>
        <p class="form-status" role="status"></p>
        <p class="form-note">Bitte Telefon oder E-Mail angeben. Eine Probefahrt-Anfrage ist noch keine bestätigte Terminbuchung.</p>
      </form>
    </div>
    <div class="contact-side">
      <div class="contact-card reveal">
        <svg viewBox="0 0 24 24" fill="none"><path d="M12 21s7-6.6 7-12a7 7 0 1 0-14 0c0 5.4 7 12 7 12Z" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="9" r="2.5" stroke="currentColor" stroke-width="1.6"/></svg>
        <div><b>Showroom</b><span>Schwerzistrasse 34, 8807 Freienbach SZ, Schweiz</span></div>
      </div>
      <div class="contact-card reveal">
        <svg viewBox="0 0 24 24" fill="none"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.98.36 1.94.7 2.86a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.22-1.27a2 2 0 0 1 2.11-.45c.92.34 1.88.57 2.86.7A2 2 0 0 1 22 16.92Z" stroke="currentColor" stroke-width="1.6"/></svg>
        <div><b>Telefon</b><a href="tel:+41796689088">+41 79 668 90 88</a></div>
      </div>
      <div class="contact-card reveal">
        <svg viewBox="0 0 24 24" fill="none"><path d="M4 4h16v16H4z" stroke="currentColor" stroke-width="1.6"/><path d="m4 6 8 7 8-7" stroke="currentColor" stroke-width="1.6"/></svg>
        <div><b>E-Mail</b><a href="mailto:info@e-suero.ch">info@e-suero.ch</a></div>
      </div>
      <a href="tel:+41796689088" class="btn btn-ghost magnetic" style="margin-top:.4rem">Jetzt anrufen</a>
    </div>
  </div>
</section>

</main>

{footer}

<a class="whatsapp-btn" href="https://wa.me/41796689088" target="_blank" rel="noopener" data-i18n-aria="wa_label" aria-label="Auf WhatsApp schreiben">
  <svg viewBox="0 0 24 24" fill="none"><path d="M4 20l1.4-4.2A8 8 0 1 1 9 19l-5 1Z" stroke="currentColor" stroke-width="1.6"/></svg>
</a>
<button class="back-to-top" type="button" data-i18n-aria="top_label" aria-label="Nach oben">
  <svg viewBox="0 0 24 24" fill="none"><path d="M12 19V5M5 12l7-7 7 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
</button>

<script src="../../lib/gsap.min.js" defer></script>
<script src="../../lib/ScrollTrigger.min.js" defer></script>
<script src="../../i18n.js?v=20261105" defer></script>
<script src="../../main.js?v=20261106" defer></script>
<script src="../../assets/js/sales-form.js?v=20261029" defer></script>
</body>
</html>
"""


def build_page(unit):
    canonical = f"{SITE}/verkauf/gebraucht/{unit['slug']}.html"
    og_image = f"{SITE}/assets/images/products/{unit['image']}" if unit.get("image") else f"{SITE}/assets/images/logo-mark-320.png"
    header = sales_chrome.header_html("../../", "#kontakt", None)
    mobile_nav = sales_chrome.mobile_nav_html("../../", "#kontakt", None)
    footer = sales_chrome.footer_html("../../")

    html_out = PAGE_TMPL.format(
        seo_title=esc(unit["seo_title"]), seo_title_js=unit["seo_title"].replace('"', '\\"'),
        meta_description=esc(unit["meta_description"]), meta_description_js=unit["meta_description"].replace('"', '\\"'),
        canonical=canonical, og_image=og_image,
        jsonld=build_jsonld(unit),
        header=header, mobile_nav=mobile_nav, footer=footer,
        title=esc(unit["title"]), title_attr=esc(unit["title"]), slug=unit["slug"],
        media=media_html(unit),
        intro=esc(unit["intro"]),
        service_block_title=esc(SERVICE_BLOCK_TITLE), service_block_text=esc(SERVICE_BLOCK_TEXT),
        brand=esc(BRAND), model=esc(MODEL), color=esc(unit["color"]),
        battery_voltage=esc(BATTERY_VOLTAGE), battery_capacity=esc(BATTERY_CAPACITY),
        range_text=esc(RANGE_TEXT), service_text=esc(SERVICE_TEXT), warranty=esc(WARRANTY),
        location=esc(LOCATION), range_disclaimer=esc(RANGE_DISCLAIMER),
        trust_block=f'<section class="section-tight"><div class="container">{trust_block_html("../../")}</div></section>',
    )
    return html_out


def generate():
    os.makedirs(OUT_DIR, exist_ok=True)
    for unit in UNITS:
        out_path = os.path.join(OUT_DIR, f"{unit['slug']}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(build_page(unit))
        print("wrote", os.path.abspath(out_path))


if __name__ == "__main__":
    generate()
