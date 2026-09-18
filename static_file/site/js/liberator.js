/* Liberator — sayt skripti (kutubxonalarsiz): header, mobil menyu, qayta qo'ng'iroq oynasi,
   paydo bo'lish animatsiyasi, cookie xabari va analitika maqsadlari. */
(function () {
  "use strict";

  var doc = document.documentElement;
  var body = document.body;
  doc.classList.add("js");
  window.libReady = true;

  // "Orqaga" tugmasi bilan qaytilganda yuborish tugmasi faol bo'lsin.
  window.addEventListener("pageshow", function () {
    document.querySelectorAll("[data-lead-form] button[type=submit]").forEach(function (b) {
      b.disabled = false; b.removeAttribute("aria-busy");
    });
  });

  function storageGet(key) {
    try { return window.localStorage.getItem(key); } catch (e) { return null; }
  }
  function storageSet(key, value) {
    try { window.localStorage.setItem(key, value); } catch (e) { /* private rejim */ }
  }

  // --- Header soyasi -----------------------------------------------------------
  var header = document.querySelector(".header");
  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // --- Oynalar (mobil menyu va qayta qo'ng'iroq) --------------------------------
  var lastFocus = null;
  function open(el) {
    if (!el) return;
    lastFocus = document.activeElement;
    el.classList.add("is-open");
    el.setAttribute("aria-hidden", "false");
    body.classList.add("is-locked");
    var focusable = el.querySelector("input:not([type=hidden]):not([tabindex='-1']), a, button");
    if (focusable) setTimeout(function () { focusable.focus(); }, 50);
  }
  function close(el) {
    if (!el || !el.classList.contains("is-open")) return;
    el.classList.remove("is-open");
    el.setAttribute("aria-hidden", "true");
    body.classList.remove("is-locked");
    if (lastFocus) lastFocus.focus();
  }

  var drawer = document.getElementById("drawer");
  var modal = document.getElementById("callback-modal");

  document.addEventListener("click", function (e) {
    var t = e.target.closest ? e.target : null;
    if (!t) return;
    if (t.closest("[data-drawer-open]")) { e.preventDefault(); open(drawer); }
    else if (t.closest("[data-drawer-close]")) { e.preventDefault(); close(drawer); }
    else if (t.closest("[data-callback-open]")) { e.preventDefault(); close(drawer); open(modal); }
    else if (t.closest("[data-callback-close]")) { e.preventDefault(); close(modal); }
    else if (drawer && t.closest("#drawer a[href]")) { close(drawer); }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { close(modal); close(drawer); }
  });

  // --- Paydo bo'lish animatsiyasi --------------------------------------------------
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("is-visible"); });
  }

  // --- Analitika maqsadlari (Yandex Metrika + GA4); ID bo'lmasa hech narsa qilmaydi ---
  function trackGoal(name) {
    var metrikaId = body.getAttribute("data-metrika-id");
    if (metrikaId && typeof window.ym === "function") window.ym(Number(metrikaId), "reachGoal", name);
    if (typeof window.gtag === "function") window.gtag("event", name);
  }
  document.addEventListener("click", function (e) {
    var link = e.target.closest ? e.target.closest("a[href]") : null;
    if (!link) return;
    var href = link.getAttribute("href");
    if (href.indexOf("tel:") === 0) trackGoal("phone_click");
    else if (href.indexOf("t.me") !== -1) trackGoal("telegram_click");
    else if (href.indexOf("wa.me") !== -1) trackGoal("whatsapp_click");
  });
  document.addEventListener("submit", function (e) {
    var form = e.target;
    if (!form.matches || !form.matches("[data-lead-form]")) return;
    trackGoal("lead_form_submit");
    var button = form.querySelector("button[type=submit]");
    if (button) { button.disabled = true; button.setAttribute("aria-busy", "true"); }
  });

  // --- Cookie xabari -------------------------------------------------------------------
  var banner = document.getElementById("cookie-banner");
  if (banner && storageGet("lib-cookie-ok") !== "1") {
    banner.classList.add("is-visible");
    banner.querySelector("button").addEventListener("click", function () {
      storageSet("lib-cookie-ok", "1");
      banner.classList.remove("is-visible");
    });
  }
})();
