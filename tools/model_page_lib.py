# -*- coding: utf-8 -*-
"""Shared individual-model-page renderer, used by every vehicle category
(E-Roller, E-Motorräder, E-Scooter, E-Bike, E-Minicar). Pure data -> HTML,
no invented facts — every sentence is built from a real, confirmed field
in that category's own catalog module.

A `category` is a dict:
  name          "E-Roller"            (shown in breadcrumb/eyebrow/title)
  dir           "e-roller"            (folder under fahrzeuge/)
  landing       "fahrzeuge/e-roller.html"
"""
import os, re, html, json

SITE = "https://e-suero.ch"
IMG_BASE = "../../assets/images/products/"

import sys
sys.path.insert(0, os.path.dirname(__file__))
import sales_chrome


def esc(s):
    return html.escape(str(s), quote=True)


NAME_I18N_KEY = {
    "E-Roller": "nav_e_roller",
    "E-Motorräder": "nav_e_motorraeder",
    "E-Scooter": "nav_e_scooter",
    "E-Bike": "nav_e_bike",
    "E-Minicar": "nav_e_minicar",
}


def is_a1(p):
    return "Kat. A1" in p["badges"]


def spec_dict(p):
    return dict(p["spec"])


def chf(rappen):
    return "CHF {:,.2f}".format(rappen / 100).replace(",", "'")


def price_block_html(p, extra_style=""):
    """Price display, incl. optional before/after sale price
    (p["price_before_rappen"]) — never invented, only rendered when the
    catalog explicitly sets it."""
    style_attr = f' style="{extra_style}"' if extra_style else ""
    has_price = bool(p.get("price_rappen"))
    if not has_price:
        return f'<span class="price"{style_attr}>Preis auf Anfrage</span>'
    if p.get("variants"):
        return f'<span class="price"{style_attr}>{esc(p["variants"][0]["price_label"])}</span>'
    price_label = chf(p["price_rappen"])
    before = p.get("price_before_rappen")
    if before and before > p["price_rappen"]:
        save = before - p["price_rappen"]
        return (
            f'<span class="price-sale"{style_attr}>'
            f'<span class="price-old">{esc(chf(before))}</span>'
            f'<span class="price">{esc(price_label)}</span>'
            f'<span class="price-save">Sie sparen {esc(chf(save))}</span>'
            f'</span>'
        )
    return f'<span class="price"{style_attr}>{esc(price_label)}</span>'


def trust_block_html(base):
    """Post-purchase trust block, reused on every vehicle detail page
    (new and used) via model_page_lib.build_page() / gebraucht-katalog.js's
    equivalent. `base` is the relative path back to the site root."""
    return f"""<div class="trust-block reveal">
          <div class="trust-block-head">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M14.7 6.3a3 3 0 0 0-4.24 4.24L4 17v3h3l6.46-6.46a3 3 0 0 0 4.24-4.24l-2.3-2.3-1.4 1.4 1.4 1.4-1.06 1.06-1.4-1.4 1.4-1.4-2.3-2.3Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>
            <div>
              <h3 data-i18n="trust_title">Auch nach dem Kauf für Sie da.</h3>
              <p data-i18n="trust_body">Bei E-Suero haben Sie einen persönlichen Ansprechpartner und eine eigene Werkstatt in Freienbach. Ob Wartung, Reparatur oder Fragen zu Ihrem Fahrzeug: Wir unterstützen Sie auch nach der Übergabe.</p>
            </div>
          </div>
          <ul class="trust-block-list">
            <li><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 12.5l4.5 4.5L20 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span data-i18n="trust_item_workshop">Eigene Werkstatt in Freienbach</span></li>
            <li><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 12.5l4.5 4.5L20 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span data-i18n="trust_item_contact">Persönlicher Ansprechpartner</span></li>
            <li><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 12.5l4.5 4.5L20 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span data-i18n="trust_item_onsite">Wartung und Reparatur vor Ort</span></li>
          </ul>
          <a href="{base}leistungen/werkstatt.html" class="trust-block-link" data-i18n="trust_link">Unsere Werkstatt kennenlernen →</a>
        </div>"""


def media_html(p, category, css_class, alt_suffix, img_base=None):
    """Real product photo, or an honest placeholder if none exists yet —
    never a stock/representative image standing in for the real vehicle.
    img_base defaults to the model-page depth (../../); pass "../" when
    rendering on a one-level-deep category landing page instead."""
    base = img_base if img_base is not None else IMG_BASE
    if p.get("no_photo"):
        return (
            f'<div class="{css_class} photo-pending">'
            f'<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 11.5 5 7h14l2 4.5M4 11.5h16v7a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-7Z" stroke="currentColor" stroke-width="1.4"/><circle cx="7.5" cy="15" r="1.4" stroke="currentColor" stroke-width="1.3"/><circle cx="16.5" cy="15" r="1.4" stroke="currentColor" stroke-width="1.3"/></svg>'
            f'<span>Foto folgt in Kürze</span>'
            f'</div>'
        )
    main_img = p["color_imgs"][p["colors"][0]]
    return f'<div class="{css_class}"><img src="{base}{main_img}?v=20260812" alt="E-Suero {esc(p["name"])} {esc(alt_suffix)}" width="960" height="640" loading="lazy"></div>'


def color_swatches_html(p, img_base=None):
    if not p.get("colors"):
        return ""
    base = img_base if img_base is not None else IMG_BASE
    out = []
    for i, c in enumerate(p["colors"]):
        img = p["color_imgs"][c]
        hexv = p["color_hex"][c]
        is_active = " is-active" if i == 0 else ""
        extra_border = ';border-color:#3a3f3d' if hexv.lower() in ("#f2f2f2",) else ''
        out.append(
            f'<button type="button" class="color-dot{is_active}" style="background:{hexv}{extra_border}" '
            f'data-img="{base}{img}?v=20260812" aria-label="{esc(c)}"></button>'
        )
    return "".join(out)


SPEC_LABEL_KEYS = {
    'Höchstgeschwindigkeit': 'spec_top_speed',
    'Führerschein': 'spec_license',
    'Akkukapazität / Typ': 'spec_battery_cap',
    'Reichweite (pro Akkuladung)': 'spec_range',
    'Gewicht': 'spec_weight',
    'Ladezeit': 'spec_charge_time',
    'Nutzlast': 'spec_payload',
    'Kontrollschild / Fahrzeugausweis': 'spec_plate',
    'Akkuleistung': 'spec_voltage',
    'Garantie': 'spec_warranty',
    'Optionales Zubehör': 'spec_accessories',
    'USB-Schnittstelle': 'spec_usb',
    'Alarmanlage': 'spec_alarm',
    'Länge / Breite / Höhe': 'spec_dimensions',
    'Fernbedienung (Keyless Drive)': 'spec_remote',
    'Motorleistung': 'spec_motor_power',
    'Bremse vorne / hinten': 'spec_brakes',
    'Maximale Steigung': 'spec_max_incline',
    'Typengenehmigung': 'spec_type_approval',
    'Rückwärtsgang': 'spec_reverse',
    'Plätze': 'spec_seats',
    'Motor Nenn- / Spitzenleistung': 'spec_motor_power_peak',
    'Typengeprüft in CH': 'spec_ch_tested',
    'Motor': 'spec_motor',
    'Batterie': 'spec_battery',
    'Rahmen': 'spec_frame',
    'Schaltung': 'spec_gears',
    'Bremsen': 'spec_brakes_generic',
    'Reifen': 'spec_tires',
    'Kontrollschild': 'spec_plate_short',
    'Herstellergarantie': 'spec_mfr_warranty',
    'Display': 'spec_display',
    'Gabel': 'spec_fork',
    'Frontlicht': 'spec_front_light',
    'Rücklicht': 'spec_rear_light',
    'Felgen': 'spec_rims',
    'Bremsen / System': 'spec_brake_system',
    'Carplay Display (Apple & Android)': 'spec_carplay',
    'Bremse vorne und hinten': 'spec_brakes_fr_und',
    'Bereifung vorne': 'spec_tire_front',
    'Bereifung hinten': 'spec_tire_rear',
    'Länge / Breite / Sitzhöhe': 'spec_dim_seat',
    'Alarmanlage / Bluetooth': 'spec_alarm_bt',
    'Bereifung': 'spec_tires_generic',
    'Reichweite': 'spec_range_short',
    'Federung': 'spec_suspension',
    'Farben & Zubehör': 'spec_colors_accessories',
    'Fertigung': 'spec_manufacturing',
    'Bremsen vorne und hinten': 'spec_brakes_fr_und2',
    'Bordelektronik': 'spec_electronics',
    'Alarmanlage & Hill Assist': 'spec_alarm_hillassist',
    'Elektrische Fensterheber': 'spec_power_windows',
    'Parksensoren & Rückfahrkamera': 'spec_parking_sensors',
    'Zubehör': 'spec_accessories_short',
}


DD_VALUE_KEYS = {
    "Serienmässig": "dd_standard",
    "Nicht erforderlich": "dd_not_required",
    "Erforderlich": "dd_required",
    "Nicht verfügbar": "dd_not_available",
    "Ja": "dd_yes",
    "Ab 16 Jahren nicht erforderlich": "dd_none_from_16",
    "Kat. A1 ab 15 Jahren (Unterkategorie)": "dd_a1_15_sub",
    "Kat. A1 ab 16 Jahren": "dd_a1_16",
    "Konfigurierbar": "dd_configurable",
    "2 Jahre": "dd_warranty_2y",
    "3 Jahre": "dd_warranty_3y",
    "5 Std.": "dd_charge_5h",
    "4–5 Std.": "dd_charge_45h",
    "4 Std. (75% nach 2 Std.)": "dd_charge_4h75",
    "Scheibenbremsen": "dd_disc_brakes",
    "Zusatzakku": "dd_spare_battery",
    "Winterreifen": "dd_winter_tyres",
    "Zusatzakku / Winterreifen": "dd_spare_batt_wintertyres",
    "Zusatzakku / Winterreifen / Topcase / Handyhalter": "dd_accessories_combo1",
    "Zusatzakku / Winterreifen / Handyhalter": "dd_accessories_combo2",
}


def dt_html(label):
    key = SPEC_LABEL_KEYS.get(label)
    attr = f' data-i18n="{key}"' if key else ""
    return f"<dt{attr}>{esc(label)}</dt>"


def dd_html(value):
    key = DD_VALUE_KEYS.get(value)
    attr = f' data-i18n="{key}"' if key else ""
    return f"<dd{attr}>{esc(value)}</dd>"


def spec_table_html(p):
    rows = "".join(f"{dt_html(k)}{dd_html(v)}" for k, v in p["spec"])
    return f'<dl class="spec-list">{rows}</dl>'


def practical_info_rows(p):
    """Only confirmed fields — never invents battery warranty / included
    charger / removable-battery claims that aren't in the source data."""
    sd = spec_dict(p)
    rows = []
    for key in ("Höchstgeschwindigkeit", "Reichweite (pro Akkuladung)"):
        if sd.get(key):
            rows.append((key, sd[key]))
    akku_cap = sd.get("Akkukapazität / Typ")
    if akku_cap:
        rows.append(("Akkukapazität / Typ", f"{akku_cap} ({p['voltage']})"))
    for key in ("Ladezeit", "Gewicht", "Nutzlast", "Plätze"):
        if sd.get(key):
            rows.append((key, sd[key]))
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


def needs_text(p, category):
    sd = spec_dict(p)
    a1 = is_a1(p)
    top_speed = sd.get("Höchstgeschwindigkeit", "")
    if a1:
        return (f"Mit Kat.-A1-Zulassung und bis zu {top_speed} ist dieses Modell für längere "
                f"Pendelstrecken und zügiges Vorankommen ausgelegt — Kontrollschild und Führerausweis "
                f"der entsprechenden Kategorie sind dafür Voraussetzung.")
    if "nicht erforderlich" in sd.get("Führerschein", "").lower():
        return (f"Als führerscheinfreies Modell bis {top_speed} eignet es sich für den täglichen "
                f"Weg zur Arbeit, zum Bahnhof oder für Besorgungen in und um Freienbach, ohne "
                f"Führerausweis-Pflicht.")
    return f"Ein {category['name']}-Modell für den täglichen Einsatz in und um Freienbach SZ."


def find_sibling(p, products):
    base = re.sub(r"\s*45 km/h$", "", p["name"]).strip()
    for q in products:
        if q["slug"] != p["slug"] and re.sub(r"\s*45 km/h$", "", q["name"]).strip() == base:
            return q
    return None


def find_price_neighbor(p, products, exclude_slugs=()):
    others = [q for q in products if q["slug"] != p["slug"] and q["slug"] not in exclude_slugs]
    if not others:
        return None
    return min(others, key=lambda q: abs(q["price_rappen"] - p["price_rappen"]))


def differences_text(p, products):
    sib = find_sibling(p, products)
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
    neighbor = find_price_neighbor(p, products, exclude_slugs={sib["slug"]} if sib else set())
    if neighbor:
        nb_sd = spec_dict(neighbor)
        price_diff = neighbor["price_rappen"] - p["price_rappen"]
        if price_diff == 0:
            price_phrase = "zum gleichen Preis"
        else:
            diff_word = "günstiger" if price_diff > 0 else "teurer"
            price_phrase = f"{abs(price_diff)//100:.0f} CHF {diff_word}"
        parts.append(
            f"Preislich nahe liegt auch <strong>{esc(neighbor['name'])}</strong> ({chf(neighbor['price_rappen'])}, "
            f"{price_phrase}) mit "
            f"{esc(nb_sd.get('Höchstgeschwindigkeit','–'))} und {esc(neighbor['voltage'])}."
        )
    if not parts:
        return "Dieses Modell steht aktuell allein in seiner Kategorie — die vollständigen technischen Daten finden Sie weiter unten."
    return " ".join(parts)


def faq_items(p, category):
    sd = spec_dict(p)
    items = []
    fs = sd.get("Führerschein", "")
    if "nicht erforderlich" in fs.lower():
        items.append((f"Brauche ich einen Führerausweis für den {p['name']}?",
                       f"Nein. Dieses Modell ist mit {sd.get('Höchstgeschwindigkeit', '')} "
                       f"in der Schweiz führerscheinfrei ({fs})."))
    elif fs:
        items.append((f"Welchen Führerausweis brauche ich für den {p['name']}?",
                       f"Für dieses Modell ({sd.get('Höchstgeschwindigkeit', '')}) gilt: {fs}."))
    garantie = sd.get("Garantie") or sd.get("Herstellergarantie")
    if garantie:
        items.append(("Wie viel Garantie erhalte ich beim Kauf?",
                       f"Auf den {p['name']} erhalten Sie {garantie} Herstellergarantie ab Übergabe."))
    items.append((f"Kann ich den {p['name']} vorher testen?",
                   "Ja — über den Button „Probefahrt anfragen“ auf dieser Seite können Sie einen Termin in "
                   "unserem Showroom in Freienbach SZ anfragen. Der Termin wird anschliessend von uns bestätigt."))
    items.append(("Wie läuft Lieferung oder Abholung ab?",
                   "Details zu Bearbeitungs- und Lieferzeit sowie zur kostenlosen Abholung im Showroom finden "
                   "Sie in unserem <a href=\"../../verkauf/bestell-lieferprozess.html\">Bestell- &amp; Lieferprozess</a>."))
    return items


def card_html(p, category, img_base=None, link_dir=None):
    """img_base/link_dir let this be reused from pages outside fahrzeuge/
    (e.g. the homepage, which sits at the site root) — both default to the
    paths that work from a one-level-deep fahrzeuge/<category>.html page."""
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
    has_price = bool(p.get("price_rappen"))
    colors_line = f' · Farben: {esc(", ".join(p["colors"]))}' if p.get("colors") else ""
    card_img_base = img_base if img_base is not None else "../assets/images/products/"
    link_base = link_dir if link_dir is not None else category["dir"]
    media = media_html(p, category, "product-media", f'{category["name"]} kaufen Freienbach SZ', img_base=card_img_base)
    if has_price:
        buy_attrs = f'data-buy-name="{esc(p["name"])}" data-buy-price="{p["price_rappen"]}" data-buy-img="{SITE}/assets/images/products/{p["color_imgs"][p["colors"][0]]}" data-buy-slug="{p["slug"]}" '
        buy_btn = '<button type="button" class="btn btn-primary btn-sm magnetic" data-buy-btn data-i18n="buy_now">Jetzt kaufen</button>'
    else:
        buy_attrs = ""
        buy_btn = f'<a href="{link_base}/{p["slug"]}.html#modell-kontakt" data-reason="angebot" class="btn btn-primary btn-sm magnetic" data-i18n="cta_angebot">Angebot anfragen</a>'
    return (
        f'<div class="tilt-card"><div class="tilt-card-inner" id="p-{p["id"][2:]}" {buy_attrs}>'
        f'{media}'
        f'<div class="color-swatches">{color_swatches_html(p, img_base=card_img_base)}</div>'
        f'<div class="catalog-badges" style="margin-bottom:.9rem">{badges_html}</div>'
        f'<h3><a href="{link_base}/{p["slug"]}.html">{esc(p["name"])}</a></h3>'
        f'<p class="model-desc">{esc(p["voltage"])}{colors_line}</p>'
        f'{variants_html}'
        f'{price_block_html(p)}'
        f'<div style="display:flex;gap:.6rem;margin-top:1.1rem;flex-wrap:wrap">'
        f'{buy_btn}'
        f'<a href="{link_base}/{p["slug"]}.html" class="btn btn-ghost btn-sm magnetic" data-i18n="view_model">Modell ansehen</a>'
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
<link rel="stylesheet" href="../../styles.css?v=20261031">
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
      <a href="../../{landing}" data-i18n="{category_i18n_key}">{category_name}</a> ›
      <span aria-current="page">{name}</span>
    </nav>

    <div class="model-hero reveal"{buy_attrs}>
      <div class="model-gallery">
        {media_block}
        <div class="color-swatches">{swatches}</div>
      </div>
      <div class="model-info">
        <span class="eyebrow">{category_name} · {badge0}</span>
        <h1>{name}</h1>
        <p class="model-desc" style="font-size:1rem">{voltage}{colors_line}</p>
        {variant_select}
        {price_block}
        {needs_text}
        <div style="margin:1.2rem 0">
          {benefits}
        </div>
        <p class="delivery-note"><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v5l3 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg><span data-i18n-html="model_delivery_note_html">Verfügbarkeit beim Lieferanten · Bearbeitung: 0–3 Werktage · <a href="../../verkauf/bestell-lieferprozess.html">Mehr zu Lieferung &amp; Abholung</a></span></p>
        <div style="display:flex;gap:.8rem;margin-top:1.4rem;flex-wrap:wrap">
          {buy_button}
          <a href="#modell-kontakt" data-reason="probefahrt" class="btn btn-ghost magnetic" data-i18n="nav_cta_probefahrt">Probefahrt anfragen</a>
          <a href="#" class="btn btn-ghost magnetic" data-wa-model="{name_attr}" target="_blank" rel="noopener" data-i18n="cta_whatsapp_ask">Auf WhatsApp fragen</a>
        </div>
        {trust_block}
      </div>
    </div>
  </div>
</section>

{marketing_section}

{gallery_section}

<section class="section-tight">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow" data-i18n="model_practical_eyebrow">Praktische Angaben</span>
      <h2 data-i18n="model_practical_h">Was Sie vor dem Kauf wissen sollten.</h2>
    </div>
    <dl class="spec-list reveal">
      {practical_rows}
    </dl>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow" data-i18n="model_diff_eyebrow">Unterschiede</span>
      <h2 data-i18n="model_diff_h">Im Vergleich zu anderen Modellen.</h2>
    </div>
    <p class="reveal" style="color:var(--c-mute);max-width:72ch">{differences}</p>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow" data-i18n="model_specs_eyebrow">Technische Daten</span>
      <h2 data-i18n="model_specs_h">Vollständige Spezifikationen.</h2>
    </div>
    {full_spec}
    {footnotes}
  </div>
</section>

<section id="faq" class="section-tight">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow" data-i18n="faq_eyebrow">FAQ</span>
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
      <span class="eyebrow" data-i18n="contact_eyebrow_short">Kontakt</span>
      <h2>Anfrage zum {name}.</h2>
      <p style="color:var(--c-mute);margin-top:1rem" data-i18n="model_contact_intro">Beratung, Probefahrt oder ein persönliches Angebot — wir melden uns in der Regel innerhalb eines Werktags.</p>
      <form data-sales-form data-model="{name_attr}" class="contact-form" style="margin-top:1.6rem" novalidate>
        <input type="text" name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px;top:-9999px" aria-hidden="true">
        <div class="field" data-field="model-display" hidden>
          <label data-i18n="f_model_label">Modell</label>
          <input type="text" disabled>
        </div>
        <div class="form-row">
          <div class="field">
            <label for="sf-name-{slug}" data-i18n="f_name">Name</label>
            <input id="sf-name-{slug}" name="name" type="text" required>
          </div>
          <div class="field">
            <label for="sf-reason-{slug}" data-i18n="f_reason_label">Anliegen</label>
            <select id="sf-reason-{slug}" name="reason">
              <option value="beratung" data-i18n="f_reason_opt_beratung">Beratung</option>
              <option value="probefahrt" data-i18n="f_reason_opt_probefahrt">Probefahrt</option>
              <option value="angebot" data-i18n="f_reason_opt_angebot">Angebot</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="field">
            <label for="sf-phone-{slug}" data-i18n="side_phone_l">Telefon</label>
            <input id="sf-phone-{slug}" name="phone" type="tel">
          </div>
          <div class="field">
            <label for="sf-email-{slug}" data-i18n="side_email_l">E-Mail</label>
            <input id="sf-email-{slug}" name="email" type="email">
          </div>
        </div>
        <div class="field" data-field="preferred_date" hidden>
          <label for="sf-date-{slug}" data-i18n="f_preferred_date_label">Wunschtermin (optional)</label>
          <input id="sf-date-{slug}" name="preferred_date" type="date">
        </div>
        <div class="field">
          <label for="sf-message-{slug}" data-i18n="f_message_optional">Nachricht (optional)</label>
          <textarea id="sf-message-{slug}" name="message"></textarea>
        </div>
        <button type="submit" class="btn btn-primary magnetic" data-i18n="f_submit">Anfrage senden</button>
        <p class="form-status" role="status"></p>
        <p class="form-note" data-i18n="model_form_note">Bitte Telefon oder E-Mail angeben. Eine Probefahrt-Anfrage ist noch keine bestätigte Terminbuchung.</p>
      </form>
    </div>
    <div class="contact-side">
      <div class="contact-card reveal">
        <svg viewBox="0 0 24 24" fill="none"><path d="M12 21s7-6.6 7-12a7 7 0 1 0-14 0c0 5.4 7 12 7 12Z" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="9" r="2.5" stroke="currentColor" stroke-width="1.6"/></svg>
        <div><b data-i18n="showroom_label">Showroom</b><span data-i18n="side_address_v">Schwerzistrasse 34, 8807 Freienbach SZ, Schweiz</span></div>
      </div>
      <div class="contact-card reveal">
        <svg viewBox="0 0 24 24" fill="none"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.98.36 1.94.7 2.86a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.22-1.27a2 2 0 0 1 2.11-.45c.92.34 1.88.57 2.86.7A2 2 0 0 1 22 16.92Z" stroke="currentColor" stroke-width="1.6"/></svg>
        <div><b data-i18n="side_phone_l">Telefon</b><a href="tel:+41796689088">+41 79 668 90 88</a></div>
      </div>
      <div class="contact-card reveal">
        <svg viewBox="0 0 24 24" fill="none"><path d="M4 4h16v16H4z" stroke="currentColor" stroke-width="1.6"/><path d="m4 6 8 7 8-7" stroke="currentColor" stroke-width="1.6"/></svg>
        <div><b data-i18n="side_email_l">E-Mail</b><a href="mailto:info@e-suero.ch">info@e-suero.ch</a></div>
      </div>
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
<script src="../../i18n.js?v=20261101" defer></script>
<script src="../../main.js?v=20261101" defer></script>
<script src="../../assets/js/stripe-checkout.js?v=20260815" defer></script>
<script src="../../assets/js/sales-form.js?v=20261029" defer></script>
</body>
</html>
"""


def build_page(p, category, products):
    sd = spec_dict(p)
    canonical = f"{SITE}/fahrzeuge/{category['dir']}/{p['slug']}.html"
    has_price = bool(p.get("price_rappen"))
    if p.get("colors"):
        main_img = p["color_imgs"][p["colors"][0]]
        og_image = f"{SITE}/assets/images/products/{main_img}"
    else:
        main_img = None
        og_image = f"{SITE}/assets/images/logo-mark-320.png"
    a1 = is_a1(p)
    speed = sd.get("Höchstgeschwindigkeit", "")
    title = p.get("seo_title") or f"{p['name']} kaufen Freienbach SZ | {speed} {category['name']} — E-Suero"
    price_phrase = chf(p['price_rappen']) + "." if has_price else "Preis auf Anfrage."
    description = p.get("meta_description") or (
        f"{p['name']} bei E-Suero in Freienbach SZ: {speed}, {p['voltage']}, "
        f"{price_phrase} {'Kat. A1' if a1 else ''} "
        f"Beratung, Probefahrt und Kauf direkt beim Fachhändler.").replace("  ", " ")

    benefits = []
    fs_lower = sd.get("Führerschein", "").lower()
    if "nicht erforderlich" in fs_lower:
        benefits.append("Ohne Führerausweis-Pflicht fahrbereit")
    elif a1:
        benefits.append("Kat.-A1-Zulassung für höheres Tempo")
    elif fs_lower:
        benefits.append(f"Führerschein: {sd['Führerschein']}")
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
    if p["variants"]:
        chips = "".join(
            f'<button type="button" class="variant-chip{" is-active" if i==0 else ""}" '
            f'data-price-rappen="{v["price_rappen"]}" data-price-label="{esc(v["price_label"])}" '
            f'data-variant-label="{esc(v["label"])}">{esc(v["label"])}</button>'
            for i, v in enumerate(p["variants"])
        )
        variant_select = f'<div class="variant-select" role="radiogroup" aria-label="Variante wählen">{chips}</div>'

    practical_rows = "".join(f"{dt_html(k)}{dd_html(v)}" for k, v in practical_info_rows(p))

    faq_html_parts = []
    for i, (q, a) in enumerate(faq_items(p, category)):
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
            for q, a in faq_items(p, category)
        ],
    }
    breadcrumb_jsonld = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "E-Suero", "item": f"{SITE}/index.html"},
            {"@type": "ListItem", "position": 2, "name": "Alle Fahrzeuge", "item": f"{SITE}/verkauf/index.html"},
            {"@type": "ListItem", "position": 3, "name": category["name"], "item": f"{SITE}/{category['landing']}"},
            {"@type": "ListItem", "position": 4, "name": p["name"], "item": canonical},
        ],
    }
    product_jsonld = {
        "@context": "https://schema.org", "@type": "Product",
        "name": f"E-Suero {p['name']}",
        "description": description,
        "category": category["name"],
        "image": og_image,
        "brand": {"@type": "Brand", "name": "E-Suero"},
    }
    if has_price:
        product_jsonld["offers"] = {
            "@type": "Offer", "priceCurrency": "CHF",
            "price": "{:.2f}".format(p["price_rappen"] / 100),
            "availability": "https://schema.org/InStock",
            "url": canonical,
        }
    jsonld = json.dumps([product_jsonld, breadcrumb_jsonld, faq_jsonld], ensure_ascii=False, indent=2)

    header = sales_chrome.header_html("../../", "#modell-kontakt", category["landing"])
    mobile_nav = sales_chrome.mobile_nav_html("../../", "#modell-kontakt", category["landing"])
    footer = sales_chrome.footer_html("../../")

    colors_line = f' · Farben: {esc(", ".join(p["colors"]))}' if p.get("colors") else ""
    media_block = media_html(p, category, "product-media model-media", f'{category["name"]} kaufen Freienbach SZ')

    marketing_section = ""
    if p.get("marketing_body"):
        disclaimer = f'<p style="color:var(--c-mute-2);font-size:.82rem;margin-top:1rem">{esc(p.get("range_disclaimer",""))}</p>' if p.get("range_disclaimer") else ""
        marketing_section = (
            '<section class="section-tight"><div class="container">'
            '<div class="section-head"><span class="eyebrow" data-i18n="model_about_eyebrow">Über dieses Modell</span>'
            f'<h2 data-i18n="product_{p["slug"]}_intro">{esc(p.get("marketing_intro", ""))}</h2></div>'
            f'<p class="reveal" style="color:var(--c-mute);max-width:72ch" data-i18n="product_{p["slug"]}_body">{esc(p["marketing_body"])}</p>'
            f'{disclaimer}'
            '</div></section>'
        )
    gallery_section = ""
    if p.get("gallery_imgs"):
        thumbs = "".join(
            f'<img src="{IMG_BASE}{fname}?v=20261026" alt="E-Suero {esc(p["name"])} — {esc(alt)}" width="600" height="600" loading="lazy">'
            for fname, alt in p["gallery_imgs"]
        )
        gallery_section = (
            '<section class="section-tight"><div class="container">'
            '<div class="section-head"><span class="eyebrow">Galerie</span>'
            '<h2>Innenraum &amp; Details.</h2></div>'
            f'<div class="detail-gallery reveal-stagger reveal">{thumbs}</div>'
            '</div></section>'
        )
    footnotes = ""
    if p.get("footnotes"):
        items = "".join(f'<p style="color:var(--c-mute-2);font-size:.78rem;margin-top:.4rem">{esc(f)}</p>' for f in p["footnotes"])
        footnotes = f'<div style="margin-top:1rem">{items}</div>'
    if has_price:
        buy_button = '<button type="button" class="btn btn-primary magnetic" data-buy-btn data-i18n="buy_now">Jetzt kaufen</button>'
        buy_price_rappen = p["variants"][0]["price_rappen"] if p["variants"] else p["price_rappen"]
        buy_attrs = (f' data-buy-name="{esc(p["name"])}" data-buy-price="{buy_price_rappen}" '
                     f'data-buy-img="{SITE}/assets/images/products/{main_img}" data-buy-slug="{p["slug"]}"')
    else:
        buy_button = '<a href="#modell-kontakt" data-reason="angebot" class="btn btn-primary magnetic" data-i18n="cta_angebot">Angebot anfragen</a>'
        buy_attrs = ""

    html_out = PAGE_TMPL.format(
        title=esc(title), title_js=title.replace('"', '\\"'),
        description=esc(description), description_js=description.replace('"', '\\"'),
        canonical=canonical, og_image=og_image,
        jsonld=jsonld,
        header=header, mobile_nav=mobile_nav, footer=footer,
        landing=category["landing"], category_name=esc(category["name"]),
        category_i18n_key=NAME_I18N_KEY.get(category["name"], ""),
        name=esc(p["name"]), name_attr=esc(p["name"]), buy_attrs=buy_attrs,
        IMG_BASE=IMG_BASE, media_block=media_block,
        swatches=color_swatches_html(p),
        badge0=esc(p["badges"][0]),
        voltage=esc(p["voltage"]), colors_line=colors_line,
        variant_select=variant_select,
        price_block=price_block_html(p, extra_style="font-size:2rem;display:block;margin:.6rem 0 1rem"),
        needs_text=(
            f'<p style="color:var(--c-mute);max-width:56ch" data-i18n="product_{p["slug"]}_lead">{esc(p["lead_text"])}</p>'
            if p.get("lead_text") else
            f'<p style="color:var(--c-mute);max-width:56ch">{needs_text(p, category)}</p>'
        ),
        benefits=benefits_html,
        buy_button=buy_button,
        trust_block=trust_block_html("../../"),
        marketing_section=marketing_section,
        gallery_section=gallery_section,
        practical_rows=practical_rows,
        differences=differences_text(p, products),
        full_spec=spec_table_html(p),
        footnotes=footnotes,
        faq_html=faq_html,
        slug=p["slug"],
    )
    return html_out


def generate(products, category, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for p in products:
        out_path = os.path.join(out_dir, f"{p['slug']}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(build_page(p, category, products))
        print("wrote", out_path)
