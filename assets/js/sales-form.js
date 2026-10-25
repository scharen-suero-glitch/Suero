(function () {
  "use strict";

  var ENDPOINT = "/verkauf/inquiry.php";

  function qs(el, sel) { return el.querySelector(sel); }

  function wireForm(form) {
    var statusEl = qs(form, ".form-status");
    var reasonSelect = qs(form, '[name="reason"]');
    var dateField = qs(form, '[data-field="preferred_date"]');

    var model = form.getAttribute("data-model") || "";
    var modelField = qs(form, '[data-field="model-display"]');
    if (modelField && model) {
      modelField.hidden = false;
      var modelInput = modelField.querySelector("input");
      if (modelInput) modelInput.value = model;
    }

    function syncDateVisibility() {
      if (!dateField || !reasonSelect) return;
      dateField.hidden = reasonSelect.value !== "probefahrt";
    }
    if (reasonSelect) {
      reasonSelect.addEventListener("change", syncDateVisibility);
      syncDateVisibility();
    }

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var name = (qs(form, '[name="name"]') || {}).value || "";
      var email = (qs(form, '[name="email"]') || {}).value || "";
      var phone = (qs(form, '[name="phone"]') || {}).value || "";
      var message = (qs(form, '[name="message"]') || {}).value || "";
      var preferredDate = (qs(form, '[name="preferred_date"]') || {}).value || "";
      var reason = reasonSelect ? reasonSelect.value : "beratung";
      var model = form.getAttribute("data-model") || "";

      name = name.trim();
      email = email.trim();
      phone = phone.trim();

      if (!name) {
        setStatus(statusEl, "err", "Bitte geben Sie Ihren Namen an.");
        return;
      }
      var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
      var phoneDigits = phone.replace(/[^0-9]/g, "");
      var phoneOk = phoneDigits.length >= 7 && phoneDigits.length <= 15;
      if (!emailOk && !phoneOk) {
        setStatus(statusEl, "err", "Bitte geben Sie eine gültige Telefonnummer oder E-Mail-Adresse an.");
        return;
      }

      var submitBtn = form.querySelector('[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;
      setStatus(statusEl, "", "Wird gesendet…");

      fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name,
          email: email,
          phone: phone,
          model: model,
          reason: reason,
          message: message.trim(),
          preferred_date: preferredDate,
          page_url: window.location.href,
          website: (qs(form, '[name="website"]') || {}).value || "", // honeypot
        }),
      })
        .then(function (res) {
          return res.json().then(function (data) { return { ok: res.ok, data: data }; });
        })
        .then(function (result) {
          if (submitBtn) submitBtn.disabled = false;
          if (!result.ok || !result.data.ok) {
            setStatus(statusEl, "err", (result.data && result.data.error) || "Anfrage konnte nicht gesendet werden. Bitte rufen Sie uns an oder schreiben Sie uns auf WhatsApp.");
            return;
          }
          if (result.data.note === "pending_confirmation") {
            setStatus(statusEl, "ok", "Danke! Ihre Probefahrt-Anfrage ist eingegangen — der Termin ist noch nicht bestätigt, wir melden uns zur Terminbestätigung bei Ihnen.");
          } else {
            setStatus(statusEl, "ok", "Danke, Ihre Anfrage ist bei uns eingegangen. Wir melden uns in der Regel innerhalb eines Werktags.");
          }
          form.reset();
          syncDateVisibility();
        })
        .catch(function () {
          if (submitBtn) submitBtn.disabled = false;
          setStatus(statusEl, "err", "Die Anfrage konnte nicht gesendet werden. Bitte rufen Sie uns direkt an oder schreiben Sie uns auf WhatsApp.");
        });
    });
  }

  function setStatus(el, kind, text) {
    if (!el) return;
    el.textContent = text;
    el.className = "form-status" + (kind ? " " + kind : "");
  }

  function wireWhatsapp() {
    document.querySelectorAll("[data-wa-model]").forEach(function (link) {
      var model = link.getAttribute("data-wa-model") || "";
      var msg = "Guten Tag, ich interessiere mich für den " + model + ". Ist dieses Fahrzeug verfügbar? Ich möchte gerne eine Beratung oder Probefahrt anfragen.";
      link.href = "https://wa.me/41796689088?text=" + encodeURIComponent(msg);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-sales-form]").forEach(wireForm);
    wireWhatsapp();
  });
})();
