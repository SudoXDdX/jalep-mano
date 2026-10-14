/**
 * JALEP 2.0 — Injetor da camada premium nas páginas estáticas.
 * Uso: bun /data/data/com.termux/files/home/jalep-mano/assets/inject-premium.ts
 *
 * Idempotente: reexecutar não duplica tags.
 * Escrita atômica (tmp + rename) — seguro contra desligamento no meio.
 * Somente soma: nada existente é removido.
 */
import { readFileSync, writeFileSync, renameSync } from "node:fs";

const ROOT = "/data/data/com.termux/files/home/jalep-mano";
const PAGES = [
  "404.html",
  "_not-found.html",
  "blog.html",
  "changelog.html",
  "contato.html",
  "depoimentos.html",
  "docs.html",
  "faq.html",
  "hardware.html",
  "index.html",
  "jalepos.html",
  "lab.html",
  "parceiros.html",
  "portfolio.html",
  "pricing.html",
  "servicos.html",
  "sobre.html",
  "stack.html",
  "status.html",
  "team.html",
  "terminal.html",
  "timeline.html",
  "wallpaper.html",
];

const INJECT = [
  '<meta name="theme-color" content="#0a0a0c"/>',
  '<link rel="stylesheet" href="/jalep-mano/assets/premium.css" data-precedence="premium"/>',
  '<script defer src="/jalep-mano/assets/premium.js" data-precedence="premium"></script>',
].join("");

const results: { file: string; status: string }[] = [];

for (const page of PAGES) {
  const path = `${ROOT}/${page}`;
  try {
    let html = readFileSync(path, "utf8");

    if (html.includes("premium.css") && html.includes("premium.js")) {
      // já injetado: apenas garantir theme-color
      if (!html.includes('name="theme-color"')) {
        html = html.replace("</title>", `</title>${'<meta name="theme-color" content="#0a0a0c"/>'}`);
        writeFileSync(path, html);
        results.push({ file: page, status: "theme-color added (assets already present)" });
      } else {
        results.push({ file: page, status: "already patched (skip)" });
      }
      continue;
    }

    if (!html.includes("</head>")) {
      results.push({ file: page, status: "NO </head> — SKIPPED" });
      continue;
    }

    // Injeta ANTES de </head> (após todos os chunks existentes) e soma theme-color
    let payload = "";
    if (!html.includes('name="theme-color"')) payload += '<meta name="theme-color" content="#0a0a0c"/>';
    payload += INJECT.replace('<meta name="theme-color" content="#0a0a0c"/>', "");
    html = html.replace("</head>", `${payload}</head>`);

    // Escrita atômica: nunca deixa arquivo corrompido se o processo morrer
    const tmp = `${path}.jalep-premium.tmp`;
    writeFileSync(tmp, html);
    renameSync(tmp, path);
    results.push({ file: page, status: "patched" });
  } catch (err) {
    results.push({ file: page, status: `ERROR: ${err}` });
  }
}

for (const r of results) console.log(`${r.status.padEnd(45)} ${r.file}`);
const patched = results.filter((r) => r.status === "patched").length;
console.log(`\n${patched}/${PAGES.length} patched this run`);
