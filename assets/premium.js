/* ============================================================
   JALEP 3.0 — Premium Design Layer (runtime)
   Vanilla JS, defer-safe, sem dependências.
   - Reveal-on-scroll via IntersectionObserver (threshold .12)
   - Auto-marca filhos de main com .reveal (seletor seguro;
     só adiciona se o elemento não tiver outro sistema de
     reveal próprio — .scroll-reveal* do site é respeitado)
   - Skeleton shimmer: marca imgs carregadas com .premium-loaded
   - Toast aria-live=polite em falhas de rede de formulários
     (não intercepta nem altera o comportamento dos forms)
   - prefers-reduced-motion: pula TUDO de animação de entrada
   - Reveals com stagger 40ms por lote (--reveal-index, premium.css)
   - data-perf="low": pula auto-reveal (preferência do usuário)
   ============================================================ */
(function () {
  "use strict";

  var doc = document;
  /* prefers-reduced-motion: checado 1x e cacheado (motion tokens 3.0) */
  var reducedMotion = false;
  try {
    reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch (e) { /* matchMedia indisponível: assume motion ok */ }

  var perfLow = false;
  try {
    perfLow = doc.documentElement.getAttribute("data-perf") === "low";
  } catch (e) { /* noop */ }

  /* ---------- Skeleton para imagens ---------- */
  function markLoadedImages(scope) {
    var imgs = scope.querySelectorAll("main img");
    for (var i = 0; i < imgs.length; i++) {
      (function (img) {
        var done = function () {
          img.classList.add("premium-loaded");
        };
        if (img.complete && img.naturalWidth > 0) {
          done();
        } else {
          img.addEventListener("load", done, { once: true });
          img.addEventListener("error", done, { once: true });
        }
      })(imgs[i]);
    }
  }

  /* ---------- Auto-reveal: marca filhos de main ---------- */
  /* Classes de reveal próprias do site — não duplicar animação.
     Elementos DENTRO de um .scroll-reveal ancestral também são
     pulados: o ancestral já revela o bloco inteiro. */
  function hasOwnRevealSystem(el) {
    if (!el.className || typeof el.className !== "string") return false;
    if (/(^|\s)scroll-reveal(-left|-scale|-blur)?(\s|$)/.test(el.className)) return true;
    if (el.closest && el.closest(".scroll-reveal, .reveal, [data-reveal]")) return true;
    return false;
  }

  function autoMarkReveal() {
    var nodes = doc.querySelectorAll(
      "main h2, main h3, main p, main .card, main img, main .glass-card, main .neon-card, main .stat-card"
    );
    var marked = [];
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.classList.contains("reveal")) continue;
      if (el.classList.contains("in")) continue;
      if (hasOwnRevealSystem(el)) continue;
      if (el.tagName === "IMG") {
        var parent = el.closest ? el.closest(".reveal") : null;
        if (parent) continue; /* o card ancestral já revela */
        var w = el.getAttribute("width");
        var h = el.getAttribute("height");
        if (w === "1" || h === "1") continue; /* pixel de tracking */
        var src = (el.getAttribute("src") || "");
        if (src.indexOf("data:") === 0 && src.length < 200) continue; /* ícone inline */
      }
      el.classList.add("reveal");
      marked.push(el);
    }
    return marked;
  }

  /* ---------- Observer (3.0: stagger 40ms por lote) ---------- */
  /* Entradas do mesmo callback = mesmo lote visual (grid/lista que
     entra junto). O primeiro item revela já, o k-ésimo espera
     k × 40ms via --reveal-index (consumido pelo premium.css).
     Lotes posteriores recomeçam em zero. */
  function revealAllInstantly() {
    var all = doc.querySelectorAll(".reveal");
    for (var i = 0; i < all.length; i++) {
      all[i].classList.add("in");
    }
  }

  function observeReveals() {
    if (reducedMotion || !("IntersectionObserver" in window)) {
      revealAllInstantly();
      return;
    }

    var io = new IntersectionObserver(
      function (entries) {
        var batchIndex = 0;
        for (var k = 0; k < entries.length; k++) {
          var entry = entries[k];
          if (entry.isIntersecting) {
            if (batchIndex > 0) {
              entry.target.style.setProperty("--reveal-index", String(batchIndex));
            }
            entry.target.classList.add("in");
            io.unobserve(entry.target);
            batchIndex++;
          }
        }
      },
      { threshold: 0.12, rootMargin: "0px 0px -4% 0px" }
    );

    var targets = doc.querySelectorAll(".reveal:not(.in)");
    for (var t = 0; t < targets.length; t++) {
      io.observe(targets[t]);
    }
    return io;
  }

  /* ---------- Toast (aria-live=polite) ---------- */
  var toastLiveRegion = null;

  function ensureToastRegion() {
    if (toastLiveRegion && toastLiveRegion.parentNode) return toastLiveRegion;
    toastLiveRegion = doc.getElementById("premium-toast-region");
    if (!toastLiveRegion) {
      toastLiveRegion = doc.createElement("div");
      toastLiveRegion.id = "premium-toast-region";
      toastLiveRegion.setAttribute("aria-live", "polite");
      toastLiveRegion.setAttribute("role", "status");
      toastLiveRegion.setAttribute(
        "style",
        "position:fixed;left:50%;bottom:1.5rem;transform:translateX(-50%);" +
          "z-index:99999;pointer-events:none;display:flex;flex-direction:column;" +
          "gap:.5rem;align-items:center;margin:0;padding:0;"
      );
      doc.body.appendChild(toastLiveRegion);
    }
    return toastLiveRegion;
  }

  function showToast(message) {
    try {
      var region = ensureToastRegion();
      var toast = doc.createElement("div");
      toast.setAttribute("role", "status");
      toast.textContent = message;
      /* estilo inline: funciona mesmo antes/do premium.css carregar */
      toast.setAttribute(
        "style",
        "background:rgba(14,16,25,.92);-webkit-backdrop-filter:blur(20px) saturate(1.4);backdrop-filter:blur(20px) saturate(1.4);" +
          "border:1px solid rgba(255,255,255,.08);border-radius:12px;color:#e8ecf6;" +
          "font:500 .875rem/1.4 var(--font-sans, system-ui, sans-serif);" +
          "padding:.75rem 1.25rem;box-shadow:0 8px 24px rgba(0,0,0,.4);" +
          "max-width:min(24rem, 90vw);opacity:0;transform:translateY(8px);" +
          "transition:opacity var(--duration-fast, .25s) var(--ease-smooth-out, cubic-bezier(0.22,1,0.36,1))," +
          "transform var(--duration-fast, .25s) var(--ease-smooth-out, cubic-bezier(0.22,1,0.36,1));"
      );
      region.appendChild(toast);
      /* entra (fast = open) */
      requestAnimationFrame(function () {
        toast.style.opacity = "1";
        toast.style.transform = "translateY(0)";
      });
      /* sai (medium = toast close 350ms) */
      window.setTimeout(function () {
        toast.style.transitionDuration = "var(--duration-medium, .35s)";
        toast.style.opacity = "0";
        toast.style.transform = "translateY(8px)";
        window.setTimeout(function () {
          if (toast.parentNode) toast.parentNode.removeChild(toast);
        }, 400);
      }, 4200);
    } catch (e) { /* toast é progressive enhancement: falha silenciosa */ }
  }

  /* ---------- Form: toast em falha (não altera o form) ---------- */
  /* O site submete forms via JS/fetch (sem action). Não interceptamos
     nada: apenas anotamos QUE houve submit e, se nos segundos seguintes
     aparecer um erro/rejection com cara de rede, avisamos com um toast
     educado em região aria-live=polite. */
  var lastSubmitAt = -Infinity;
  var WINDOW_MS = 15000;

  doc.addEventListener(
    "submit",
    function () {
      lastSubmitAt = Date.now();
    },
    { capture: true, passive: true }
  );

  function isNetworkFailureMessage(msg) {
    return /network|fetch|load failed|failed to (fetch|load|send)|offline|timeout|aborted/i.test(msg);
  }

  function looksRelatedToSubmit() {
    return Date.now() - lastSubmitAt < WINDOW_MS;
  }

  function watchFormNetworkFailures() {
    /* Erros de script/requisição com sinal de rede */
    window.addEventListener("error", function (event) {
      var msg = ((event && event.message) || "") + "";
      if (isNetworkFailureMessage(msg)) {
        if (looksRelatedToSubmit()) {
          showToast("Não foi possível enviar sua mensagem. Verifique sua conexão e tente novamente.");
        } else {
          showToast("Não foi possível conectar. Verifique sua internet e tente novamente.");
        }
      }
    });

    /* Promise rejections não tratadas (fetch do form cai aqui) */
    window.addEventListener("unhandledrejection", function (event) {
      var reason = event && event.reason;
      var msg = "";
      if (reason) {
        msg = ((reason.message || "") + " " + (reason.name || "") + " " + (reason || "")).trim();
      }
      if (isNetworkFailureMessage(msg)) {
        if (looksRelatedToSubmit()) {
          showToast("Não foi possível enviar sua mensagem. Verifique sua conexão e tente novamente.");
        } else {
          showToast("Não foi possível concluir a ação. Tente novamente em instantes.");
        }
      }
    });
  }

  /* ---------- Init ---------- */
  function init() {
    try {
      markLoadedImages(doc);
      autoMarkReveal();
      observeReveals();
      watchFormNetworkFailures();
    } catch (e) {
      /* a camada premium nunca deve quebrar a página base */
    }
  }

  if (doc.readyState === "loading") {
    doc.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
