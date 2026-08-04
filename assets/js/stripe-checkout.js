(function () {
  "use strict";

  // Publishable key only — safe to expose client-side. The secret key lives
  // exclusively in stripe/create-checkout-session.php on the server.
  var STRIPE_PUBLISHABLE_KEY = "pk_live_51TxFHKRymeNj4j0TQebIXmdJNLLiCyzlyVVaRg9QOvKhYUnPBnVLgJYQq67MYaTBIuV1LnIFaAp0yx41cpCxCcfq00nORbl0yV";
  var ENDPOINT = "/stripe/create-checkout-session.php";

  var stripePromise = null;
  function loadStripe() {
    if (stripePromise) return stripePromise;
    stripePromise = new Promise(function (resolve, reject) {
      if (window.Stripe) return resolve(window.Stripe(STRIPE_PUBLISHABLE_KEY));
      var script = document.createElement("script");
      script.src = "https://js.stripe.com/v3/";
      script.onload = function () {
        window.Stripe ? resolve(window.Stripe(STRIPE_PUBLISHABLE_KEY)) : reject(new Error("Stripe.js failed to load"));
      };
      script.onerror = function () { reject(new Error("Stripe.js failed to load")); };
      document.head.appendChild(script);
    });
    return stripePromise;
  }

  function parsePriceToRappen(text) {
    if (!text) return 0;
    var digits = text.replace(/[^0-9]/g, "");
    return digits ? parseInt(digits, 10) * 100 : 0;
  }

  function buildModal() {
    var overlay = document.createElement("div");
    overlay.className = "checkout-overlay";
    overlay.innerHTML =
      '<div class="checkout-modal">' +
        '<button type="button" class="checkout-close" aria-label="Schliessen">&times;</button>' +
        '<div class="checkout-modal-head">' +
          '<span class="eyebrow">E-Suero</span>' +
          '<h3 class="checkout-product-name"></h3>' +
        "</div>" +
        '<div class="checkout-status">Zahlung wird vorbereitet…</div>' +
        '<div class="checkout-mount"></div>' +
      "</div>";
    document.body.appendChild(overlay);
    return overlay;
  }

  function closeModal(overlay, checkoutInstance) {
    if (checkoutInstance) {
      try { checkoutInstance.destroy(); } catch (e) {}
    }
    overlay.remove();
    document.body.classList.remove("checkout-open");
  }

  function openCheckout(product) {
    var overlay = buildModal();
    document.body.classList.add("checkout-open");
    overlay.querySelector(".checkout-product-name").textContent = product.name;
    var statusEl = overlay.querySelector(".checkout-status");
    var mountEl = overlay.querySelector(".checkout-mount");
    var checkoutInstance = null;

    overlay.querySelector(".checkout-close").addEventListener("click", function () {
      closeModal(overlay, checkoutInstance);
    });
    overlay.addEventListener("click", function (ev) {
      if (ev.target === overlay) closeModal(overlay, checkoutInstance);
    });

    Promise.all([
      loadStripe(),
      fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(product),
      }).then(function (res) {
        if (!res.ok) throw new Error("checkout session request failed");
        return res.json();
      }),
    ])
      .then(function (results) {
        var stripe = results[0];
        var data = results[1];
        if (!data.clientSecret) throw new Error(data.error || "no client secret");
        statusEl.remove();
        checkoutInstance = stripe.initEmbeddedCheckout({ clientSecret: data.clientSecret });
        return checkoutInstance.mount(mountEl);
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
