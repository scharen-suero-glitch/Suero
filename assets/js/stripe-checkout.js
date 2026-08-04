(function () {
  "use strict";

  var ENDPOINT = "/stripe/create-checkout-session.php";

  function parsePriceToRappen(text) {
    if (!text) return 0;
    var digits = text.replace(/[^0-9]/g, "");
    return digits ? parseInt(digits, 10) * 100 : 0;
  }

  function buildOverlay() {
    var overlay = document.createElement("div");
    overlay.className = "checkout-overlay";
    overlay.innerHTML =
      '<div class="checkout-modal">' +
        '<button type="button" class="checkout-close" aria-label="Schliessen">&times;</button>' +
        '<div class="checkout-modal-head">' +
          '<span class="eyebrow">E-Suero</span>' +
          '<h3 class="checkout-product-name"></h3>' +
        "</div>" +
        '<div class="checkout-status">Sie werden zur sicheren Stripe-Zahlungsseite weitergeleitet…</div>' +
      "</div>";
    document.body.appendChild(overlay);
    return overlay;
  }

  function closeOverlay(overlay) {
    overlay.remove();
    document.body.classList.remove("checkout-open");
  }

  function openCheckout(product) {
    var overlay = buildOverlay();
    document.body.classList.add("checkout-open");
    overlay.querySelector(".checkout-product-name").textContent = product.name;
    var statusEl = overlay.querySelector(".checkout-status");

    overlay.querySelector(".checkout-close").addEventListener("click", function () {
      closeOverlay(overlay);
    });
    overlay.addEventListener("click", function (ev) {
      if (ev.target === overlay) closeOverlay(overlay);
    });

    fetch(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(product),
    })
      .then(function (res) {
        if (!res.ok) throw new Error("checkout session request failed");
        return res.json();
      })
      .then(function (data) {
        if (!data.url) throw new Error(data.error || "no checkout url");
        // Full-page redirect to Stripe's own hosted, PCI-compliant checkout page.
        window.location.href = data.url;
      })
      .catch(function () {
        statusEl.textContent = "Die Online-Zahlung ist momentan nicht verfügbar. Bitte kontaktieren Sie uns direkt unter info@e-suero.ch oder +41 79 668 90 88.";
        statusEl.classList.add("checkout-status-error");
      });
  }

  function buyButtons() {
    document.addEventListener("click", function (ev) {
      var btn = ev.target.closest("[data-buy-btn]");
      if (!btn) return;
      ev.preventDefault();
      var card = btn.closest("[data-buy-name]");
      if (!card) return;
      openCheckout({
        name: card.getAttribute("data-buy-name") || "",
        price: parseInt(card.getAttribute("data-buy-price"), 10) || parsePriceToRappen(card.querySelector(".price") && card.querySelector(".price").textContent),
        image: card.getAttribute("data-buy-img") || "",
        slug: card.getAttribute("data-buy-slug") || "",
      });
    });
  }

  document.addEventListener("DOMContentLoaded", buyButtons);
})();
