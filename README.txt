====================================================
E-SUERO WEBSITE — DEPLOYMENT INSTRUCTIONS (HOSTINGER)
====================================================

This package contains the complete, production-ready E-Suero website:
the full catalog (E-Motorräder, E-Roller 20+45 km/h, E-Bike 20+45 km/h,
E-Scooter), live Stripe checkout, search/filters/wishlist/comparison,
and all SEO/structured data. Pure HTML/CSS/JavaScript with a small PHP
backend for payments — no build step, no npm, no database.

----------------------------------------------------
HOW TO DEPLOY
----------------------------------------------------

1. Log into Hostinger (hpanel.hostinger.com).

2. Open File Manager (under "Files" in the left menu).

3. Open the "public_html" folder. This is the web root for e-suero.ch.

4. Delete the default files if any exist (e.g. Hostinger's placeholder
   index.html, "default.php", or a sample index page). Do NOT delete
   public_html itself — only its contents.

5. Upload the ZIP into public_html, then right-click it in File
   Manager and choose "Extract". Extract it directly into public_html
   (not into a new subfolder).

6. Verify that index.html is located directly inside public_html —
   i.e. the path is public_html/index.html, NOT
   public_html/e-suero/index.html. If the ZIP extracted into its own
   subfolder, move all files and folders up one level into
   public_html, then delete the now-empty subfolder.

7. Open stripe/config.php in File Manager's code editor. Find this
   line near the top:

     define('STRIPE_SECRET_KEY', 'sk_live_REPLACE_WITH_YOUR_STRIPE_SECRET_KEY');

   Replace the placeholder with your real Stripe LIVE secret key
   (starts with sk_live_...), from https://dashboard.stripe.com/apikeys.
   Save the file. This is the only manual step required — every other
   Stripe file reads its configuration from this one file, and the
   entire checkout flow (order metadata, success page, error handling)
   is already built and wired up.

8. Visit https://e-suero.ch to confirm the website is live, and place
   a small real test purchase to confirm Stripe is working end to end.

That's it — no environment variables, no build command. Every asset
(fonts, scripts, images, icons) is self-contained inside this package
and loads via relative paths.

----------------------------------------------------
WHAT'S INSIDE
----------------------------------------------------

index.html            Homepage (hero, about, products catalog with
                       tabs, workshop, battery lab, gallery, reviews,
                       FAQ, contact)
styles.css             All styles
main.js                Core site interactivity (GSAP animations, menu,
                       language switcher, forms, tabs, carousels, etc.)
i18n.js                German/English/Italian/Spanish translations
manifest.json          PWA manifest (home-screen icon support on mobile)
robots.txt              Search engine crawl rules
sitemap.xml             Sitemap for search engines
.htaccess               Apache config: HTTPS redirect, clean URLs,
                       caching, compression
favicon.ico             Browser tab icon (legacy format)

fahrzeuge/              Dedicated sales pages per category:
                       e-motorraeder.html, e-roller.html, e-bike.html,
                       e-scooter.html — each with its own SEO
                       title/description, Open Graph, Twitter Card,
                       and Product/ItemList structured data (JSON-LD).

leistungen/              Service pages (diagnostics, battery repair,
                       controller repair, fleet maintenance, workshop,
                       premium care).

verkauf/                 Gebraucht & Geprüft (used-vehicle) catalog —
                       driven entirely by assets/js/gebraucht-katalog.js.

legal/                   Datenschutz (privacy), Impressum, AGB (terms).

lib/                     Third-party JS used by the site (GSAP +
                       ScrollTrigger — self-hosted, no external CDN).

stripe/                  Payment backend:
    config.php                    Stripe secret key + shared settings.
                                  The ONLY file you edit (step 7 above).
    create-checkout-session.php   Creates a Stripe Embedded Checkout
                                  session for whichever product the
                                  visitor clicks "Jetzt kaufen" on.
    success.php                  Post-payment confirmation page.
                                  Verifies payment status directly with
                                  Stripe, logs the order to orders.log,
                                  and emails info@e-suero.ch.
    .htaccess                    Blocks direct web access to *.log
                                  files (they contain customer emails).
    orders.log / error.log       Created automatically at runtime —
                                  do not create these manually.

assets/
  fonts/                Self-hosted Inter + Space Grotesk webfonts
  icons/                Favicon, apple-touch-icon, and PWA icons
  images/                Logo mark images (PNG + WebP)
  images/products/       Product photos for every vehicle in the
                       catalog (studio white-background treatment)
  js/
    catalog-tools.js     Search, filters, wishlist, and comparison —
                       auto-applies to every product card site-wide.
    stripe-checkout.js   Opens the embedded Stripe checkout modal.
    gebraucht-katalog.js Drives the used-vehicle catalog (see below).

----------------------------------------------------
UPDATING PRODUCTS / PRICES / SPECS
----------------------------------------------------

Every product card lives directly inside its category's HTML (index.html
for the homepage carousels, and the matching file in fahrzeuge/ for the
dedicated sales page). Each card is a self-contained block starting with
<div class="tilt-card">. To change a price, spec, or description, edit
the visible text inside that block — no other file needs touching.
Cards with more than one photographed color show clickable color dots
(<button class="color-dot" data-img="...">); add or remove a dot to
add/remove a color, pointing data-img at a photo already inside
assets/images/products/.

To add a brand-new product, copy an existing <div class="tilt-card">...
</div></div> block as a template, change its id, images, text and
data-buy-* attributes, and paste it into both index.html and the
matching fahrzeuge/ page (and JSON-LD block if you want it in search
results).

----------------------------------------------------
MANAGING THE "GEBRAUCHT & GEPRÜFT" CATALOG
----------------------------------------------------

Clicking the "Gebraucht geprüft" tab or visiting
verkauf/gebraucht-geprueft.html opens a dedicated browsing page:
Kategorie → Marke → Modell → Detailseite (Zustand + Werkstatt-Badges).

Everything is driven by ONE plain-text file — no database, no CMS:

  assets/js/gebraucht-katalog.js

To add a brand, a model, set a vehicle's condition, or turn the
"Kontrolliert" / "Geprüft" badges on or off, open that file in any text
editor and follow the instructions in its header comment.

----------------------------------------------------
BEFORE YOU GO LIVE — THINGS TO DOUBLE-CHECK
----------------------------------------------------

- Stripe secret key: see step 7 above — required for checkout to work.

- Stripe Dashboard payment methods: card is enabled by default. To
  offer TWINT, Apple Pay, Google Pay, Klarna or PayPal, enable them in
  Stripe Dashboard → Settings → Payment methods. No code changes
  needed — the checkout automatically offers whatever is enabled.

- Domain: the site expects to be served at https://e-suero.ch (set in
  canonical URLs, sitemap.xml, robots.txt, structured data, and the
  Stripe return URL in create-checkout-session.php). If the domain
  differs, update these references accordingly.

- Google Maps: the contact section embeds a Google Maps iframe for
  Schwerzistrasse 34, 8807 Freienbach SZ. Works automatically once the
  site is live on a public domain.

- WhatsApp / phone / email: all point to +41 79 668 90 88 and
  info@e-suero.ch. Update these in index.html (and the legal pages) if
  they ever change.

- Contact form: validates input in the browser and opens the visitor's
  email client with a pre-filled message (mailto:) — no server-side
  form handler.

- SSL: Hostinger issues a free SSL certificate per domain. Make sure
  it's active (hPanel → SSL) — .htaccess already forces HTTPS.

- PHP: stripe/ requires PHP with cURL enabled, which is standard on
  Hostinger shared hosting by default — no extra setup needed.

----------------------------------------------------
SUPPORT
----------------------------------------------------

If a page looks unstyled or a section is missing after upload, the
most common cause is the ZIP having extracted one folder too deep
(see step 6 above) — double check that index.html, styles.css, and
the assets/lib/legal/stripe folders sit directly inside public_html.

If checkout shows "Zahlung ist noch nicht konfiguriert", the Stripe
secret key placeholder in stripe/create-checkout-session.php and/or
stripe/success.php hasn't been replaced yet (step 7 above).
