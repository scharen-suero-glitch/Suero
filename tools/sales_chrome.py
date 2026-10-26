# -*- coding: utf-8 -*-
"""Shared header/nav/footer for the sales section (verkauf/, fahrzeuge/*).

The sales section is deliberately self-contained: no Werkstatt, no
Batterie-Labor, no "Über uns" in its nav or footer — only vehicle
categories, the sales contact, and the legally-required footer links.
`base` is the relative path back to the site root ("../" from
fahrzeuge/e-roller.html or verkauf/index.html, "../../" from
fahrzeuge/e-roller/<slug>.html).
"""

CATEGORIES = [
    ("E-Roller", "fahrzeuge/e-roller.html", "nav_e_roller"),
    ("E-Motorräder", "fahrzeuge/e-motorraeder.html", "nav_e_motorraeder"),
    ("E-Scooter", "fahrzeuge/e-scooter.html", "nav_e_scooter"),
    ("E-Bike", "fahrzeuge/e-bike.html", "nav_e_bike"),
    ("E-Minicar", "fahrzeuge/e-minicar.html", "nav_e_minicar"),
]


def nav_links(base, current_href=None):
    links = []
    for name, href, i18n_key in CATEGORIES:
        full = base + href
        active = ' aria-current="page"' if href == current_href else ""
        links.append(f'<a href="{full}"{active} data-i18n="{i18n_key}">{name}</a>')
    return "\n      ".join(links)


def header_html(base, cta_href, current_href=None):
    return f"""<header class="site-header">
  <div class="container">
    <a href="{base}index.html" class="logo">
      <picture>
        <source srcset="{base}assets/images/logo-mark-160.webp 1x, {base}assets/images/logo-mark-320.webp 2x" type="image/webp">
        <img class="logo-mark" src="{base}assets/images/logo-mark-160.png" srcset="{base}assets/images/logo-mark-320.png 2x" alt="" width="38" height="38" loading="eager">
      </picture>
      <b>E</b>-SUERO
    </a>

    <nav class="nav-desktop" aria-label="Fahrzeug-Kategorien">
      {nav_links(base, current_href)}
      <a href="{base}leistungen/werkstatt.html" class="nav-werkstatt-link" data-i18n="nav_werkstatt_short">Werkstatt</a>
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
      <a href="{cta_href}" data-reason="probefahrt" class="btn btn-primary btn-sm magnetic" data-i18n="nav_cta_probefahrt">Probefahrt anfragen</a>
      <button class="burger" type="button" aria-label="Menü öffnen" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>"""


def mobile_nav_html(base, cta_href, current_href=None):
    cat_links = "\n  ".join(
        f'<a href="{base}{href}" data-i18n="{i18n_key}">{name}</a>' for name, href, i18n_key in CATEGORIES
    )
    return f"""<div class="mobile-nav">
  <a href="{base}verkauf/index.html" data-i18n="nav_all_vehicles">Alle Fahrzeuge</a>
  {cat_links}
  <a href="{base}leistungen/werkstatt.html" data-i18n="nav_werkstatt_short">Werkstatt</a>
  <a href="{cta_href}" data-reason="probefahrt" class="btn btn-primary" data-i18n="nav_cta_probefahrt">Probefahrt anfragen</a>
</div>"""


def footer_html(base):
    cat_links = "\n        ".join(
        f'<a href="{base}{href}" data-i18n="{i18n_key}">{name}</a>' for name, href, i18n_key in CATEGORIES
    )
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <a href="{base}index.html" class="logo">
          <picture>
            <source srcset="{base}assets/images/logo-mark-160.webp 1x, {base}assets/images/logo-mark-320.webp 2x" type="image/webp">
            <img class="logo-mark" src="{base}assets/images/logo-mark-160.png" srcset="{base}assets/images/logo-mark-320.png 2x" alt="" width="38" height="38" loading="lazy">
          </picture>
          <b>E</b>-SUERO
        </a>
        <p data-i18n="footer_sales_desc">Premium Elektrofahrzeuge in Freienbach SZ — E-Roller, E-Motorräder, E-Scooter, E-Bike und E-Minicar.</p>
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
        <h3 data-i18n="footer_vehicles_h">Fahrzeuge</h3>
        {cat_links}
      </div>
      <div class="footer-col">
        <h3 data-i18n="footer_buy_h">Kauf</h3>
        <a href="{base}verkauf/index.html" data-i18n="nav_all_vehicles">Alle Fahrzeuge</a>
        <a href="{base}verkauf/bestell-lieferprozess.html" data-i18n="footer_order_delivery">Bestell- &amp; Lieferprozess</a>
        <a href="{base}verkauf/gebraucht-geprueft.html" data-i18n="used_catalog_link">Geprüft gebraucht</a>
      </div>
      <div class="footer-col">
        <h3 data-i18n="footer_col3_h">Rechtliches</h3>
        <a href="{base}legal/privacy.html" data-i18n="fc3_1">Datenschutz</a>
        <a href="{base}legal/impressum.html" data-i18n="fc3_2">Impressum</a>
        <a href="{base}legal/terms.html" data-i18n="fc3_3">AGB</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span id="year">2026</span> E-Suero. <span data-i18n="footer_rights">Alle Rechte vorbehalten.</span></span>
      <div class="legal-links">
        <a href="{base}legal/privacy.html" data-i18n="fc3_1">Datenschutz</a>
        <a href="{base}legal/impressum.html" data-i18n="fc3_2">Impressum</a>
        <a href="{base}legal/terms.html" data-i18n="fc3_3">AGB</a>
      </div>
    </div>
  </div>
</footer>"""
