# Hyperframes Composition Brief: JALEP Corporação

## Objective
Create a short launch-style brag video for JALEP Corporação — a Next.js 16 tech-repair "enterprise" site that is actually a 7th-grade school project. The video treats it with total deadpan corporate seriousness and reveals "7° Ano A" as the final punchline.

## Output
- Composition directory: `brag-output/composition/`
- Rendered video: `brag-output/brag.mp4`
- Format: landscape — 1920x1080
- Duration: 21 seconds

## Source Material
- Project root: `~/jalep-mano` (static Next.js export; the live site is https://sudoxddx.github.io/jalep-mano/)
- Primary files read: `index.html` (hero, services, lab, specs, budget form, footer), `manifest.json`, `_next/static/chunks/1wk3i7t9txvj-.css` (design tokens), `status.html`, `jalepos.html`, `team.html`, `changelog.html`, `data/repair-database.json` (250 repair cases powering the AI quote engine)
- Product name: JALEP Corporação
- Tagline / strongest claim: "Diagnóstico preciso. Reparo certeiro. Zero improviso."
- Key UI or visual moment to recreate: the neon-card stat row (4 / 2026 / 100% / 7) and the "Simular Orçamento" form with its chip selectors
- Copy that must appear verbatim (Portuguese, from the actual site):
  - `jalep//` (nav logo)
  - "Assistência Técnica Profissional"
  - "4 Serviços · 2026 Fundação · 100% Compromisso · 7 Turma"
  - "Taxa de Sucesso" → "100%" and "Improvisos" → "0"
  - "Solicitar Orçamento" / "Simular Orçamento" (button copy)
  - "Orçamento gerado por IA — valores são estimativas."
  - "Diagnóstico Engine · Lab API · JalepOS Runtime" + "Operacional"
  - "© 2026 JALEP Corporação — 7° Ano A"
  - Optional flavor (grounded in repair-database.json): "250 casos · R$ 234.474 · RC-2025-0019 · Logitech MX Master 3S · RAM slot failure · R$ 441,39"

## Creative Direction
- Tone preset: yc-parody
- Creative direction: "Fake Series-A launch for an enterprise repair corporation — delivered with total deadpan seriousness"
- Interpretation: structured pacing, hard cuts, corporate-metric typography, restrained motion. Humor comes only from specificity and the final reveal. No winks, no cartoon energy, no goofy SFX.
- Angle: The video sells JALEP as a funded enterprise: metrics, an AI quote engine, an operating system, live infrastructure status. The final beat quietly reveals the footer truth: it's a 7th-grade class project ("7° Ano A"). The joke is never stated; it recontextualizes everything.
- Hook (first 2-3s): terminal boot — blinking cursor types `jalep://`, blue dot pulses, then the hero tag "Assistência Técnica Profissional" settles.
- Outro / punchline: `jalep//` + "JALEP Corporação" hold, then the quiet mono line "© 2026 — 7° Ano A" fades in and holds in near-silence.
- Avoid:
  - Generic SaaS language ("streamline your workflow" etc.) — use only the site's actual copy
  - Abstract filler visuals — every scene recreates real UI from the site
  - Any visual redesign — match the site's exact dark navy + neon-blue identity

## Visual Identity
- Background: `#0E1019`
- Card/surface: `#181D32`, hover surface `#1E2440`
- Text: `#E8ECF6` (primary), `#9098B8` (secondary), `#5C6280` (muted)
- Accent: `#82B1FF` (primary blue; also used for glows: `box-shadow: 0 0 12px rgba(130,177,255,0.15)`, dim fill `rgba(130,177,255,0.12)`, border `rgba(130,177,255,0.28)`)
- Secondary accents (use sparingly): `#18FFFF` cyan, `#B388FF` violet, `#69F0AE` green (status "Operacional" tiles), `#FFD740` amber
- Display font: Google Sans Flex (fallback: Inter, system sans)
- Body/mono font: JetBrains Mono (fallback: ui-monospace) — all labels, numbers, chips, kickers are mono
- Visual references from the project:
  - `neon-card`: glassy dark card `#181D32`, 1px border `rgba(255,255,255,0.06)`, radius ~20px, soft blue glow on emphasis
  - `hero-tag`: small blue dot (8px, glow `0 0 6px #82B1FF`) + mono label
  - `chip`: pill/rounded-2xl mono tag, selected state = blue dim bg + blue border + blue text + dot indicator
  - `spec-bar`: thin track with blue fill bar animating to 100%
  - `stat-card`: icon + big number (Google Sans Flex bold) + tiny mono label
  - Status tiles: green `#69F0AE` dot/text "Operacional"

## Storyboard
Use the storyboard in `brag-output/brag-plan.md` as the creative contract.

Scene summary (21.0s total):
1. **boot** — 0.0–3.0s — `jalep://` types on dark bg (JetBrains Mono), blinking cursor, blue dot pops, tag "Assistência Técnica Profissional" settles. Must read: `jalep://` and the tag.
2. **a empresa** — 3.0–6.5s — the four real stat cards slide in one by one (4 Serviços / 2026 Fundação / 100% Compromisso / 7 Turma), numbers count up. Must read: all four stat labels + numbers.
3. **especificações** — 6.5–9.5s — left: "Taxa de Sucesso" spec-bar fills 0→100% with "100%" readout; right: glass card counts "0 Improvisos" landing on 0. Must read: "Taxa de Sucesso 100%" and "0 Improvisos".
4. **orçamento IA** — 9.5–14.0s — budget form: service chips appear (Upgrade/Reparo/Diagnóstico/Outro), simulated cursor clicks "Upgrade"; device chips, cursor clicks "Notebook"; result card materializes with real DB case (RC-2025-0019 · Logitech MX Master 3S · RAM slot failure · R$ 441,39) and tiny note "Orçamento gerado por IA — valores são estimativas." Must read: "Simular Orçamento", the selected chips, and the result card's device + price.
5. **JalepOS + Status** — 14.0–17.5s — left: JalepOS desktop window (title "JalepOS v0.1", dock icons Dashboard/Inventário/Comunicação/Analytics/Config); right: three status tiles flip to green "Operacional" (Diagnóstico Engine, Lab API, JalepOS Runtime). Must read: "JalepOS" and at least two "Operacional" tiles.
6. **punchline** — 17.5–21.0s — `jalep//` logo + "JALEP Corporação" centered on dark; then quiet mono line "© 2026 — 7° Ano A" fades in below; hold to end in near-silence. Must read: "JALEP Corporação" and "7° Ano A".

## Audio
- Audio role: warm corporate bed with sparse professional accents
- Audio arc: music enters at frame 0 with the boot, carries the corporate montage, ducks slightly at the punchline, fades to near-silence for the final hold
- Music: `happy-beats-business-moves-vol-11-by-ende-dot-app.mp3` (114.84 BPM, warm/business-y)
- Music treatment: volume ~0.30; start 0.0s; fade out across 19.5–21.0s to ~0.05 for the final hold
- Music cue guidance: bundled preset at `<skill-dir>/assets/music/cues/happy-beats-business-moves-vol-11-by-ende-dot-app.music-cues.json` (also copied to `brag-output/composition/assets/music/cues/`). Strong cues in window: 1.60, 3.70, 5.80, 6.34, 8.96, 9.50, 12.65, 17.91, 22.65, 24.23. Beat grid ≈ every 0.525s (see .md/.json).
- Audio-reactive treatment: subtle — the hero blue-dot glow and card presence may breathe with music RMS; no waveform/equalizer visuals, no strobing.
- Audio-coupled moments:
  - Scene 1 hook: typed `jalep://` with randomized `keyboard/keypress-*.wav` ticks; dot pop on a beat
  - Scene 2: stat card arrivals on every-other-beat (readable text) — target beats 3.18, 4.23, 5.28, 6.34 (6.34 is a strong cue; final card may nudge ±0.15s to it)
  - Scene 3: spec-bar fill swish; "0" landing tick near 9.50s strong cue
  - Scene 4: soft `interface/click_*` on chip selections (consecutive beats OK — selection accents, not text reads); one dry success hit (`impact/impactBell_heavy_000` or `impactSoft_medium_*`) when the result card resolves
  - Scene 5: dock icon pops + status tile flips on every-other-beat, restrained
  - Scene 6: near-silence; optional single quiet logo hit (`impactSoft_medium_*`) at the logo slam (~17.91s strong cue), nothing after
- SFX selection guidance: yc-parody = sparse, 2-4 restrained cues total beyond typing/clicks. Prefer low HF-risk files: `impact/impactSoft_medium_001/002/004` for reveals/transitions, `interface/click_002/003/005` for simulated clicks, `ui/click2` as alternative, `keyboard/keypress-*` randomized for typing, one `impact/impactBell_heavy_000` (medium risk, isolated) for the quote-card payoff. Avoid casino family here (too playful for deadpan).
- SFX analysis guidance: `<skill-dir>/assets/sfx/sfx-analysis.md` (same dir as the SFX library)
- Exact SFX choice: Hyperframes decides filenames, timestamps, density, and volume based on the implemented animation.
- Audio files: copy the music (already planned) and Hyperframes-selected SFX into `brag-output/composition/assets/`

## Hyperframes Instructions
Load the composition-building Hyperframes domain skills — `hyperframes-core` (composition contract + `data-*` timing), `hyperframes-animation` (motion), `hyperframes-creative` (design spec, beats, audio-reactive), `hyperframes-keyframes` (seek-safe keyframes), and `hyperframes-cli` (lint/check/render). /brag is its own workflow: do not enter the `hyperframes` entry-point intent interview and do not route into its generic promo / launch-video workflow. Prefer native Hyperframes conventions over anything in `/brag`.

Requirements:
- Show at least one real UI, copy, or visual element from the source project (this video recreates five: hero tag, stat row, spec bars, budget form, status tiles + JalepOS).
- Keep all text readable in the final render. Portuguese copy verbatim from the site (including accents: "Assistência Técnica Profissional", "Orçamento", "Ano").
- Keep the video within 15-25 seconds (target 21.0s).
- Include the planned music/SFX layer as specified above.
- Treat `/brag` audio notes as guidance, not a fixed cue sheet. Choose SFX after the visual animation exists.
- Treat music cue metadata as optional timing hints. Major reveals may move toward strong cues within ~0.15s; smaller entrances to beats within ~0.10s. Use only 1-3 strong cue locks (suggested: hook tag settle ~1.60s, "0 Improvisos" landing ~9.50s, final logo ~17.91s).
- Sequential TEXT (stat labels, status tiles) snaps to every-other-beat (~1.05s spacing) to respect the ~0.8s readable-label floor; selection clicks/chip accents may hit consecutive beats.
- When music is present, consider the Hyperframes audio-reactive workflow (per `hyperframes-creative`): subtle glow/presence modulation only.
- Use local assets (copy music + SFX into `composition/assets/`).
- Run `hyperframes check` before render — it is brag's single gate.
- Keep creation and rendering local. No remote publishing.
