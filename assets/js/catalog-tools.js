(function () {
  "use strict";

  var WISHLIST_KEY = "esuero_wishlist";
  var COMPARE_KEY = "esuero_compare";
  var COMPARE_MAX = 3;

  function readStore(key) {
    try { return JSON.parse(localStorage.getItem(key)) || {}; } catch (e) { return {}; }
  }
  function writeStore(key, obj) {
    try { localStorage.setItem(key, JSON.stringify(obj)); } catch (e) {}
  }

  function slugify(str) {
    return str.toLowerCase()
      .replace(/[äáà]/g, "a").replace(/[öóò]/g, "o").replace(/[üúù]/g, "u").replace(/ß/g, "ss")
      .replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
  }

  function parsePrice(text) {
    if (!text) return null;
    var digits = text.replace(/[^0-9]/g, "");
    return digits ? parseInt(digits, 10) : null;
  }

  function cardData(card) {
    var h3 = card.querySelector("h3");
    var priceEl = card.querySelector(".price");
    var img = card.querySelector(".product-media img");
    var name = h3 ? h3.textContent.trim() : "";
    var specs = [];
    card.querySelectorAll(".spec-list dt").forEach(function (dt) {
      var dd = dt.nextElementSibling;
      if (dd) specs.push([dt.textContent.trim(), dd.textContent.trim()]);
    });
    var badges = Array.prototype.map.call(card.querySelectorAll(".badge"), function (b) { return b.textContent.trim(); });
    return {
      slug: card.getAttribute("data-buy-slug") || slugify(name),
      name: name,
      price: priceEl ? priceEl.textContent.trim() : "",
      priceValue: priceEl ? parsePrice(priceEl.textContent) : null,
      img: img ? img.getAttribute("src") : "",
      badges: badges,
      specs: specs,
      url: window.location.pathname,
    };
  }

  function speedOf(card) {
    for (var i = 0; i < card._data.badges.length; i++) {
      var m = card._data.badges[i].match(/(\d+)\s*km\/h/);
      if (m) return parseInt(m[1], 10);
    }
    return null;
  }
  function licenseOf(card) {
    var badges = card._data.badges;
    if (badges.indexOf("Kat. A1") !== -1) return "a1";
    if (badges.some(function (b) { return /nicht erforderlich/i.test(b); })) return "frei";
    return "";
  }

  /* ---------------- Wishlist ---------------- */

  function isWishlisted(slug) { return !!readStore(WISHLIST_KEY)[slug]; }
  function toggleWishlist(data, btn) {
    var store = readStore(WISHLIST_KEY);
    if (store[data.slug]) { delete store[data.slug]; }
    else { store[data.slug] = data; }
    writeStore(WISHLIST_KEY, store);
    updateWishlistUI();
    if (btn) btn.classList.toggle("is-active", !!store[data.slug]);
  }
  function wishlistCount() { return Object.keys(readStore(WISHLIST_KEY)).length; }

  function updateWishlistUI() {
    var count = wishlistCount();
    document.querySelectorAll(".wishlist-count").forEach(function (el) {
      el.textContent = count;
      el.style.display = count > 0 ? "inline-flex" : "none";
    });
  }

  function injectWishlistHeaderButton() {
    var actions = document.querySelector(".header-actions");
    if (!actions || actions.querySelector(".wishlist-btn")) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "wishlist-btn";
    btn.setAttribute("aria-label", "Wunschliste öffnen");
    btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none"><path d="M12 20s-7-4.35-9.5-8.5C.8 8.1 2.4 4.5 6 4.5c2 0 3.3 1 4 2.2.7-1.2 2-2.2 4-2.2 3.6 0 5.2 3.6 3.5 7C19 15.65 12 20 12 20Z" stroke="currentColor" stroke-width="1.6"/></svg><span class="wishlist-count">0</span>';
    var cta = actions.querySelector(".btn");
    actions.insertBefore(btn, cta || actions.firstChild.nextSibling);
    btn.addEventListener("click", openWishlistPanel);
  }

  function openWishlistPanel() {
    var store = readStore(WISHLIST_KEY);
    var items = Object.keys(store).map(function (k) { return store[k]; });
    var overlay = document.createElement("div");
    overlay.className = "checkout-overlay";
    var rows = items.length
      ? items.map(function (it) {
          return '<div class="wishlist-row" data-slug="' + it.slug + '">' +
            (it.img ? '<img src="' + it.img + '" alt="" loading="lazy">' : '<div class="wishlist-row-noimg"></div>') +
            '<div class="wishlist-row-info"><strong>' + it.name + '</strong><span>' + it.price + '</span></div>' +
            '<button type="button" class="wishlist-remove" aria-label="Entfernen">&times;</button>' +
            "</div>";
        }).join("")
      : '<p class="checkout-status">Ihre Wunschliste ist leer. Tippen Sie auf das Herz-Symbol bei einem Fahrzeug, um es zu speichern.</p>';
    overlay.innerHTML =
      '<div class="checkout-modal">' +
        '<button type="button" class="checkout-close" aria-label="Schliessen">&times;</button>' +
        '<div class="checkout-modal-head"><span class="eyebrow">E-Suero</span><h3 class="checkout-product-name">Wunschliste</h3></div>' +
        '<div class="wishlist-list">' + rows + "</div>" +
      "</div>";
    document.body.appendChild(overlay);
    document.body.classList.add("checkout-open");
    function close() { overlay.remove(); document.body.classList.remove("checkout-open"); }
    overlay.querySelector(".checkout-close").addEventListener("click", close);
    overlay.addEventListener("click", function (ev) { if (ev.target === overlay) close(); });
    overlay.querySelectorAll(".wishlist-remove").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var slug = btn.closest(".wishlist-row").getAttribute("data-slug");
        var s = readStore(WISHLIST_KEY);
        delete s[slug];
        writeStore(WISHLIST_KEY, s);
        updateWishlistUI();
        btn.closest(".wishlist-row").remove();
        document.querySelectorAll('.wishlist-heart[data-slug="' + slug + '"]').forEach(function (h) { h.classList.remove("is-active"); });
      });
    });
  }

  /* ---------------- Compare ---------------- */

  function isCompared(slug) { return !!readStore(COMPARE_KEY)[slug]; }
  function toggleCompare(data, btn) {
    var store = readStore(COMPARE_KEY);
    if (store[data.slug]) {
      delete store[data.slug];
    } else {
      if (Object.keys(store).length >= COMPARE_MAX) {
        alert("Sie können bis zu " + COMPARE_MAX + " Fahrzeuge gleichzeitig vergleichen.");
        return;
      }
      store[data.slug] = data;
    }
    writeStore(COMPARE_KEY, store);
    if (btn) btn.classList.toggle("is-active", !!store[data.slug]);
    updateCompareBar();
  }

  function updateCompareBar() {
    var store = readStore(COMPARE_KEY);
    var items = Object.keys(store).map(function (k) { return store[k]; });
    var bar = document.querySelector(".compare-bar");
    if (!items.length) { if (bar) bar.remove(); return; }
    if (!bar) {
      bar = document.createElement("div");
      bar.className = "compare-bar";
      document.body.appendChild(bar);
    }
    bar.innerHTML =
      '<span>' + items.length + (items.length === 1 ? " Fahrzeug" : " Fahrzeuge") + ' zum Vergleich ausgewählt</span>' +
      '<button type="button" class="btn btn-primary btn-sm magnetic" data-compare-open>Vergleichen</button>' +
      '<button type="button" class="compare-clear" aria-label="Vergleich leeren">&times;</button>';
    bar.querySelector("[data-compare-open]").addEventListener("click", openCompareModal);
    bar.querySelector(".compare-clear").addEventListener("click", function () {
      writeStore(COMPARE_KEY, {});
      document.querySelectorAll(".compare-toggle.is-active").forEach(function (b) { b.classList.remove("is-active"); });
      bar.remove();
    });
  }

  function openCompareModal() {
    var store = readStore(COMPARE_KEY);
    var items = Object.keys(store).map(function (k) { return store[k]; });
    if (!items.length) return;
    var labels = [];
    items.forEach(function (it) {
      it.specs.forEach(function (pair) { if (labels.indexOf(pair[0]) === -1) labels.push(pair[0]); });
    });
    var head = '<tr><th>Modell</th>' + items.map(function (it) { return "<th>" + it.name + "</th>"; }).join("") + "</tr>";
    var priceRow = '<tr><td>Preis</td>' + items.map(function (it) { return "<td>" + it.price + "</td>"; }).join("") + "</tr>";
    var rows = labels.map(function (label) {
      return "<tr><td>" + label + "</td>" + items.map(function (it) {
        var pair = it.specs.filter(function (p) { return p[0] === label; })[0];
        return "<td>" + (pair ? pair[1] : "—") + "</td>";
      }).join("") + "</tr>";
    }).join("");

    var overlay = document.createElement("div");
    overlay.className = "checkout-overlay";
    overlay.innerHTML =
      '<div class="checkout-modal compare-modal">' +
        '<button type="button" class="checkout-close" aria-label="Schliessen">&times;</button>' +
        '<div class="checkout-modal-head"><span class="eyebrow">E-Suero</span><h3 class="checkout-product-name">Fahrzeugvergleich</h3></div>' +
        '<div class="compare-table-wrap"><table class="compare-table"><thead>' + head + "</thead><tbody>" + priceRow + rows + "</tbody></table></div>" +
      "</div>";
    document.body.appendChild(overlay);
    document.body.classList.add("checkout-open");
    function close() { overlay.remove(); document.body.classList.remove("checkout-open"); }
    overlay.querySelector(".checkout-close").addEventListener("click", close);
    overlay.addEventListener("click", function (ev) { if (ev.target === overlay) close(); });
  }

  /* ---------------- Card tools injection ---------------- */

  function injectCardTools() {
    document.querySelectorAll(".tilt-card-inner").forEach(function (card) {
      if (card.querySelector(".card-tools")) return;
      var h3 = card.querySelector("h3");
      if (!h3) return;
      var data = cardData(card);
      card._data = data;

      var tools = document.createElement("div");
      tools.className = "card-tools";

      var heart = document.createElement("button");
      heart.type = "button";
      heart.className = "wishlist-heart" + (isWishlisted(data.slug) ? " is-active" : "");
      heart.setAttribute("data-slug", data.slug);
      heart.setAttribute("aria-label", "Zur Wunschliste hinzufügen");
      heart.innerHTML = '<svg viewBox="0 0 24 24" fill="none"><path d="M12 20s-7-4.35-9.5-8.5C.8 8.1 2.4 4.5 6 4.5c2 0 3.3 1 4 2.2.7-1.2 2-2.2 4-2.2 3.6 0 5.2 3.6 3.5 7C19 15.65 12 20 12 20Z" stroke="currentColor" stroke-width="1.6"/></svg>';
      heart.addEventListener("click", function () { toggleWishlist(card._data, heart); });

      var compareBtn = document.createElement("button");
      compareBtn.type = "button";
      compareBtn.className = "compare-toggle" + (isCompared(data.slug) ? " is-active" : "");
      compareBtn.setAttribute("aria-label", "Zum Vergleich hinzufügen");
      compareBtn.textContent = "Vergleichen";
      compareBtn.addEventListener("click", function () { toggleCompare(card._data, compareBtn); });

      tools.appendChild(heart);
      tools.appendChild(compareBtn);
      card.insertBefore(tools, card.firstChild);
    });
    updateWishlistUI();
    updateCompareBar();
  }

  /* ---------------- Search + filters ---------------- */

  function buildToolbar(container) {
    var toolbar = document.createElement("div");
    toolbar.className = "catalog-toolbar reveal";
    toolbar.innerHTML =
      '<input type="search" class="catalog-search" placeholder="Suche nach Marke, Modell, Reichweite …" aria-label="Fahrzeuge durchsuchen">' +
      '<select class="catalog-filter" data-filter="speed" aria-label="Höchstgeschwindigkeit filtern">' +
        '<option value="">Alle Geschwindigkeiten</option>' +
        '<option value="25">bis 25 km/h</option>' +
        '<option value="45">bis 45 km/h</option>' +
        '<option value="46">über 45 km/h</option>' +
      "</select>" +
      '<select class="catalog-filter" data-filter="license" aria-label="Führerschein filtern">' +
        '<option value="">Führerschein: Alle</option>' +
        '<option value="frei">Nicht erforderlich</option>' +
        '<option value="a1">Kat. A1</option>' +
      "</select>" +
      '<p class="catalog-empty" hidden>Keine Fahrzeuge gefunden. Bitte Suche oder Filter anpassen.</p>';
    container.parentNode.insertBefore(toolbar, container);
    return toolbar;
  }

  function wireToolbar(toolbar, container) {
    var search = toolbar.querySelector(".catalog-search");
    var speedSel = toolbar.querySelector('[data-filter="speed"]');
    var licenseSel = toolbar.querySelector('[data-filter="license"]');
    var emptyMsg = toolbar.querySelector(".catalog-empty");

    function applyFilters() {
      var q = search.value.trim().toLowerCase();
      var speedMax = speedSel.value ? parseInt(speedSel.value, 10) : null;
      var license = licenseSel.value;
      var visibleCount = 0;

      container.querySelectorAll(".tilt-card").forEach(function (card) {
        var inner = card.querySelector(".tilt-card-inner");
        if (!inner || !inner._data) { card.style.display = ""; visibleCount++; return; }
        var data = inner._data;
        var matchesText = !q || (inner.textContent || "").toLowerCase().indexOf(q) !== -1;
        var speed = speedOf(inner);
        var matchesSpeed = !speedMax || (speed !== null && (speedMax === 46 ? speed > 45 : speed <= speedMax));
        var matchesLicense = !license || licenseOf(inner) === license;
        var visible = matchesText && matchesSpeed && matchesLicense;
        card.style.display = visible ? "" : "none";
        if (visible) visibleCount++;
      });

      emptyMsg.hidden = visibleCount !== 0;
    }

    search.addEventListener("input", applyFilters);
    speedSel.addEventListener("change", applyFilters);
    licenseSel.addEventListener("change", applyFilters);
  }

  function injectToolbars() {
    document.querySelectorAll(".carousel-track, .vehicle-grid").forEach(function (container) {
      if (!container.querySelector(".tilt-card")) return;
      if (container.previousElementSibling && container.previousElementSibling.classList && container.previousElementSibling.classList.contains("catalog-toolbar")) return;
      // carousel-track sits inside nested wrapper divs — anchor the toolbar to the outermost carousel/grid block
      var anchor = container.closest(".carousel") || container;
      if (anchor.parentNode.querySelector(":scope > .catalog-toolbar")) return;
      var toolbar = buildToolbar(anchor);
      wireToolbar(toolbar, container);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    injectWishlistHeaderButton();
    injectCardTools();
    injectToolbars();
  });
})();
