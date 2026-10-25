# -*- coding: utf-8 -*-
"""Generates /fahrzeuge/e-roller/<slug>.html individual model pages from the
canonical eroller_catalog.py data. Pure data -> HTML templating, no invented
facts: every sentence is built from a real, confirmed field."""
import sys, os, re, html, json
sys.path.insert(0, os.path.dirname(__file__))
from eroller_catalog import PRODUCTS

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "fahrzeuge", "e-roller")
IMG_BASE = "../../assets/images/products/"
SITE = "https://e-suero.ch"

def esc(s):
    return html.escape(str(s), quote=True)

def by_slug(slug):
    for p in PRODUCTS:
        if p["slug"] == slug:
            return p
    return None

def is_a1(p):
    return "Kat. A1" in p["badges"]

def spec_dict(p):
    return dict(p["spec"])

def find_sibling(p):
    """The 25<->45 km/h twin of the same base name, if one exists."""
    base = re.sub(r"\s*45 km/h$", "", p["name"]).strip()
    for q in PRODUCTS:
        if q["slug"] != p["slug"] and re.sub(r"\s*45 km/h$", "", q["name"]).strip() == base:
            return q
    return None

def find_price_neighbor(p):
    """Closest-priced other product, for an honest 'alternative' comparison."""
    others = [q for q in PRODUCTS if q["slug"] != p["slug"]]
    return min(others, key=lambda q: abs(q["price_rappen"] - p["price_rappen"]))

def chf(rappen):
    return "CHF {:,.2f}".format(rappen / 100).replace(",", "'")

def color_swatches_html(p, active_color=None):
    active_color = active_color or p["colors"][0]
    out = []
    for c in p["colors"]:
        img = p["color_imgs"][c]
        hexv = p["color_hex"][c]
        is_active = " is-active" if c == active_color else ""
        extra_border = ';border-color:#3a3f3d' if hexv.lower() in ("#f2f2f2",) else ''
        out.append(
            f'<button type="button" class="color-dot{is_active}" style="background:{hexv}{extra_border}" '
            f'data-img="{IMG_BASE}{img}?v=20260812" aria-label="{esc(c)}"></button>'
        )
    return "".join(out)

def spec_table_html(p):
    rows = "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in p["spec"])
    return f'<dl class="spec-list">{rows}</dl>'

def practical_info_rows(p):
    """Only confirmed fields — brief explicitly forbids inventing battery
    warranty / included-charger / removable-battery claims we don't have."""
    sd = spec_dict(p)
    rows = []
    rows.append(("Höchstgeschwindigkeit", sd.get("Höchstgeschwindigkeit", "")))
    if "Reichweite (pro Akkuladung)" in sd:
        rows.append(("Reichweite (pro Akkuladung)", sd["Reichweite (pro Akkuladung)"]))
    akku_cap = sd.get("Akkukapazität / Typ")
    if akku_cap:
        rows.append(("Akkukapazität / Typ", f"{akku_cap} ({p['voltage']})"))
    if "Ladezeit" in sd:
        rows.append(("Ladezeit", sd["Ladezeit"]))
    if "Gewicht" in sd:
        rows.append(("Gewicht", sd["Gewicht"]))
    if "Nutzlast" in sd:
        rows.append(("Nutzlast", sd["Nutzlast"]))
    if "Plätze" in sd:
        rows.append(("Plätze", sd["Plätze"]))
    garantie = sd.get("Garantie") or sd.get("Herstellergarantie")
    if garantie:
        rows.append(("Garantie", garantie))
    fs = sd.get("Führerschein")
    if fs:
        rows.append(("Führerschein", fs))
    ks = sd.get("Kontrollschild") or sd.get("Kontrollschild / Fahrzeugausweis")
    if ks:
        rows.append(("Kontrollschild / Fahrzeugausweis", ks))
    return rows

def needs_text(p):
    a1 = is_a1(p)
    sd = spec_dict(p)
    reich = sd.get("Reichweite (pro Akkuladung)", "")
    if a1:
        return (f"Mit Kat.-A1-Zulassung und bis zu {p['spec'][0][1]} ist dieses Modell für längere "
                f"Pendelstrecken und zügiges Vorankommen ausgelegt — Kontrollschild und Führerausweis "
                f"der entsprechenden Kategorie sind dafür Voraussetzung.")
    else:
        return (f"Als führerscheinfreies Modell bis {p['spec'][0][1]} eignet es sich für den täglichen "
                f"Weg zur Arbeit, zum Bahnhof oder für Besorgungen in und um Freienbach, ohne Führerausweis-Pflicht.")

def differences_text(p):
    sib = find_sibling(p)
    parts = []
    if sib:
        if is_a1(p):
            parts.append(
                f"Gegenüber der führerscheinfreien Version <strong>{esc(sib['name'])}</strong> (bis "
                f"{dict(sib['spec']).get('Höchstgeschwindigkeit')}) erlaubt dieses Modell eine höhere "
                f"Höchstgeschwindigkeit, benötigt dafür aber Kontrollschild und den passenden Führerausweis."
            )
        else:
            parts.append(
                f"Wer mehr Tempo möchte, findet in <strong>{esc(sib['name'])}</strong> dieselbe Basis mit "
                f"Kat.-A1-Zulassung bis {dict(sib['spec']).get('Höchstgeschwindigkeit')} — dafür mit "
                f"Kontrollschild-Pflicht."
            )
    neighbor = find_price_neighbor(p)
    nb_sd = spec_dict(neighbor)
    price_diff = neighbor["price_rappen"] - p["price_rappen"]
    diff_word = "günstiger" if price_diff > 0 else "teurer"
    parts.append(
        f"Preislich nahe liegt auch <strong>{esc(neighbor['name'])}</strong> ({chf(neighbor['price_rappen'])}, "
        f"{abs(price_diff)//100 if abs(price_diff)>=100 else 0:.0f} CHF {diff_word}) mit "
        f"{esc(nb_sd.get('Höchstgeschwindigkeit','–'))} und {esc(neighbor['voltage'])}."
    )
    return " ".join(parts)

def faq_items(p):
    sd = spec_dict(p)
    items = []
    fs = sd.get("Führerschein", "")
    if "nicht erforderlich" in fs.lower():
        items.append(("Brauche ich einen Führerausweis für den " + p["name"] + "?",
                       "Nein. Dieses Modell ist mit " + sd.get("Höchstgeschwindigkeit", "") +
                       " in der Schweiz führerscheinfrei (" + fs + ")."))
    else:
        items.append(("Welchen Führerausweis brauche ich für den " + p["name"] + "?",
                       "Für dieses Kat.-A1-Modell (" + sd.get("Höchstgeschwindigkeit", "") + ") gilt: " + fs +
                       ". Ein Kontrollschild ist zusätzlich erforderlich."))
    garantie = sd.get("Garantie") or sd.get("Herstellergarantie")
    if garantie:
        items.append(("Wie viel Garantie erhalte ich beim Kauf?",
                       "Auf den " + p["name"] + " erhalten Sie " + garantie + " Herstellergarantie ab Übergabe."))
    items.append(("Kann ich den " + p["name"] + " vorher testen?",
                   "Ja — über den Button „Probefahrt anfragen“ auf dieser Seite können Sie einen Termin in "
                   "unserem Showroom in Freienbach SZ anfragen. Der Termin wird anschliessend von uns bestätigt."))
    items.append(("Wie läuft Lieferung oder Abholung ab?",
                   "Details zu Bearbeitungs- und Lieferzeit sowie zur kostenlosen Abholung im Showroom finden "
                   "Sie in unserem <a href=\"../../verkauf/bestell-lieferprozess.html\">Bestell- &amp; Lieferprozess</a>."))
    return items


def card_html(p, slug_prefix=""):
    sd = spec_dict(p)
    badges_html = "".join(f'<span class="badge{" ok" if not is_a1(p) else ""}">{esc(b)}</span>' for b in p["badges"])
    variants_html = ""
    if p["variants"]:
        chips = "".join(
            f'<button type="button" class="variant-chip{" is-active" if i==0 else ""}" '
            f'data-price-rappen="{v["price_rappen"]}" data-price-label="{esc(v["price_label"])}" '
            f'data-variant-label="{esc(v["label"])}">{esc(v["label"])}</button>'
            for i, v in enumerate(p["variants"])
        )
        variants_html = f'<div class="variant-select" role="radiogroup" aria-label="Variante wählen">{chips}</div>'
    price_label = p["variants"][0]["price_label"] if p["variants"] else chf(p["price_rappen"])
    main_img = p["color_imgs"][p["colors"][0]]
    return (
        f'<div class="tilt-card"><div class="tilt-card-inner" id="p-{p["id"][2:]}" '
        f'data-buy-name="{esc(p["name"])}" data-buy-price="{p["price_rappen"]}" '
        f'data-buy-img="{SITE}/assets/images/products/{main_img}" data-buy-slug="{p["slug"]}">'
        f'<div class="product-media"><img src="{IMG_BASE}{main_img}?v=20260812" alt="E-Suero {esc(p["name"])} E-Roller kaufen Freienbach SZ" width="960" height="640" loading="lazy"></div>'
        f'<div class="color-swatches">{color_swatches_html(p)}</div>'
        f'<div class="catalog-badges" style="margin-bottom:.9rem">{badges_html}</div>'
        f'<h3><a href="{p["slug"]}.html">{esc(p["name"])}</a></h3>'
        f'<p class="model-desc">{esc(p["voltage"])} · Farben: {esc(", ".join(p["colors"]))}</p>'
        f'{variants_html}'
        f'<span class="price">{esc(price_label)}</span>'
        f'<div style="display:flex;gap:.6rem;margin-top:1.1rem;flex-wrap:wrap">'
        f'<a href="{p["slug"]}.html" class="btn btn-ghost btn-sm magnetic">Modell ansehen</a>'
        f'</div></div></div>'
    )


PAGE_TMPL = """<!doctype html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#050505">
<link rel="icon" href="../../assets/icons/favicon.png" type="image/png">
<link rel="icon" href="../../assets/icons/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="../../assets/icons/apple-touch-icon.png">
<link rel="manifest" href="../../manifest.json">
<script>window.__PAGE_META__={{title:"{title_js}",desc:"{description_js}"}};</script>
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="product">
<meta property="og:site_name" content="E-Suero">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{og_image}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image}">

<link rel="preload" href="../../assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../../assets/fonts/space-grotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../../assets/fonts/fonts.css?v=20260808">
<link rel="stylesheet" href="../../styles.css?v=20261025">
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

<header class="site-header">
  <div class="container">
    <a href="../../index.html" class="logo">
      <picture>
        <source srcset="../../assets/images/logo-mark-160.webp 1x, ../../assets/images/logo-mark-320.webp 2x" type="image/webp">
        <img class="logo-mark" src="../../assets/images/logo-mark-160.png" srcset="../../assets/images/logo-mark-320.png 2x" alt="" width="38" height="38" loading="eager">
      </picture>
      <b>E</b>-SUERO
    </a>

    <nav class="nav-desktop" aria-label="Hauptnavigation">
      <a href="../../verkauf/index.html" data-i18n="nav_buy_vehicles">Fahrzeuge kaufen</a>
      <a href="../../index.html#workshop" data-i18n="nav_workshop">Werkstatt & Reparatur</a>
      <a href="../../index.html#lab" data-i18n="nav_lab">Batterie-Labor</a>
      <a href="../../index.html#about" data-i18n="nav_about">Über uns</a>
      <a href="../../index.html#contact" data-i18n="nav_contact">Kontakt</a>
    </nav>

    <div class="header-actions">
      <div class="lang-switch">
        <button class="lang-current" type="button" aria-haspopup="true"><span>DE</span> ▾</button>
        <div class="lang-menu" role="menu">
          <button type="button" data-lang="de" class="is-active">Deutsch</button>
          <button type="button" data-lang="en">English</button>
          <button type="button" data-lang="it">Italiano</button>
          <button type="button" data-lang="es">Español</button>
        </div>
      </div>
      <a href="#modell-kontakt" class="btn btn-primary btn-sm magnetic" data-i18n="nav_cta_probefahrt">Probefahrt anfragen</a>
      <button class="burger" type="button" aria-label="Menü öffnen" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<div class="mobile-nav">
  <a href="../../verkauf/index.html" data-i18n="nav_buy_vehicles">Fahrzeuge kaufen</a>
  <a href="../../index.html#workshop" data-i18n="nav_workshop">Werkstatt & Reparatur</a>
  <a href="../../index.html#lab" data-i18n="nav_lab">Batterie-Labor</a>
  <a href="../../index.html#about" data-i18n="nav_about">Über uns</a>
  <a href="../../index.html#contact" data-i18n="nav_contact">Kontakt</a>
  <a href="#modell-kontakt" class="btn btn-primary" data-i18n="nav_cta_probefahrt">Probefahrt anfragen</a>
</div>

<main id="main">

<section class="section-tight">
  <div class="container">
    <nav aria-label="Breadcrumb" class="breadcrumb">
      <a href="../../index.html">E-Suero</a> ›
      <a href="../../verkauf/index.html">Fahrzeuge kaufen</a> ›
      <a href="../e-roller.html">E-Roller</a> ›
      <span aria-current="page">{name}</span>
    </nav>

    <div class="model-hero reveal">
      <div class="model-gallery">
        <div class="product-media model-media"><img src="{IMG_BASE}{main_img}?v=20260812" alt="E-Suero {name} E-Roller kaufen Freienbach SZ" width="960" height="640" loading="eager"></div>
        <div class="color-swatches">{swatches}</div>
      </div>
      <div class="model-info">
        <span class="eyebrow">E-Roller · {badge0}</span>
        <h1>{name}</h1>
        <p class="model-desc" style="font-size:1rem">{voltage} · Farben: {colors}</p>
        {variant_select}
        <span class="price" style="font-size:2rem;display:block;margin:.6rem 0 1rem">{price_label}</span>
        <p style="color:var(--c-mute);max-width:56ch">{needs_text}</p>
        <div style="margin:1.2rem 0">
          {benefits}
        </div>
        <p class="delivery-note"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v5l3 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg><span>Verfügbarkeit beim Lieferanten · Bearbeitung: 0–3 Werktage · <a href="../../verkauf/bestell-lieferprozess.html">Mehr zu Lieferung &amp; Abholung</a></span></p>
        <div style="display:flex;gap:.8rem;margin-top:1.4rem;flex-wrap:wrap">
          <button type="button" class="btn btn-primary magnetic" data-buy-btn>Jetzt kaufen</button>
          <a href="#modell-kontakt" class="btn btn-ghost magnetic">Probefahrt anfragen</a>
          <a href="#" class="btn btn-ghost magnetic" data-wa-model="{name_attr}" target="_blank" rel="noopener">Auf WhatsApp fragen</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Praktische Angaben</span>
      <h2>Was Sie vor dem Kauf wissen sollten.</h2>
    </div>
    <dl class="spec-list reveal">
      {practical_rows}
    </dl>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Unterschiede</span>
      <h2>Im Vergleich zu anderen Modellen.</h2>
    </div>
    <p class="reveal" style="color:var(--c-mute);max-width:72ch">{differences}</p>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Technische Daten</span>
      <h2>Vollständige Spezifikationen.</h2>
    </div>
    {full_spec}
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Nach dem Kauf</span>
      <h2>Support von E-Suero.</h2>
    </div>
    <p class="reveal" style="color:var(--c-mute);max-width:72ch">Als Käuferin oder Käufer des {name} profitieren Sie von unserer eigenen Werkstatt in Freienbach SZ für <a href="../../leistungen/batterie.html">Batterie-Diagnostik und -Reparatur</a> sowie <a href="../../leistungen/werkstatt.html">allgemeinen Service</a> — auch nach Ablauf der Herstellergarantie.</p>
  </div>
</section>

<section id="faq" class="section-tight">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">FAQ</span>
      <h2>Fragen zum {name}.</h2>
    </div>
    <div class="faq-list reveal">
      {faq_html}
    </div>
  </div>
</section>

<section id="modell-kontakt" class="section-tight">
  <div class="container contact-wrap">
    <div>
      <span class="eyebrow">Kontakt</span>
      <h2>Anfrage zum {name}.</h2>
      <p style="color:var(--c-mute);margin-top:1rem">Beratung, Probefahrt oder ein persönliches Angebot — wir melden uns in der Regel innerhalb eines Werktags.</p>
      <form data-sales-form data-model="{name_attr}" class="contact-form" style="margin-top:1.6rem" novalidate>
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
    </div>
  </div>
</section>

</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <a href="../../index.html" class="logo">
          <picture>
            <source srcset="../../assets/images/logo-mark-160.webp 1x, ../../assets/images/logo-mark-320.webp 2x" type="image/webp">
            <img class="logo-mark" src="../../assets/images/logo-mark-160.png" srcset="../../assets/images/logo-mark-320.png 2x" alt="" width="38" height="38" loading="lazy">
          </picture>
          <b>E</b>-SUERO
        </a>
        <p data-i18n="footer_desc">Premium Elektromobilität, Werkstatt und Batterie-Diagnostik in Freienbach SZ — für Kanton Schwyz, die Zürichsee-Region und den Nebelkanton.</p>
        <p class="footer-nap">
          Schwerzistrasse 34, 8807 Freienbach SZ<br>
          <a href="tel:+41796689088">+41 79 668 90 88</a> · <a href="mailto:info@e-suero.ch">info@e-suero.ch</a>
        </p>
        <div class="footer-social">
          <a href="https://wa.me/41796689088" target="_blank" rel="noopener" aria-label="WhatsApp">
            <svg viewBox="0 0 24 24" fill="none"><path d="M4 20l1.4-4.2A8 8 0 1 1 9 19l-5 1Z" stroke="currentColor" stroke-width="1.6"/></svg>
          </a>
        </div>
      </div>
      <div class="footer-col">
        <h3 data-i18n="footer_col1_h">Services</h3>
        <a href="../../leistungen/diagnose.html" data-i18n="fc1_1">Batterie-Diagnostik</a>
        <a href="../../leistungen/batterie.html" data-i18n="fc1_2">Batterie-Reparatur</a>
        <a href="../../leistungen/software.html" data-i18n="fc1_3">Controller-Reparatur</a>
        <a href="../../leistungen/mobility.html" data-i18n="fc1_4">Flottenwartung</a>
      </div>
      <div class="footer-col">
        <h3 data-i18n="footer_col2_h">Unternehmen</h3>
        <a href="../../index.html#about" data-i18n="fc2_1">Über uns</a>
        <a href="../../leistungen/werkstatt.html" data-i18n="fc2_2">Werkstatt</a>
        <a href="../../verkauf/bestell-lieferprozess.html" data-i18n="footer_order_delivery">Bestell- &amp; Lieferprozess</a>
        <a href="../../index.html#gallery" data-i18n="fc2_3">Galerie</a>
        <a href="../../index.html#contact" data-i18n="fc2_4">Kontakt</a>
      </div>
      <div class="footer-col">
        <h3 data-i18n="footer_col3_h">Rechtliches</h3>
        <a href="../../legal/privacy.html" data-i18n="fc3_1">Datenschutz</a>
        <a href="../../legal/impressum.html" data-i18n="fc3_2">Impressum</a>
        <a href="../../legal/terms.html" data-i18n="fc3_3">AGB</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span id="year">2026</span> E-Suero. <span data-i18n="footer_rights">Alle Rechte vorbehalten.</span></span>
      <div class="legal-links">
        <a href="../../legal/privacy.html" data-i18n="fc3_1">Datenschutz</a>
        <a href="../../legal/impressum.html" data-i18n="fc3_2">Impressum</a>
        <a href="../../legal/terms.html" data-i18n="fc3_3">AGB</a>
      </div>
    </div>
  </div>
</footer>

<a class="whatsapp-btn" href="https://wa.me/41796689088" target="_blank" rel="noopener" data-i18n-aria="wa_label" aria-label="Auf WhatsApp schreiben">
  <svg viewBox="0 0 24 24" fill="none"><path d="M4 20l1.4-4.2A8 8 0 1 1 9 19l-5 1Z" stroke="currentColor" stroke-width="1.6"/></svg>
</a>
<button class="back-to-top" type="button" data-i18n-aria="top_label" aria-label="Nach oben">
  <svg viewBox="0 0 24 24" fill="none"><path d="M12 19V5M5 12l7-7 7 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
</button>

<script src="../../lib/gsap.min.js" defer></script>
<script src="../../lib/ScrollTrigger.min.js" defer></script>
<script src="../../i18n.js?v=20260819" defer></script>
<script src="../../main.js?v=20260819" defer></script>
<script src="../../assets/js/stripe-checkout.js?v=20260815" defer></script>
<script src="../../assets/js/sales-form.js?v=20261025" defer></script>
</body>
</html>
"""


def build_page(p):
    sd = spec_dict(p)
    canonical = f"{SITE}/fahrzeuge/e-roller/{p['slug']}.html"
    main_img = p["color_imgs"][p["colors"][0]]
    og_image = f"{SITE}/assets/images/products/{main_img}"
    a1 = is_a1(p)
    speed = sd.get("Höchstgeschwindigkeit", "")
    title = f"{p['name']} kaufen Freienbach SZ | {speed} E-Roller — E-Suero"
    description = (f"{p['name']} bei E-Suero in Freienbach SZ: {speed}, {p['voltage']}, "
                    f"{chf(p['price_rappen'])}. {'Kat. A1' if a1 else 'Ohne Führerschein'}. "
                    f"Beratung, Probefahrt und Kauf direkt beim Fachhändler.")

    benefits = []
    if "nicht erforderlich" in sd.get("Führerschein", "").lower():
        benefits.append("Ohne Führerausweis-Pflicht fahrbereit")
    else:
        benefits.append("Kat.-A1-Zulassung für höheres Tempo")
    if "Reichweite (pro Akkuladung)" in sd:
        benefits.append(f"Reichweite {sd['Reichweite (pro Akkuladung)']}")
    garantie = sd.get("Garantie") or sd.get("Herstellergarantie")
    if garantie:
        benefits.append(f"{garantie} Herstellergarantie")
    benefits_html = "<ul class=\"check-list\">" + "".join(
        f'<li><svg viewBox="0 0 24 24" fill="none"><path d="M4 12.5l4.5 4.5L20 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>{esc(b)}</li>'
        for b in benefits
    ) + "</ul>"

    variant_select = ""
    price_label = chf(p["price_rappen"])
    if p["variants"]:
        chips = "".join(
            f'<button type="button" class="variant-chip{" is-active" if i==0 else ""}" '
            f'data-price-rappen="{v["price_rappen"]}" data-price-label="{esc(v["price_label"])}" '
            f'data-variant-label="{esc(v["label"])}">{esc(v["label"])}</button>'
            for i, v in enumerate(p["variants"])
        )
        variant_select = f'<div class="variant-select" role="radiogroup" aria-label="Variante wählen">{chips}</div>'
        price_label = p["variants"][0]["price_label"]

    practical_rows = "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in practical_info_rows(p))

    faq_html_parts = []
    for i, (q, a) in enumerate(faq_items(p)):
        open_cls = " is-open" if i == 0 else ""
        style = ' style="max-height:200px"' if i == 0 else ""
        faq_html_parts.append(
            f'<div class="faq-item{open_cls}"><button class="faq-q"><span>{esc(q)}</span><span class="plus"></span></button>'
            f'<div class="faq-a"{style}><p>{a}</p></div></div>'
        )
    faq_html = "".join(faq_html_parts)

    faq_jsonld = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": re.sub("<[^>]+>", "", q),
             "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}}
            for q, a in faq_items(p)
        ],
    }
    breadcrumb_jsonld = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "E-Suero", "item": f"{SITE}/index.html"},
            {"@type": "ListItem", "position": 2, "name": "Fahrzeuge kaufen", "item": f"{SITE}/verkauf/index.html"},
            {"@type": "ListItem", "position": 3, "name": "E-Roller", "item": f"{SITE}/fahrzeuge/e-roller.html"},
            {"@type": "ListItem", "position": 4, "name": p["name"], "item": canonical},
        ],
    }
    product_jsonld = {
        "@context": "https://schema.org", "@type": "Product",
        "name": f"E-Suero {p['name']}",
        "description": description,
        "category": "E-Roller",
        "image": og_image,
        "brand": {"@type": "Brand", "name": "E-Suero"},
        "offers": {
            "@type": "Offer", "priceCurrency": "CHF",
            "price": "{:.2f}".format(p["price_rappen"] / 100),
            "availability": "https://schema.org/InStock",
            "url": canonical,
        },
    }
    jsonld = json.dumps([product_jsonld, breadcrumb_jsonld, faq_jsonld], ensure_ascii=False, indent=2)

    html_out = PAGE_TMPL.format(
        title=esc(title), title_js=title.replace('"', '\\"'),
        description=esc(description), description_js=description.replace('"', '\\"'),
        canonical=canonical, og_image=og_image,
        jsonld=jsonld,
        name=esc(p["name"]), name_attr=esc(p["name"]),
        IMG_BASE=IMG_BASE, main_img=main_img,
        swatches=color_swatches_html(p),
        badge0=esc(p["badges"][0]),
        voltage=esc(p["voltage"]), colors=esc(", ".join(p["colors"])),
        variant_select=variant_select, price_label=esc(price_label),
        needs_text=needs_text(p),
        benefits=benefits_html,
        practical_rows=practical_rows,
        differences=differences_text(p),
        full_spec=spec_table_html(p),
        faq_html=faq_html,
        slug=p["slug"],
    )
    return html_out


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for p in PRODUCTS:
        out_path = os.path.join(OUT_DIR, f"{p['slug']}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(build_page(p))
        print("wrote", out_path)
