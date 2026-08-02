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
    return Object.assign({ name: name, condition: "", controlled: false, approved: false }, opts || {});
  }
  function brand(name, models) {
    return { name: name, models: models || [] };
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
    "e-roller": category("E-Roller", []),
    "e-motorraeder": category("E-Motorräder", [])
  };

  var CATEGORY_ORDER = ["e-scooter", "e-bike", "e-roller", "e-motorraeder"];

  var CATEGORY_IMAGES = {
    "e-scooter": "../assets/images/products/scooter-category.jpg?v=20260801",
    "e-bike": "../assets/images/products/ebike-category.jpg?v=20260801",
    "e-roller": "../assets/images/products/eroller-category.jpg?v=20260801",
    "e-motorraeder": "../assets/images/products/moto-category.jpg?v=20260801"
  };

  var CATEGORY_DESC = {
    "e-scooter": "Geprüfte Elektro-Scooter namhafter Marken.",
    "e-bike": "Geprüfte E-Bikes — Marken und Modelle folgen in Kürze.",
    "e-roller": "Geprüfte E-Roller — Marken und Modelle folgen in Kürze.",
    "e-motorraeder": "Geprüfte Elektromotorräder — Marken und Modelle folgen in Kürze."
  };

  var root = document.getElementById("catalog-root");
  var crumbsEl = document.getElementById("catalog-crumbs");
  var eyebrowEl = document.getElementById("catalog-eyebrow");
  var titleEl = document.getElementById("catalog-title");
  var subEl = document.getElementById("catalog-sub");
  if (!root) return;

  function esc(str) {
    return String(str).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
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

  function setHead(eyebrow, title, sub) {
    if (eyebrowEl) eyebrowEl.textContent = eyebrow;
    if (titleEl) titleEl.textContent = title;
    if (subEl) subEl.textContent = sub;
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
    setCrumbs([{ label: "Gebraucht & Geprüft", href: "#/" }]);
    setHead("Verkauf", "Gebraucht & Geprüft", "Sorgfältig geprüfte Gebrauchtfahrzeuge aus unserer Werkstatt in Freienbach — nach Kategorie wählen.");
    var html = '<div class="value-grid reveal-stagger is-visible">';
    CATEGORY_ORDER.forEach(function (slug) {
      var cat = CATALOG[slug];
      html += '<a class="value-card catalog-card" href="#/' + slug + '">' +
        '<div class="product-media"><img src="' + CATEGORY_IMAGES[slug] + '" alt="' + esc(cat.name) + '" width="1200" height="800" loading="lazy"></div>' +
        "<h3>" + esc(cat.name) + "</h3>" +
        "<p>" + esc(CATEGORY_DESC[slug]) + "</p>" +
        "</a>";
    });
    html += "</div>";
    root.innerHTML = html;
  }

  function renderBrands(catSlug) {
    var cat = findCategory(catSlug);
    if (!cat) { renderCategories(); return; }
    setCrumbs([
      { label: "Gebraucht & Geprüft", href: "#/" },
      { label: cat.name, href: "#/" + catSlug }
    ]);
    setHead("Gebraucht & Geprüft", cat.name, "Marke wählen.");

    if (!cat.brands.length) {
      root.innerHTML = '<div class="catalog-empty"><p>Diese Kategorie wird in Kürze mit Marken und Modellen befüllt. Bitte kontaktieren Sie uns direkt für aktuelle ' + esc(cat.name) + '-Angebote.</p>' +
        '<a href="../index.html#contact" class="btn btn-ghost btn-sm">Kontakt aufnehmen</a></div>';
      return;
    }

    var html = '<div class="brand-grid is-visible">';
    cat.brands.forEach(function (b) {
      var bSlug = slugify(b.name);
      var count = b.models.length;
      html += '<a class="brand-card" href="#/' + catSlug + "/" + bSlug + '">' +
        "<h3>" + esc(b.name) + "</h3>" +
        '<span class="brand-card-count">' + count + (count === 1 ? " Modell" : " Modelle") + "</span>" +
        "</a>";
    });
    html += '</div><p class="catalog-note">+ Weitere Marken folgen in Kürze.</p>';
    root.innerHTML = html;
  }

  function renderModels(catSlug, brandSlug) {
    var cat = findCategory(catSlug);
    if (!cat) { renderCategories(); return; }
    var b = findBrand(cat, brandSlug);
    if (!b) { renderBrands(catSlug); return; }
    setCrumbs([
      { label: "Gebraucht & Geprüft", href: "#/" },
      { label: cat.name, href: "#/" + catSlug },
      { label: b.name, href: "#/" + catSlug + "/" + brandSlug }
    ]);
    setHead(cat.name, b.name, "Modell wählen.");

    var html = '<div class="model-grid is-visible">';
    b.models.forEach(function (mo) {
      var mSlug = slugify(mo.name);
      var condLabel = mo.condition ? CONDITIONS[mo.condition] : "";
      html += '<a class="model-card" href="#/' + catSlug + "/" + brandSlug + "/" + mSlug + '">' +
        (mo.image ? '<div class="product-media"><img src="' + esc(mo.image) + '" alt="' + esc(mo.name) + '" width="960" height="640" loading="lazy"></div>' : "") +
        "<h3>" + esc(mo.name) + "</h3>" +
        (mo.desc ? '<p class="model-desc">' + esc(mo.desc) + "</p>" : "") +
        (condLabel ? '<span class="badge ok">' + esc(condLabel) + "</span>" : '<span class="badge">Zustand auf Anfrage</span>') +
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

    setCrumbs([
      { label: "Gebraucht & Geprüft", href: "#/" },
      { label: cat.name, href: "#/" + catSlug },
      { label: b.name, href: "#/" + catSlug + "/" + brandSlug },
      { label: mo.name, href: "#/" + catSlug + "/" + brandSlug + "/" + modelSlug }
    ]);
    setHead(cat.name + " · " + b.name, mo.name, "");

    var condLabel = mo.condition ? CONDITIONS[mo.condition] : "Auf Anfrage";
    var badges = '<span class="badge ok">Zustand: ' + esc(condLabel) + "</span>";
    if (mo.controlled) badges += '<span class="badge ok">✓ Kontrolliert</span>';
    if (mo.approved) badges += '<span class="badge ok">✓ Geprüft</span>';

    root.innerHTML =
      '<div class="tilt-card catalog-detail"><div class="tilt-card-inner">' +
      (mo.image ? '<div class="product-media"><img src="' + esc(mo.image) + '" alt="' + esc(mo.name) + '" width="960" height="640" loading="eager"></div>' : "") +
      '<span class="eyebrow">' + esc(cat.name) + "</span>" +
      "<h2>" + esc(b.name) + " — " + esc(mo.name) + "</h2>" +
      (mo.desc ? '<p class="model-desc">' + esc(mo.desc) + "</p>" : "") +
      '<span class="price">Preis auf Anfrage</span>' +
      '<div class="catalog-badges">' + badges + "</div>" +
      '<a href="../index.html#contact" class="btn btn-primary magnetic">Jetzt anfragen</a>' +
      "</div></div>";
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
})();
