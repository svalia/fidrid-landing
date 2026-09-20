# Dark Keynote — дизайн-система Martech / СберМаркетинг

Reusable design system extracted from the **Martech** project: the dark, cinematic
"product-keynote" language used across the E2E roadmap decks, the agency-workspace
landing, and the Plasma integration schemas. Near-black navy canvas, white Golos Text,
cyan→blue and lavender→purple gradients, frosted-glass cards, long soft entrance motion.

> **Brand origin:** СберМаркетинг (sbermarketing.ru). The source decks were built in this
> keynote idiom for the Campaign Manager / Plasma E2E initiative.

---

## Sources analysed (provenance — stored under `reference/`)
- `reference/martech-keynote.html` — the master scrolling keynote ("Рабочее место сотрудника
  агентства"): hero, the agent-workspace proof scene, vision, architecture, risks, ask.
- `reference/SberMarketing_style_map.md` — colour/type/component map reverse-engineered from
  the live sbermarketing.ru CSS + screenshots (the basis for the tokens).
- `reference/brief.md` — the CM design-process briefing.
- `reference/roadmap_e2e_baza_prezentacii.md` — E2E roadmap presentation base.
- Diagram assets: `assets/schema-2026.png`, `assets/schema-2027.png`, `assets/status-*.png`.

The original Martech zip also contained standalone deck exports (E2E schemas, "Развилка CM",
the workspace landing). They were summarised here rather than copied wholesale.

---

## CONTENT FUNDAMENTALS — how copy is written
- **Language:** Russian, professional but human. Business-domain terms (медиаплан, бриф,
  согласование, ДЗО/ПАО, Trading Desk) used precisely, not dumbed down.
- **Voice:** confident, declarative, keynote-style. Short punchy headlines, one idea each.
  Bodies explain the *why* in 1–3 sentences.
- **Person:** mostly impersonal / 3rd-person ("Plasma становится центром расчёта"). Occasional
  2nd-person for the reader in landing contexts.
- **Casing:** sentence case for body; product names keep their own casing (Plasma, Trading
  Desk, Битрикс24, МАРК, AdPilot). Eyebrows & act-labels are UPPERCASE with wide tracking.
- **Emphasis:** key terms bolded to full-white inside muted paragraphs (`<b>` → `#fff`).
- **No emoji.** Iconography is geometric/structural, not decorative.
- **Vibe:** «Apple/Huawei keynote × enterprise martech». Calm authority, generous whitespace,
  one statement per beat. Headline pattern: plain noun phrase with the load-bearing word in a gradient.

---

## VISUAL FOUNDATIONS
- **Canvas:** deep navy `--bg #05101E` (never pure black); `--bg-2` for panels. Persistent
  **ambient field** — two huge blurred radial orbs (blue top-left, purple bottom-right,
  `blur(120px)`, opacity ~.5) fixed behind all content (`.ambient`).
- **Type:** **Golos Text** (variable) for everything — display & body share the family,
  separated by weight. Display/headlines 600; body 400; labels 500–600. Headlines carry tight
  negative tracking (`-.02em`→`-.035em`); uppercase labels `+.14em`–`.16em`. Headlines
  `text-wrap: balance`, bodies `text-wrap: pretty`.
- **Colour usage:** white text on navy. Accent only through **gradients on text/fills**, not
  flat blocks. Cyan→blue (`--grad-cta`, `--grad-headline-rich`) = primary/energy; lavender→
  purple→cyan (`--grad-section`) = section identity; green `--green #2BFDCC` = "go"/target.
  Purple-soft tints act-labels.
- **Surfaces / cards:** frosted glass — `--surface-1/2/3` (white @ 10/5/2.5% alpha) +
  `backdrop-filter: blur()` + 1px `--border-soft` hairline. Radius `--radius-card 28px`;
  chips/eyebrows fully pilled at `--radius-pill 40px`. Big soft outer shadows only on elevated
  frames (`0 40px 120px rgba(0,0,0,.45)`); most cards rely on the hairline, not shadow.
- **Borders:** white at descending alpha (`--border .40` → `--border-faint .06`).
- **Buttons:** round gradient "circle + label" CTA (`--grad-cta`, scales 1.08 on hover); quiet
  text buttons (muted→white); nav CTA is a pilled glass chip.
- **Motion:** long soft settle — `--ease-soft cubic-bezier(.16,.84,.34,1)` over ~1s, staggered
  by `--i * 90ms`. Entrances fade-up / line-mask reveals; scroll-driven sticky "scenes" in the
  landing. End-state is the base style, animate *from* hidden, gated on reduced-motion. No
  infinite decorative loops.
- **Hover/press:** lift (`translateY(-1px..-6px)`) + brighten / cyan border; press is light.
- **Transparency & blur:** core to the look — glass chrome, blurred ambient, `blur(20–24px)`
  sticky nav. **Light schema cards (`#f6f8fc`) are the deliberate exception** so dense diagrams
  stay legible against the dark page.
- **Imagery vibe:** cool, technical, structural. Diagrams over photography.

---

## ICONOGRAPHY
- The system is **icon-light** — meaning is carried by typography, gradients and structure.
  No bundled icon font.
- Where marks appear they are **tiny geometric primitives**: gradient dots (`.eyebrow .dot`),
  the brand mark tile (rounded square filled with `--grad-cta`, glyph «М»), macOS traffic dots
  on app frames, thin inline-SVG line icons (1.6–1.7px stroke) tinted per accent in the vision cards.
- **No emoji.** If a broader icon set is needed, use a thin-stroke line set (e.g. Lucide via CDN)
  tinted `--text-muted` — flagged as a substitution; the source decks ship none.

---

## VISUAL ASSETS
Type- and token-driven brand. The "logo" is the **Golos wordmark + gradient mark tile** («М»).
Real raster assets present are the integration **schema diagrams** and **media-plan status**
shots in `assets/`. No official SberMarketing logo files were in the source — drop them into
`assets/` and document here if they become available.

---

## Index / manifest

**Root entry (consumers link only this):**
- `styles.css` — `@import`s fonts → tokens → base. Nothing inline.
- `golos-embed.css` — Golos Text variable webfont, embedded (no external deps).
- `base.css` — reset + reusable utility/component classes (`.wrap`, `.eyebrow`,
  `.section-title`, `.lede`, `.act-label`, `.grad-text`, `.nav`, `.btn-round`, glass cards,
  the `.app*` workspace frame, plus landing scene classes).

**Tokens** (`tokens/`): `colors.css` · `typography.css` · `effects.css` · `layout.css` (48 tokens).

**Foundation cards** (`guidelines/`) — 15 specimen cards in the Design System tab
(Цвет, Типографика, Сетка, Эффекты, Иконки, Бренд).

**Components** (`components/core/`) — React primitives: `Button`, `Badge`, `GlassCard`, `StatCard`
(+ `core.card.html` showcase). Bundle namespace `window.DarkKeynoteMartechDesignSystem_7ee322`.

**Showcase** (`showcase/`) — extra static state galleries (buttons, badges, cards, nav, stats,
status, schema).

**Sample slides** (`slides/`) — `TitleSlide`, `SectionSlide`, `StatementSlide` (1280×720).

**UI kit** (`ui_kits/workspace/`) — interactive recreation of the **agency agent workspace**:
the AI assistant that builds a context-ad media plan from a brief and exports it.

**Template** (`templates/keynote/`) — `Keynote.dc.html`, a copy-and-edit dark keynote deck
(title · manifesto · numbers). The consumer-facing starting point.

`SKILL.md` — Agent-Skill manifest for Claude Code / downloaded-skill use.

---

## CAVEATS
- **Font substitution:** only **Golos Text** is embedded. The brand face is **SB Sans
  Display / SB Sans Text** (named as fallbacks but not shipped — licensing). Golos Text is a
  very close open match. If you have the official SB Sans files, add them and update
  `golos-embed.css` / `tokens/typography.css`.
- No official SberMarketing logo/photographic assets were in the source; the wordmark + mark
  tile stand in.
