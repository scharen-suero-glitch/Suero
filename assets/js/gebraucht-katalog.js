/* ==========================================================================
   E-SUERO — "Gebraucht & Geprüft" Katalog
   ==========================================================================
   Rein manuelle Datenquelle — keine Datenbank, kein CMS, kein Lagerbestand.

   SO FÜGEN SIE EINE NEUE MARKE / EIN NEUES MODELL HINZU:
   1. Marke:  brand("Markenname", [ ...Modelle... ]) in die passende
              Kategorie (CATALOG.brands) einfügen.
   2. Modell: m("Modellname") in die Modell-Liste der Marke einfügen.
   3. Zustand manuell setzen (optional, siehe CONDITIONS unten):
              m("Modellname", { condition: "like-new" })
   4. Werkstatt-Badges manuell ein-/ausschalten (optional, Standard = aus):
              m("Modellname", { condition: "good", controlled: true, approved: true })
   5. Foto hinzufügen (optional): Bild in assets/images/products/ hochladen,
              dann den Dateinamen eintragen:
              m("Modellname", { image: "../assets/images/products/xiaomi-4-ultra.jpg?v=20260801" })
              Das Foto erscheint in der Modell-Liste UND auf der Detailseite.
   6. Kurzbeschreibung hinzufügen (optional, z.B. Reichweite/Leistung):
              m("Modellname", { desc: "60 km Reichweite, 1'000 W Spitzenleistung." })

   Alle Felder lassen sich beliebig kombinieren:
   m("Modellname", { condition: "good", controlled: true, image: "...", desc: "..." })

   Kein Code, kein Layout muss dafür angepasst werden.
   ========================================================================== */
(function () {
  "use strict";

  var CONDITIONS = {
    "like-new": "Wie neu",
    "very-good": "Sehr gut",
    "good": "Gut",
    "fair": "Fahrbereit"
  };

  function slugify(str) {
    return String(str)
      .toLowerCase()
      .replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/(^-+|-+$)/g, "");
  }

  function m(name, opts) {
    // href (optional): when a model has its own real published page (own
    // canonical/meta/JSON-LD — needed for SEO-eligible listings), link
    // straight to it instead of the internal hash-routed detail view.
    // price/badges (optional): shown on the model card when set.
    // available (optional, default true): set to false the moment a unit
    // sells — it's then skipped from the listing instead of staying
    // announced as buyable.
    return Object.assign({ name: name, condition: "", controlled: false, approved: false, available: true }, opts || {});
  }
  function brand(name, models, opts) {
    // opts.image (optional): shown on the brand-selection card so a buyer
    // recognizes the vehicle at a glance instead of skipping a text-only tile.
    return Object.assign({ name: name, models: models || [] }, opts || {});
  }
  function category(name, brands) {
    return { name: name, brands: brands || [] };
  }

  var CATALOG = {
    "e-scooter": category("E-Scooter", [
      brand("Xiaomi", [
        m("Xiaomi 4 Ultra", { image: "../assets/images/products/xiaomi-4-ultra.jpg?v=20260801", desc: "Bis zu 70 km Reichweite und 940 W Spitzenleistung — der reichweitenstärkste Scooter der Serie, mit Doppelfederung für Komfort." }),
        m("Xiaomi 5 Pro", { image: "../assets/images/products/xiaomi-5-pro.jpg?v=20260801", desc: "60 km Reichweite, 1'000 W Spitzenleistung und Trommelbremse mit E-ABS für kraftvolles, sicheres Bremsen." }),
        m("Xiaomi 5 Max", { image: "../assets/images/products/xiaomi-5-max.jpg?v=20260801", desc: "60 km Reichweite und 1'000 W Spitzenleistung bei robusten 10-Zoll-Reifen — für Steigungen bis 22%." }),
        m("Xiaomi 5", { image: "../assets/images/products/xiaomi-5.jpg?v=20260801", desc: "60 km Reichweite bei 350 W Nennleistung — die ausgewogene Mitte der aktuellen Xiaomi-Generation." }),
        m("Xiaomi 4 Pro Max", { image: "../assets/images/products/xiaomi-4-pro-max.jpg?v=20260801", desc: "60 km Reichweite, Doppel-Zylinder-Federung und pannensichere 10-Zoll-Reifen für den täglichen Einsatz." }),
        m("Xiaomi 4 Pro 2nd Gen", { image: "../assets/images/products/xiaomi-4-pro-2nd-gen.jpg?v=20260801", desc: "60 km Reichweite bei nur 19 kg Gewicht — überarbeitete Generation mit E-ABS-Bremssystem." }),
        m("Xiaomi Elite", { image: "../assets/images/products/xiaomi-elite.jpg?v=20260801", desc: "45 km Reichweite mit Doppelfederung vorne — komfortabel für längere Pendelstrecken." }),
        m("Xiaomi Mi 1S", { image: "../assets/images/products/xiaomi-mi-1s.jpg?v=20260801", desc: "30 km Reichweite bei nur 12.5 kg — der bewährte Allrounder für die letzte Meile." }),
        m("Xiaomi Mi Essential", { image: "../assets/images/products/xiaomi-mi-essential.jpg?v=20260801", desc: "20 km Reichweite und 12 kg Leichtgewicht — kompakter Einsteiger-Scooter für die Stadt." }),
        m("Xiaomi M365", { image: "../assets/images/products/xiaomi-m365.jpg?v=20260801", desc: "30 km Reichweite — der Klassiker, der die Elektro-Scooter-Bewegung 2016 mitbegründete." }),
        m("Xiaomi 4 Lite 2nd Gen", { image: "../assets/images/products/xiaomi-4-lite-2nd-gen.jpg?v=20260801", desc: "25 km Reichweite bei nur 16.2 kg — leicht, wendig und ideal für urbane Strecken." })
      ]),
      brand("Segway Ninebot", [
        m("Ninebot E22D"), m("Ninebot ES2"), m("Ninebot FDN"), m("Ninebot E2 Pro"), m("Ninebot Air T15E")
      ]),
      brand("SoFlow", [
        m("S03 2nd Gen"), m("S02 Zero"), m("S02 Air"), m("S04 Pro 2nd Gen"), m("S01")
      ]),
      brand("VMAX", [
        m("VX2 Pro STB"), m("VX2 Pro LTB"), m("VX2 Pro LT"), m("VX2 ST"),
        m("VX5 LT (2 Brake)"), m("VX5 LT (1 Brake)"), m("VX5 ST"), m("VX3"),
        m("VT36/30A"), m("JYX48500")
      ]),
      brand("Ocean Drive", [
        m("E8"), m("E8 Plus"), m("T4H"), m("S9 CFX"), m("S9"), m("M25H"), m("X9 Series")
      ]),
      brand("OKAI", [m("ES30")]),
      brand("Yadea", [m("KS5 Pro")]),
      brand("Easy Drive", [m("NABEE BDF")]),
      brand("Micro", [m("Merlin")]),
      brand("Acer", [m("Unknown Model")]),
      brand("FN", [m("FN-E5 Plus")]),
      brand("Tier", [m("SO MY TIER")]),
      brand("E-Trottinet", [m("Unknown Model")]),
      brand("GC", [m("Unknown Model")]),
      brand("Fenix", [m("Unknown Model")]),
      brand("Urban Glider", [m("Unknown Model")]),
      brand("Green Technology", [m("Pro")]),
      brand("Scooter Factory", [m("Unknown Model")]),
      brand("MPMAN", [m("Unknown Model")]),
      brand("Dock Green", [m("Unknown Model")]),
      brand("Augment", [m("Unknown Model")]),
      brand("Urban Mobility", [m("Unknown Model")]),
      brand("Eflow", [m("Unknown Model"), m("Eflow Lead Battery")]),
      brand("Uber Scoot", [m("S300")]),
      brand("Razor", [m("Unknown Model")])
      /* Weitere Marken: hier eine neue brand("Name", [ m("Modell") ]) Zeile einfügen. */
    ]),
    "e-bike": category("E-Bike", []),
    "e-roller": category("E-Roller", [
      brand("Vespino", [
        m("Vespino 7i Occasion – Schwarz", {
          href: "gebraucht/vespino-7i-schwarz.html",
          image: "../assets/images/products/vespino-7i-schwarz.jpg",
          price: "CHF 1'500.–",
          badges: ["Occasion", "Service durchgeführt", "6 Monate Garantie"]
        }),
        m("Vespino 7i Occasion – Weiss / roter Sitz", {
          href: "gebraucht/vespino-7i-weiss.html",
          image: "../assets/images/products/vespino-7i-weiss.jpg",
          price: "CHF 1'500.–",
          badges: ["Occasion", "Service durchgeführt", "6 Monate Garantie"]
        })
      ], { image: "../assets/images/products/vespino-7i-schwarz.jpg" })
    ]),
    "e-motorraeder": category("E-Motorräder", [])
  };

  // Custom header text for a given category/brand drill-down level —
  // falls back to the generic "Marke wählen."/"Modell wählen." text when
  // no override is set for that combination.
  var BRAND_HEADLINES = {
    "e-roller/vespino": {
      eyebrow: "E-Roller Occasion",
      title: "E-Roller Occasion in Freienbach",
      sub: "Entdecken Sie unsere gebrauchten Vespino 7i: Beide Fahrzeuge haben einen vollständigen mechanischen und elektronischen Service erhalten. Für CHF 1'500 pro Fahrzeug und mit 6 Monaten Garantie – persönlich beraten bei E-Suero in Freienbach SZ."
    }
  };

  var CATEGORY_ORDER = ["e-scooter", "e-bike", "e-roller", "e-motorraeder"];

  var CATEGORY_IMAGES = {
    "e-scooter": "../assets/images/products/scooter-category.jpg?v=20260801",
    "e-bike": "../assets/images/products/ebike-category.jpg?v=20260801",
    "e-roller": "../assets/images/products/eroller-next-nx1-schwarz.jpg?v=20260812",
    "e-motorraeder": "../assets/images/products/moto-category.jpg?v=20260801"
  };

  var CATEGORY_DESC = {
    "e-scooter": "Geprüfte Elektro-Scooter namhafter Marken.",
    "e-bike": "Geprüfte E-Bikes — Marken und Modelle folgen in Kürze.",
    "e-roller": "Geprüfte E-Roller Occasion — Vespino 7i verfügbar, weitere Marken folgen in Kürze.",
    "e-motorraeder": "Geprüfte Elektromotorräder — Marken und Modelle folgen in Kürze."
  };

  var root = document.getElementById("catalog-root");
  var crumbsEl = document.getElementById("catalog-crumbs");
  var eyebrowEl = document.getElementById("catalog-eyebrow");
  var titleEl = document.getElementById("catalog-title");
  var subEl = document.getElementById("catalog-sub");
  var metaDescEl = document.querySelector('meta[name="description"]');
  var ogTitleEl = document.querySelector('meta[property="og:title"]');
  var ogDescEl = document.querySelector('meta[property="og:description"]');
  if (!root) return;

  function esc(str) {
    return String(str).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  var CAT_NAME_KEY = {
    "E-Scooter": "nav_e_scooter",
    "E-Bike": "nav_e_bike",
    "E-Roller": "nav_e_roller",
    "E-Motorräder": "nav_e_motorraeder"
  };

  function currentLang() {
    try {
      var l = localStorage.getItem("esuero_lang");
      if (["de", "en", "it", "es"].indexOf(l) > -1) return l;
    } catch (e) {}
    return "de";
  }

  function t(key, fallback) {
    var dict = (window.__ESUERO_I18N__ || {})[currentLang()] || {};
    return dict[key] !== undefined ? dict[key] : fallback;
  }

  function catName(cat) {
    var key = CAT_NAME_KEY[cat.name];
    return key ? t(key, cat.name) : cat.name;
  }

  function condLabelFor(condition) {
    if (!condition) return "";
    var key = { "like-new": "cond_like_new", "very-good": "cond_very_good", "good": "cond_good", "fair": "cond_fair" }[condition];
    return key ? t(key, CONDITIONS[condition]) : CONDITIONS[condition];
  }

  function applyI18nScoped(el) {
    el.querySelectorAll("[data-i18n]").forEach(function (node) {
      var key = node.getAttribute("data-i18n");
      var val = t(key, undefined);
      if (val !== undefined) node.textContent = val;
    });
    el.querySelectorAll("[data-i18n-html]").forEach(function (node) {
      var key = node.getAttribute("data-i18n-html");
      var val = t(key, undefined);
      if (val !== undefined) node.innerHTML = val;
    });
  }

  function findCategory(catSlug) {
    return CATALOG[catSlug] || null;
  }
  function findBrand(cat, brandSlug) {
    for (var i = 0; i < cat.brands.length; i++) {
      if (slugify(cat.brands[i].name) === brandSlug) return cat.brands[i];
    }
    return null;
  }
  function findModel(brandObj, modelSlug) {
    var matches = brandObj.models.filter(function (mo) { return slugify(mo.name) === modelSlug; });
    if (matches.length <= 1) return matches[0] || null;
    /* Duplikate innerhalb derselben Marke: über Index disambiguieren (#slug--2, #slug--3, ...) */
    return matches[0] || null;
  }

  function setHead(eyebrow, title, sub, seoTitle, seoDesc) {
    if (eyebrowEl) eyebrowEl.textContent = eyebrow;
    if (titleEl) titleEl.textContent = title;
    if (subEl) subEl.textContent = sub;
    if (seoTitle) {
      document.title = seoTitle;
      window.__PAGE_META__ = { title: seoTitle, desc: seoDesc };
      if (ogTitleEl) ogTitleEl.setAttribute("content", seoTitle);
    }
    if (seoDesc) {
      if (metaDescEl) metaDescEl.setAttribute("content", seoDesc);
      if (ogDescEl) ogDescEl.setAttribute("content", seoDesc);
    }
  }

  function setCrumbs(items) {
    if (!crumbsEl) return;
    var html = items.map(function (it, idx) {
      if (idx === items.length - 1) return '<span class="is-current">' + esc(it.label) + "</span>";
      return '<a href="' + it.href + '">' + esc(it.label) + "</a><span>/</span>";
    }).join("");
    crumbsEl.innerHTML = html;
  }

  function renderCategories() {
    setCrumbs([{ label: t("used_catalog_title", "Gebraucht & Geprüft"), href: "#/" }]);
    setHead(t("used_sales_eyebrow", "Verkauf"), t("used_catalog_title", "Gebraucht & Geprüft"), t("used_home_sub", "Sorgfältig geprüfte Gebrauchtfahrzeuge aus unserer Werkstatt in Freienbach — nach Kategorie wählen."),
      "Gebrauchte E-Fahrzeuge kaufen Freienbach SZ | E-Suero",
      "Geprüfte Gebraucht-Elektrofahrzeuge von E-Suero in Freienbach SZ: E-Scooter, E-Bikes, E-Roller und Elektromotorräder nach Marke und Modell kaufen.");
    var html = '<div class="value-grid reveal-stagger is-visible">';
    CATEGORY_ORDER.forEach(function (slug) {
      var cat = CATALOG[slug];
      html += '<a class="value-card catalog-card" href="#/' + slug + '">' +
        '<div class="product-media"><img src="' + CATEGORY_IMAGES[slug] + '" alt="' + esc(cat.name) + '" width="1200" height="800" loading="lazy"></div>' +
        "<h3>" + esc(catName(cat)) + "</h3>" +
        "<p>" + esc(t("cat_desc_" + slug, CATEGORY_DESC[slug])) + "</p>" +
        "</a>";
    });
    html += "</div>";
    root.innerHTML = html;
  }

  function renderBrands(catSlug) {
    var cat = findCategory(catSlug);
    if (!cat) { renderCategories(); return; }
    var catLabel = catName(cat);
    setCrumbs([
      { label: t("used_catalog_title", "Gebraucht & Geprüft"), href: "#/" },
      { label: catLabel, href: "#/" + catSlug }
    ]);
    setHead(t("used_catalog_title", "Gebraucht & Geprüft"), catLabel, t("used_pick_brand", "Marke wählen."),
      cat.name + " gebraucht kaufen Freienbach SZ | E-Suero",
      "Gebrauchte " + cat.name + " geprüft und einsatzbereit bei E-Suero in Freienbach SZ — Marke wählen und passendes Modell finden.");

    if (!cat.brands.length) {
      var emptyMsg = t("used_cat_empty", "Diese Kategorie wird in Kürze mit Marken und Modellen befüllt. Bitte kontaktieren Sie uns direkt für aktuelle %CAT%-Angebote.").replace("%CAT%", esc(catLabel));
      root.innerHTML = '<div class="catalog-empty"><p>' + emptyMsg + '</p>' +
        '<a href="../index.html#contact" class="btn btn-ghost btn-sm">' + esc(t("used_contact_cta", "Kontakt aufnehmen")) + '</a></div>';
      return;
    }

    var html = '<div class="brand-grid is-visible">';
    cat.brands.forEach(function (b) {
      var bSlug = slugify(b.name);
      var count = b.models.length;
      html += '<a class="brand-card" href="#/' + catSlug + "/" + bSlug + '">' +
        (b.image ? '<div class="product-media"><img src="' + esc(b.image) + '" alt="' + esc(b.name) + '" width="960" height="640" loading="lazy"></div>' : "") +
        "<h3>" + esc(b.name) + "</h3>" +
        '<span class="brand-card-count">' + count + " " + esc(count === 1 ? t("used_model_singular", "Modell") : t("used_model_plural", "Modelle")) + "</span>" +
        "</a>";
    });
    html += '</div><p class="catalog-note">+ ' + esc(t("used_more_brands", "Weitere Marken folgen in Kürze.")) + '</p>';
    root.innerHTML = html;
  }

  function renderModels(catSlug, brandSlug) {
    var cat = findCategory(catSlug);
    if (!cat) { renderCategories(); return; }
    var b = findBrand(cat, brandSlug);
    if (!b) { renderBrands(catSlug); return; }
    var catLabel = catName(cat);
    setCrumbs([
      { label: t("used_catalog_title", "Gebraucht & Geprüft"), href: "#/" },
      { label: catLabel, href: "#/" + catSlug },
      { label: b.name, href: "#/" + catSlug + "/" + brandSlug }
    ]);
    var headline = BRAND_HEADLINES[catSlug + "/" + brandSlug];
    if (headline) {
      setHead(headline.eyebrow, headline.title, headline.sub,
        headline.title + " | E-Suero", headline.sub);
    } else {
      setHead(catLabel, b.name, t("used_pick_model", "Modell wählen."),
        b.name + " " + cat.name + " gebraucht kaufen | E-Suero Freienbach SZ",
        "Geprüfte gebrauchte " + b.name + " " + cat.name + " bei E-Suero in Freienbach SZ — alle verfügbaren Modelle im Überblick.");
    }

    var availableModels = b.models.filter(function (mo) { return mo.available !== false; });
    if (!availableModels.length) {
      root.innerHTML = '<div class="catalog-empty"><p>' + esc(t("used_cond_inquiry", "Zustand auf Anfrage")) + '</p>' +
        '<a href="../index.html#contact" class="btn btn-ghost btn-sm">' + esc(t("used_contact_cta", "Kontakt aufnehmen")) + '</a></div>';
      return;
    }

    var html = '<div class="model-grid is-visible">';
    availableModels.forEach(function (mo) {
      var mSlug = slugify(mo.name);
      var condLabel = condLabelFor(mo.condition);
      var desc = mo.desc ? t("xiaomi_desc_" + mo.name, mo.desc) : "";
      var href = mo.href ? mo.href : "#/" + catSlug + "/" + brandSlug + "/" + mSlug;
      var badgesHtml = (mo.badges || []).map(function (bd, i) {
        return '<span class="badge' + (i === 0 ? "" : " ok") + '">' + esc(bd) + "</span>";
      }).join("");
      html += '<a class="model-card" href="' + esc(href) + '">' +
        (mo.image ? '<div class="product-media"><img src="' + esc(mo.image) + '" alt="' + esc(mo.name) + '" width="960" height="640" loading="lazy"></div>' : "") +
        "<h3>" + esc(mo.name) + "</h3>" +
        (desc ? '<p class="model-desc">' + esc(desc) + "</p>" : "") +
        (badgesHtml ? '<div class="catalog-badges" style="margin:.6rem 0">' + badgesHtml + "</div>" :
          (condLabel ? '<span class="badge ok">' + esc(condLabel) + "</span>" : '<span class="badge">' + esc(t("used_cond_inquiry", "Zustand auf Anfrage")) + "</span>")) +
        (mo.price ? '<span class="price" style="display:block;margin-top:.6rem">' + esc(mo.price) + "</span>" : "") +
        (mo.href ? '<div style="margin-top:1rem"><span class="btn btn-ghost btn-sm magnetic">Fahrzeug ansehen</span></div>' : "") +
        "</a>";
    });
    html += "</div>";
    root.innerHTML = html;
  }

  function renderDetail(catSlug, brandSlug, modelSlug) {
    var cat = findCategory(catSlug);
    if (!cat) { renderCategories(); return; }
    var b = findBrand(cat, brandSlug);
    if (!b) { renderBrands(catSlug); return; }
    var mo = findModel(b, modelSlug);
    if (!mo) { renderModels(catSlug, brandSlug); return; }

    var catLabel = catName(cat);
    setCrumbs([
      { label: t("used_catalog_title", "Gebraucht & Geprüft"), href: "#/" },
      { label: catLabel, href: "#/" + catSlug },
      { label: b.name, href: "#/" + catSlug + "/" + brandSlug },
      { label: mo.name, href: "#/" + catSlug + "/" + brandSlug + "/" + modelSlug }
    ]);
    var desc = mo.desc ? t("xiaomi_desc_" + mo.name, mo.desc) : "";
    var detailDesc = (desc ? desc + " " : "") + "Geprüft und einsatzbereit — gebraucht kaufen bei E-Suero in Freienbach SZ.";
    var fullModelName = mo.name.toLowerCase().indexOf(b.name.toLowerCase()) === 0 ? mo.name : b.name + " " + mo.name;
    setHead(catLabel + " · " + b.name, mo.name, "",
      fullModelName + " gebraucht kaufen Freienbach SZ | E-Suero",
      detailDesc);

    var condLabel = mo.condition ? condLabelFor(mo.condition) : t("used_cond_onrequest", "Auf Anfrage");
    var badges = '<span class="badge ok">' + esc(t("used_cond_prefix", "Zustand:")) + " " + esc(condLabel) + "</span>";
    if (mo.controlled) badges += '<span class="badge ok">✓ ' + esc(t("used_badge_controlled", "Kontrolliert")) + "</span>";
    if (mo.approved) badges += '<span class="badge ok">✓ ' + esc(t("used_badge_approved", "Geprüft")) + "</span>";

    root.innerHTML =
      '<div class="tilt-card catalog-detail"><div class="tilt-card-inner">' +
      (mo.image ? '<div class="product-media"><img src="' + esc(mo.image) + '" alt="' + esc(mo.name) + '" width="960" height="640" loading="eager"></div>' : "") +
      '<span class="eyebrow">' + esc(catLabel) + "</span>" +
      "<h2>" + esc(b.name) + " — " + esc(mo.name) + "</h2>" +
      (desc ? '<p class="model-desc">' + esc(desc) + "</p>" : "") +
      '<span class="price">' + esc(t("p_u3_p", "Preis auf Anfrage")) + "</span>" +
      '<div class="catalog-badges">' + badges + "</div>" +
      '<a href="../index.html#contact" class="btn btn-primary magnetic">' + esc(t("request_now", "Jetzt anfragen")) + "</a>" +
      trustBlockHtml() +
      "</div></div>";
    applyI18nScoped(root);
  }

  function trustBlockHtml() {
    return '<div class="trust-block reveal">' +
      '<div class="trust-block-head">' +
      '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M14.7 6.3a3 3 0 0 0-4.24 4.24L4 17v3h3l6.46-6.46a3 3 0 0 0 4.24-4.24l-2.3-2.3-1.4 1.4 1.4 1.4-1.06 1.06-1.4-1.4 1.4-1.4-2.3-2.3Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>' +
      "<div>" +
      '<h3 data-i18n="trust_title">Auch nach dem Kauf für Sie da.</h3>' +
      '<p data-i18n="trust_body">Bei E-Suero haben Sie einen persönlichen Ansprechpartner und eine eigene Werkstatt in Freienbach. Ob Wartung, Reparatur oder Fragen zu Ihrem Fahrzeug: Wir unterstützen Sie auch nach der Übergabe.</p>' +
      "</div></div>" +
      '<ul class="trust-block-list">' +
      '<li><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 12.5l4.5 4.5L20 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span data-i18n="trust_item_workshop">Eigene Werkstatt in Freienbach</span></li>' +
      '<li><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 12.5l4.5 4.5L20 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span data-i18n="trust_item_contact">Persönlicher Ansprechpartner</span></li>' +
      '<li><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 12.5l4.5 4.5L20 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span data-i18n="trust_item_onsite">Wartung und Reparatur vor Ort</span></li>' +
      "</ul>" +
      '<a href="../leistungen/werkstatt.html" class="trust-block-link" data-i18n="trust_link">Unsere Werkstatt kennenlernen →</a>' +
      "</div>";
  }

  function render() {
    var hash = window.location.hash.replace(/^#\/?/, "");
    var parts = hash.split("/").filter(Boolean).map(decodeURIComponent);
    if (parts.length === 0) return renderCategories();
    if (parts.length === 1) return renderBrands(parts[0]);
    if (parts.length === 2) return renderModels(parts[0], parts[1]);
    return renderDetail(parts[0], parts[1], parts[2]);
  }

  function routeOnNavigation() {
    render();
    var anchor = crumbsEl || root;
    window.scrollTo({ top: anchor.getBoundingClientRect().top + window.scrollY - 110, behavior: "smooth" });
  }

  window.addEventListener("hashchange", routeOnNavigation);
  document.addEventListener("DOMContentLoaded", render);
  document.addEventListener("esuero:langchange", render);
})();
