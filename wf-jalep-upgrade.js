export const meta = {
  name: 'jalep-massive-upgrade',
  description: 'Upgrade massivo do site JALEP: layer de design premium global (glassmorphism premium, animacoes, efeitos) + revisao Web Interface Guidelines em todas as 23 paginas + verify adversarial',
  phases: [
    { title: 'Upgrade', detail: 'design global + auditoria por pagina' },
    { title: 'Verify', detail: 'cross-check de regressao' },
  ],
}

const SITE = '/data/data/com.termux/files/home/jalep-mano'

const GL = `
Você esta melhorando o site estatico da JALEP Corporação (assistencia tecnica),
export de Next.js (HTML estatico + Tailwind CSS 4 compilado, dark mode nativo
data-mode="dark", hospedado em sudoxddx.github.io/jalep-mano/). 23 paginas .html
na raiz. Assets em _next/static/chunks (NAO mexer nos chunks). svgs/, icons/,
lottie/ disponiveis. O dono pediu "upgrade MASSIVO" usando as Web Interface
Guidelines (vercel-labs) — o texto completo das regras esta abaixo.

REGRAS-CHAVE DA GUIDELINE (aplique sem pedir confirmacao):
- Acessibilidade: aria-label em icon-buttons, alt em imgs, <button> pra acao
  <a> pra navegacao, headings h1-h6 em ordem, focus-visible visivel
- Animacao: so transform/opacity, prefers-reduced-motion respeitado, nada de
  transition:all, interrompivel
- Tipografia: text-wrap:balance nos headings, tabular-nums em numeros, ... -> …
- Formularios: label/aria-label, autocomplete, type certo, paste liberado
- Performance: img com width/height, loading=lazy abaixo da dobra,
  preconnect p/ fonts.googleapis.com e fonts.gstatic.com
- Dark: color-scheme:dark no html (ja tem), theme-color meta
- Touch: touch-action:manipulation, overscroll-behavior em modais
- Anti-patterns: SEM user-scalable=no, SEM outline-none sem replacement,
  SEM divs clicaveis, SEM transition:all
- Copy: voz ativa, Title Case nos headings, numerals, rotulos especificos

COMO TRABALHAR: edite os .html com Edit/Write (arquivos estaticos — injeção
segura de <style>/<script> no head e classes utilitarias). NAO recompile
Next (nao temos o fonte TS, so o export). Melhoras visuais entram como CSS
custom num <style id="jalep-premium"> no head de cada pagina + classes.
`

const DESIGN_SCHEMA = {
  type: 'object',
  properties: {
    cssFile: { type: 'string' },
    jsFile: { type: 'string' },
    features: { type: 'array', items: { type: 'string' } },
    pagesPatched: { type: 'array', items: { type: 'string' } },
    notes: { type: 'string' },
  },
  required: ['cssFile', 'jsFile', 'features', 'pagesPatched'],
}

const PAGE_SCHEMA = {
  type: 'object',
  properties: {
    page: { type: 'string' },
    fixes: { type: 'array', items: { type: 'string' } },
    upgrades: { type: 'array', items: { type: 'string' } },
    remaining: { type: 'string' },
  },
  required: ['page', 'fixes', 'upgrades'],
}

const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    findings: { type: 'array', items: { type: 'object', properties: {
      page: { type: 'string' }, issue: { type: 'string' }, severity: { type: 'string' } },
      required: ['page', 'issue'] } },
    summary: { type: 'string' },
  },
  required: ['findings', 'summary'],
}

phase('Upgrade')

// AGENTE 1: o design system premium global — cria os assets + injeta em TODAS as paginas
const design = await agent(GL + `
TAREFA-NOBRE: crie o LAYER DE DESIGN PREMIUM "JALEP 2.0" e injete em todas as 23 paginas.

1. Crie ${SITE}/assets/premium.css com (TUDO vanilla CSS, sem dependencia externa):
   - Glassmorphism refinado: cards com backdrop-filter blur(20px) saturate(1.4),
     borda 1px rgba(255,255,255,.08), sombra profunda multi-layer, radius 20px
   - Gradiente animado sutil no fundo do body (radial-gradients em --color-primary/
     --color-accent, animacao transform lenta, opacity baixa) — em cima do dark atual
   - Hover premium em cards/links: translateY(-2px) + glow shadow, transition
     transform .2s, opacity .2s (listadas, nunca all), respects prefers-reduced-motion
   - Botao primario com shine sweep no hover (::before com gradiente branco
     translucido, transform translateX)
   - Scrollbar custom (webkit + firefox) no tema
   - Selecao de texto ::selection com cor da marca
   - Focus-visible: ring 2px var(--color-primary) offset 2px em TODOS interativos
   - Reveal-on-scroll: .reveal { opacity:0; translateY(12px) } .reveal.in { opacity:1;
     translateY(0) } transition transform .5s cubic-bezier, com @media
     (prefers-reduced-motion: reduce) { .reveal { opacity:1; transform:none } }
   - Tipografia: h1,h2,h3 { text-wrap:balance }, numeros tabular-nums onde listar
   - Skeleton shimmer leve pra imgs (background gradiente animado ate load)
   - Melhorias em light-mode tambem (data-mode="light" existe? use :not([data-mode="dark"]))
2. Crie ${SITE}/assets/premium.js com (vanilla, defer-safe):
   - IntersectionObserver aplicando .in aos .reveal (threshold .12)
   - Auto-marcar filhos de secoes main com .reveal (h2, p, cards — seletor seguro:
     'main h2, main h3, main p, main .card, main img' — classe so se nao tiver)
   - prefers-reduced-motion: pula tudo
   - Toast leve (aria-live=polite) se form submit falhar (nao altera o form)
3. Injete nas 23 paginas (Write/Edit em cada): <link premium.css> + <script
   defer premium.js> ANTES de </head>, apos os chunks existentes.
4. meta theme-color #0a0a0c (dark) em todas.
5. Liste tudo em features/pagesPatched.
Nao remova nada existente — so somar.`, { label: 'design:premium-layer', phase: 'Upgrade', schema: DESIGN_SCHEMA, effort: 'high' })

// AGENTES 2-5: auditoria+fix das paginas em paralelo (batch)
const allPages = ['index.html','servicos.html','hardware.html','portfolio.html','pricing.html','sobre.html','contato.html','faq.html','blog.html','docs.html','changelog.html','depoimentos.html','parceiros.html','team.html','timeline.html','lab.html','stack.html','status.html','terminal.html','wallpaper.html','jalepos.html','404.html','_not-found.html']
const batches = [
  allPages.slice(0, 5),   // core
  allPages.slice(5, 10),
  allPages.slice(10, 15),
  allPages.slice(15, 23), // resto
]

const audits = await parallel(batches.map((b, i) => () => agent(GL + `
TAREFA: auditoria + correcao das paginas ${JSON.stringify(b)} conforme a guideline.
Para CADA pagina:
1. Read no arquivo.
2. CORRIJA (Edit direto): aria-labels faltando em icon-buttons, alt em imgs,
   labels em inputs, type certo (email/tel), loading=lazy abaixo da dobra,
   width/height em imgs, outline-none sem replacement, divs clicaveis ->
   button/a, ... -> …, headings fora de ordem, placeholders com exemplo.
3. UPGRADES visuais com classes do premium.css (reveal, etc) onde somar.
4. Retorne fixes/upgrades EXATOS por pagina (array), remaining = o que nao
   coube sem quebrar.
Nao reescreva pagina inteira — Edits cirurgicos.`, { label: 'audit:batch' + (i + 1), phase: 'Upgrade', schema: PAGE_SCHEMA, effort: 'high' })))

log('Design + auditorias prontos — verify adversarial')

phase('Verify')
const verify = await agent(GL + `
TAREFA: VERIFICADOR ADVERSARIAL pos-upgrade. Leia TODAS as 23 paginas
(${'index, servicos, hardware, portfolio, pricing, sobre, contato, faq, blog, docs, changelog, depoimentos, parceiros, team, timeline, lab, stack, status, terminal, wallpaper, jalepos, 404, _not-found'}.html)
+ ${SITE}/assets/premium.css + premium.js e cace REGRESSOES:
- tags quebradas (link/script injetados duplicados ou fora do head)
- CSS que conflita com o Tailwind existente (overrides de classes core)
- prefers-reduced-motion realmente coberto
- nenhuma animacao usando propriedades caras (width/height/top/layout)
- nenhuma remocao de conteudo original (diff semantico: secoes sumidas?)
- performance: premium.css < 15KB? js < 5KB? inline ou link?
Reporte findings page+issue+severity; summary com veredito GO/NO-GO.`, { label: 'verify:regression', phase: 'Verify', schema: VERIFY_SCHEMA, effort: 'high' })

return { design, audits: audits.filter(Boolean), verify }
