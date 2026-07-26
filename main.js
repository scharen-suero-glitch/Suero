/* E-SUERO — main.js — vanilla JS, no build step, no frameworks */
(function () {
  "use strict";

  function safe(fn, name) {
    try { fn(); } catch (err) {
      console.error("[e-suero] init failed:", name, err);
    }
  }

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- i18n ---------------- */
  function initI18n() {
    var DICT = window.__ESUERO_I18N__ || {};
    var LANGS = ["de", "en", "it", "es"];
    var stored = null;
    try { stored = localStorage.getItem("esuero_lang"); } catch (e) {}
    var lang = LANGS.indexOf(stored) > -1 ? stored : "de";

    function apply(l) {
      var dict = DICT[l] || DICT.de;
      if (!dict) return;
      document.documentElement.setAttribute("lang", l);

      document.querySelectorAll("[data-i18n]").forEach(function (el) {
        var key = el.getAttribute("data-i18n");
        if (dict[key] !== undefined) el.textContent = dict[key];
      });
      document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
        var key = el.getAttribute("data-i18n-html");
        if (dict[key] !== undefined) el.innerHTML = dict[key];
      });
      document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
        var key = el.getAttribute("data-i18n-placeholder");
        if (dict[key] !== undefined) el.setAttribute("placeholder", dict[key]);
      });
      document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
        var key = el.getAttribute("data-i18n-aria");
        if (dict[key] !== undefined) el.setAttribute("aria-label", dict[key]);
      });
      if (dict.meta_title) document.title = dict.meta_title;
      var metaDesc = document.querySelector('meta[name="description"]');
      if (metaDesc && dict.meta_desc) metaDesc.setAttribute("content", dict.meta_desc);

      document.querySelectorAll(".lang-menu button").forEach(function (btn) {
        btn.classList.toggle("is-active", btn.getAttribute("data-lang") === l);
      });
      var current = document.querySelector(".lang-current span");
      if (current) current.textContent = l.toUpperCase();
    }

    apply(lang);

    document.querySelectorAll(".lang-menu button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var l = btn.getAttribute("data-lang");
        lang = l;
        try { localStorage.setItem("esuero_lang", l); } catch (e) {}
        apply(l);
        document.querySelectorAll(".lang-switch").forEach(function (s) { s.classList.remove("is-open"); });
      });
    });
  }

  /* ---------------- Splash ---------------- */
  function initSplash() {
    var splash = document.querySelector(".splash");
    if (!splash) return;
    setTimeout(function () {
      splash.style.display = "none";
    }, 1900);
  }

  /* ---------------- Custom cursor ---------------- */
  function initCursor() {
    if (window.matchMedia("(hover: none), (pointer: coarse)").matches) return;
    var dot = document.querySelector(".cursor-dot");
    var ring = document.querySelector(".cursor-ring");
    if (!dot || !ring) return;
    var rx = 0, ry = 0, dx = 0, dy = 0;

    window.addEventListener("mousemove", function (e) {
      dx = e.clientX; dy = e.clientY;
      dot.style.left = dx + "px"; dot.style.top = dy + "px";
    });

    function loop() {
      rx += (dx - rx) * 0.18;
      ry += (dy - ry) * 0.18;
      ring.style.left = rx + "px"; ring.style.top = ry + "px";
      requestAnimationFrame(loop);
    }
    loop();

    document.querySelectorAll("a, button, .tilt-card, input, textarea, select").forEach(function (el) {
      el.addEventListener("mouseenter", function () { ring.classList.add("is-active"); });
      el.addEventListener("mouseleave", function () { ring.classList.remove("is-active"); });
    });
  }

  /* ---------------- Magnetic buttons ---------------- */
  function initMagnetic() {
    if (reduceMotion) return;
    document.querySelectorAll(".magnetic").forEach(function (el) {
      var strength = 0.35;
      el.addEventListener("mousemove", function (e) {
        var r = el.getBoundingClientRect();
        var mx = e.clientX - (r.left + r.width / 2);
        var my = e.clientY - (r.top + r.height / 2);
        el.style.transform = "translate(" + mx * strength + "px," + my * strength + "px)";
      });
      el.addEventListener("mouseleave", function () {
        el.style.transform = "translate(0,0)";
      });
    });
  }

  /* ---------------- Header ---------------- */
  function initHeader() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    function onScroll() {
      header.classList.toggle("is-scrolled", window.scrollY > 40);
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---------------- Mobile nav ---------------- */
  function initMobileNav() {
    var burger = document.querySelector(".burger");
    var nav = document.querySelector(".mobile-nav");
    if (!burger || !nav) return;
    function toggle(open) {
      burger.classList.toggle("is-open", open);
      nav.classList.toggle("is-open", open);
      document.body.classList.toggle("no-scroll", open);
    }
    burger.addEventListener("click", function () {
      toggle(!nav.classList.contains("is-open"));
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { toggle(false); });
    });
  }

  /* ---------------- Language dropdown toggle ---------------- */
  function initLangDropdown() {
    var switches = document.querySelectorAll(".lang-switch");
    switches.forEach(function (sw) {
      var trigger = sw.querySelector(".lang-current");
      if (!trigger) return;
      trigger.addEventListener("click", function (e) {
        e.stopPropagation();
        var wasOpen = sw.classList.contains("is-open");
        switches.forEach(function (s) { s.classList.remove("is-open"); });
        sw.classList.toggle("is-open", !wasOpen);
      });
    });
    document.addEventListener("click", function () {
      switches.forEach(function (s) { s.classList.remove("is-open"); });
    });
  }

  /* ---------------- Scroll reveal ---------------- */
  function initReveal() {
    var targets = document.querySelectorAll(".reveal, .reveal-stagger");
    if (!targets.length) return;

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.05, rootMargin: "0px 0px -5% 0px" }
    );
    targets.forEach(function (t) { io.observe(t); });

    setTimeout(function () {
      targets.forEach(function (t) { t.classList.add("is-visible"); });
    }, 6000);
  }

  /* ---------------- Hero parallax + particle canvas ---------------- */
  function initHeroFX() {
    var hero = document.querySelector(".hero");
    var art = document.querySelector(".hero-art");
    if (hero && art && !reduceMotion) {
      hero.addEventListener("mousemove", function (e) {
        var r = hero.getBoundingClientRect();
        var mx = (e.clientX - r.left) / r.width - 0.5;
        var my = (e.clientY - r.top) / r.height - 0.5;
        art.style.transform = "translate(" + mx * -18 + "px," + my * -18 + "px)";
      });
    }

    var canvas = document.getElementById("hero-canvas");
    if (!canvas || reduceMotion) return;
    var ctx = canvas.getContext("2d");
    var particles = [];
    var count = window.innerWidth < 760 ? 26 : 55;

    function resize() {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    }
    resize();
    window.addEventListener("resize", resize);

    for (var i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 1.6 + 0.4,
        vy: Math.random() * 0.35 + 0.08,
        vx: (Math.random() - 0.5) * 0.15,
        a: Math.random() * 0.5 + 0.2,
        c: Math.random() > 0.5 ? "0,255,102" : "0,191,255"
      });
    }

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      particles.forEach(function (p) {
        p.y -= p.vy;
        p.x += p.vx;
        if (p.y < -10) { p.y = canvas.height + 10; p.x = Math.random() * canvas.width; }
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(" + p.c + "," + p.a + ")";
        ctx.fill();
      });
      requestAnimationFrame(draw);
    }
    draw();
  }

  /* ---------------- 3D tilt cards ---------------- */
  function initTilt() {
    if (reduceMotion || window.matchMedia("(hover: none)").matches) return;
    document.querySelectorAll(".tilt-card").forEach(function (card) {
      var inner = card.querySelector(".tilt-card-inner");
      if (!inner) return;
      card.addEventListener("mousemove", function (e) {
        var r = card.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width;
        var py = (e.clientY - r.top) / r.height;
        var rx = (py - 0.5) * -10;
        var ry = (px - 0.5) * 10;
        inner.style.transform = "rotateX(" + rx + "deg) rotateY(" + ry + "deg) translateZ(6px)";
      });
      card.addEventListener("mouseleave", function () {
        inner.style.transform = "rotateX(0) rotateY(0)";
      });
    });
  }

  /* ---------------- Product tabs ---------------- */
  function initProductTabs() {
    var tabs = document.querySelectorAll(".product-tab");
    var panels = document.querySelectorAll(".product-panel");
    if (!tabs.length) return;
    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        var target = tab.getAttribute("data-tab");
        tabs.forEach(function (t) { t.classList.remove("is-active"); });
        tab.classList.add("is-active");
        panels.forEach(function (p) {
          p.classList.toggle("is-active", p.getAttribute("data-panel") === target);
        });
      });
    });
  }

  /* ---------------- Animated counters (lab stats) ---------------- */
  function initCounters() {
    var els = document.querySelectorAll("[data-count-to]");
    if (!els.length) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var raw = el.getAttribute("data-count-to");
        var end = parseFloat(raw.replace(/[^0-9.]/g, ""));
        if (isNaN(end)) { io.unobserve(el); return; }
        var suffix = raw.replace(/^[0-9.]+/, "");
        var start = 0;
        var dur = 1400;
        var t0 = performance.now();
        function tick(t) {
          var p = Math.min((t - t0) / dur, 1);
          var val = start + (end - start) * (1 - Math.pow(1 - p, 3));
          el.textContent = (Number.isInteger(end) ? Math.round(val) : val.toFixed(2)) + suffix;
          if (p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
        io.unobserve(el);
      });
    }, { threshold: 0.4 });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---------------- FAQ accordion ---------------- */
  function initFAQ() {
    document.querySelectorAll(".faq-item").forEach(function (item) {
      var q = item.querySelector(".faq-q");
      var a = item.querySelector(".faq-a");
      if (!q || !a) return;
      q.addEventListener("click", function () {
        var isOpen = item.classList.contains("is-open");
        document.querySelectorAll(".faq-item").forEach(function (i) {
          i.classList.remove("is-open");
          i.querySelector(".faq-a").style.maxHeight = null;
        });
        if (!isOpen) {
          item.classList.add("is-open");
          a.style.maxHeight = a.scrollHeight + "px";
        }
      });
    });
  }

  /* ---------------- Before / After slider ---------------- */
  function initBeforeAfter() {
    var wrap = document.querySelector(".ba-wrap");
    var after = document.querySelector(".ba-after");
    var handle = document.querySelector(".ba-handle");
    var range = document.querySelector(".ba-slider");
    if (!wrap || !after || !range) return;

    function set(val) {
      after.style.clipPath = "inset(0 0 0 " + val + "%)";
      if (handle) handle.style.left = val + "%";
    }
    range.addEventListener("input", function () { set(range.value); });
    set(range.value);
  }

  /* ---------------- Back to top ---------------- */
  function initBackToTop() {
    var btn = document.querySelector(".back-to-top");
    if (!btn) return;
    window.addEventListener("scroll", function () {
      btn.classList.toggle("is-visible", window.scrollY > 600);
    }, { passive: true });
    btn.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---------------- Contact form ---------------- */
  function initForm() {
    var form = document.getElementById("contact-form");
    var status = document.querySelector(".form-status");
    if (!form) return;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = form.querySelector('[name="name"]').value.trim();
      var email = form.querySelector('[name="email"]').value.trim();
      var message = form.querySelector('[name="message"]').value.trim();
      var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

      if (!name || !emailOk || !message) {
        if (status) {
          status.textContent = "Bitte alle Pflichtfelder korrekt ausfüllen.";
          status.className = "form-status err";
        }
        return;
      }

      var subject = encodeURIComponent("Anfrage von " + name + " — E-Suero Website");
      var body = encodeURIComponent(
        "Name: " + name + "\n" +
        "E-Mail: " + email + "\n" +
        "Telefon: " + (form.querySelector('[name="phone"]').value || "-") + "\n" +
        "Service: " + (form.querySelector('[name="service"]').value || "-") + "\n\n" +
        message
      );
      window.location.href = "mailto:info@e-suero.ch?subject=" + subject + "&body=" + body;

      if (status) {
        status.textContent = "Ihr E-Mail-Programm öffnet sich mit der vorbereiteten Anfrage.";
        status.className = "form-status ok";
      }
      form.reset();
    });
  }

  /* ---------------- Footer year ---------------- */
  function initYear() {
    var el = document.getElementById("year");
    if (el) el.textContent = new Date().getFullYear();
  }

  document.addEventListener("DOMContentLoaded", function () {
    safe(initI18n, "i18n");
    safe(initSplash, "splash");
    safe(initCursor, "cursor");
    safe(initMagnetic, "magnetic");
    safe(initHeader, "header");
    safe(initMobileNav, "mobileNav");
    safe(initLangDropdown, "langDropdown");
    safe(initReveal, "reveal");
    safe(initHeroFX, "heroFX");
    safe(initTilt, "tilt");
    safe(initProductTabs, "productTabs");
    safe(initCounters, "counters");
    safe(initFAQ, "faq");
    safe(initBeforeAfter, "beforeAfter");
    safe(initBackToTop, "backToTop");
    safe(initForm, "form");
    safe(initYear, "year");
  });
})();
