/* JALEP Mano UI layer: no dependencies; progressive enhancement only. */
(() => {
  "use strict";
  const doc = document;
  const root = doc.documentElement;
  const reduced = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);

  if (!doc.getElementById("jalep-skip-link")) {
    const skip = doc.createElement("a");
    skip.id = "jalep-skip-link";
    skip.href = "#main-content";
    skip.textContent = "Pular para o conteúdo";
    doc.body.prepend(skip);
  }
  const main = doc.querySelector("main");
  if (main && !main.id) main.id = "main-content";

  let progress = doc.getElementById("jalep-reading-progress");
  if (!progress) {
    progress = doc.createElement("div");
    progress.id = "jalep-reading-progress";
    progress.setAttribute("aria-hidden", "true");
    doc.body.appendChild(progress);
  }

  let topButton = doc.getElementById("jalep-back-top");
  if (!topButton) {
    topButton = doc.createElement("button");
    topButton.id = "jalep-back-top";
    topButton.type = "button";
    topButton.setAttribute("aria-label", "Voltar ao topo");
    topButton.title = "Voltar ao topo";
    topButton.innerHTML = '<span aria-hidden="true">↑</span>';
    doc.body.appendChild(topButton);
  }
  topButton.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
  });

  let scheduled = false;
  function updateScrollUI() {
    scheduled = false;
    const max = Math.max(1, doc.documentElement.scrollHeight - window.innerHeight);
    const ratio = Math.min(1, Math.max(0, window.scrollY / max));
    progress.style.width = `${ratio * 100}%`;
    topButton.classList.toggle("is-visible", window.scrollY > 480);
  }
  function onScroll() {
    if (!scheduled) {
      scheduled = true;
      window.requestAnimationFrame(updateScrollUI);
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
  updateScrollUI();

  // Close the native details-based mobile menu after navigation or Escape.
  doc.querySelectorAll("header details").forEach((details) => {
    details.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        details.open = false;
        const summary = details.querySelector("summary");
        if (summary) summary.focus();
      }
    });
    details.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => { details.open = false; });
    });
  });

  // Mark the current navigation destination for assistive technologies.
  const current = window.location.pathname.replace(/\/+$/, "") || "/";
  doc.querySelectorAll("header nav a[href]").forEach((link) => {
    try {
      const url = new URL(link.href, window.location.href);
      const path = url.pathname.replace(/\/+$/, "") || "/";
      if (path === current && !link.hasAttribute("aria-current")) {
        link.setAttribute("aria-current", "page");
      }
    } catch (_) { /* invalid link: leave unchanged */ }
  });

  root.dataset.jalepOverhaul = "ready";
})();
