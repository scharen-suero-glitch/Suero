====================================================
E-SUERO WEBSITE — DEPLOYMENT INSTRUCTIONS (HOSTINGER)
====================================================

This package contains the complete, production-ready E-Suero website.
Pure HTML / CSS / JavaScript — no build step, no npm, no server-side code
required. It is ready to upload directly to Hostinger.

----------------------------------------------------
HOW TO DEPLOY
----------------------------------------------------

1. Log into Hostinger (hpanel.hostinger.com).

2. Open File Manager (under "Files" in the left menu).

3. Open the "public_html" folder. This is the web root for esuero.ch.

4. Delete the default files if any exist (e.g. Hostinger's placeholder
   index.html, "default.php", or a sample index page). Do NOT delete
   public_html itself — only its contents.

5. Upload "E-Suero-Website.zip" into public_html, then right-click it
   in File Manager and choose "Extract". Extract it directly into
   public_html (not into a new subfolder).

6. Verify that index.html is located directly inside public_html —
   i.e. the path is public_html/index.html, NOT
   public_html/E-Suero-Website/index.html. If the ZIP extracted into
   its own subfolder, move all the files and folders up one level into
   public_html, then delete the now-empty subfolder.

7. Visit https://esuero.ch to confirm the website is live.

That's it — no database, no environment variables, no build command.
Every asset (fonts, scripts, images, icons) is self-contained inside
this package and loads via relative paths, so it works immediately
after extraction, from any folder depth, without edits.

----------------------------------------------------
WHAT'S INSIDE
----------------------------------------------------

index.html          Homepage (all sections: hero, about, products,
                     workshop, battery lab, process timeline, brands,
                     before/after, gallery, reviews, FAQ, contact)
styles.css           All styles
main.js              All site interactivity (GSAP animations, menu,
                     language switcher, forms, sliders, etc.)
i18n.js              German/English/Italian/Spanish translations
manifest.json        PWA manifest (home-screen icon support on mobile)
robots.txt           Search engine crawl rules
sitemap.xml          Sitemap for search engines
.htaccess            Apache config: HTTPS redirect, clean URLs,
                     caching, compression, security headers
favicon.ico          Browser tab icon (legacy format)

legal/               Datenschutz (privacy), Impressum, and AGB (terms)
                     pages, linked from the homepage footer

lib/                 Third-party JavaScript libraries used by the site
                     (GSAP + ScrollTrigger — self-hosted, no external
                     CDN dependency)

assets/
  fonts/             Self-hosted Inter + Space Grotesk webfonts
  icons/             Favicon, apple-touch-icon, and PWA icons
  images/            Logo mark images (PNG + WebP)

----------------------------------------------------
BEFORE YOU GO LIVE — THINGS TO DOUBLE-CHECK
----------------------------------------------------

- Domain: the site expects to be served at https://esuero.ch (this is
  set in the canonical URL, sitemap.xml, robots.txt, and structured
  data). If the domain differs, update these references accordingly.

- Google Maps: the contact section embeds a Google Maps iframe for
  Schwerzistrasse 34, 8807 Freienbach SZ. It works automatically once
  the site is live on a public domain — no API key needed for the
  basic embed used here.

- WhatsApp / phone / email: all point to +41 79 668 90 88 and
  info@esuero.ch. Update these in index.html (and the legal pages) if
  they ever change.

- Contact form: the form validates input in the browser and opens the
  visitor's email client with a pre-filled message (via a mailto:
  link) — there is no server-side form handler. If you'd prefer
  messages to arrive without relying on the visitor's own email
  client, connect a form backend (e.g. Hostinger's own form handling,
  or a service like Formspree) later on.

- SSL: Hostinger issues a free SSL certificate per domain. Make sure
  it's active (hPanel → SSL) — the .htaccess file already forces all
  traffic to HTTPS.

----------------------------------------------------
SUPPORT
----------------------------------------------------

If a page looks unstyled or a section is missing after upload, the
most common cause is the ZIP having extracted one folder too deep
(see step 6 above) — double check that index.html, styles.css, and
the assets/lib/legal folders sit directly inside public_html.
