# ASB brand kit

Logo files for AgenticScienceBuilder (ASB) and the ASB Skill Collections.

The mark is a tower crane that lifts a platform with three building blocks: code (`</>`), mathematics (`Σ`) and data (a bar chart). It is a vector redraw of the 244 x 228 px logo used in ASB talks. The colours follow the CNRS charter already used by the ASB spec site.

## Files

Brand folder per repository:

| Repository | Folder |
|---|---|
| asb-skill-collections | `assets/brand/` |
| AgenticScienceBuilder | `docs/assets/brand/` |

| File | Content | Ground | Collections | ASB |
|---|---|---|---|---|
| `asb-logo.svg` | mark and wordmark, one line | light | yes | yes |
| `asb-logo-dark.svg` | mark and wordmark, one line | dark | yes | yes |
| `asb-mark.svg` | mark only, 256 x 256 square | light | yes | yes |
| `asb-mark-dark.svg` | mark only, 256 x 256 square | dark | yes | yes |
| `asb-wordmark.svg` | wordmark only | light | yes | yes |
| `favicon.svg` | simplified mark on a 32 x 32 grid | follows the browser scheme | yes | yes |
| `asb-logo-512.png` | `asb-logo.svg` at 512 x 98 px, transparent | light | yes | yes |
| `asb-collections-lockup.svg` | mark, "ASB Skill Collections", subtitle "AgenticScienceBuilder" | light | yes | no |
| `asb-collections-lockup-dark.svg` | same | dark | yes | no |

Which file where:

| Place | File |
|---|---|
| README header, asb-skill-collections | `asb-collections-lockup.svg` with its dark file, or `asb-logo.svg` with its dark file |
| README header, AgenticScienceBuilder | `asb-logo.svg` with `asb-logo-dark.svg` |
| Slides on paper or white | `asb-logo.svg` |
| Slides or bars on navy or black | `asb-logo-dark.svg`, `asb-mark-dark.svg` |
| Avatar, social card, square slot | `asb-mark.svg` or `asb-mark-dark.svg` |
| Name already set in text nearby | `asb-mark.svg` |
| Browser tab, 16 to 32 px | `favicon.svg` |
| Tools that refuse SVG | `asb-logo-512.png` |

All SVGs have a `viewBox`, no embedded raster, no external font and no external reference. The wordmark is drawn as outlines from IBM Plex Sans Medium (SIL Open Font License 1.1), so the logo looks the same without the font installed. Each SVG carries a `<title>` and a `<desc>`.

The Indicium standard has a sibling mark in the same palette and stroke weights: a record sheet with three claim lines, bound by a round seal. It lives in the Indicium repository and has no crane.

## Palette

| Token | Hex | Role |
|---|---|---|
| navy | `#00284b` | crane and wordmark on light grounds (CNRS blue) |
| blue-ink | `#001833` | dark page ground |
| blue-soft | `#0d3a66` | secondary navy |
| orange | `#e06c0a` | load blocks on light grounds |
| orange-dark | `#f5923a` | load blocks on dark grounds |
| paper | `#fbf7ef` | light page ground; crane and wordmark on dark grounds |
| paper-2 | `#f3ecdc` | inset surfaces, code blocks |
| ink | `#16242f` | body text |
| mute | `#5d6a78` | subtitle on light grounds |
| mute-dark | `#aebccb` | subtitle on dark grounds |
| yellow | `#ffeb6e` | CNRS accent; not used in the logo |
| yellow-soft | `#fff5a6` | highlight; not used in the logo |
| teal | `#04919a` | links on the spec site; not used in the logo |

Secondary CNRS tones for figures and charts, not for the logo: pale blue `#9ae2ff`, green `#b0ee89`, orange `#ffbc75`, violet `#6941eb`, grey `#8296a5`.

The logo uses two colours per ground: navy and orange on light, paper and orange-dark on dark. The load orange is the colour of the original logo, deepened so that it keeps a 3:1 contrast on white.

Contrast (WCAG 2):

| Pair | Ratio |
|---|---|
| navy on white | 14.95 |
| navy on paper | 13.99 |
| orange on white | 3.32 |
| orange on paper | 3.11 |
| paper on `#0d1117` | 17.71 |
| paper on navy | 13.99 |
| orange-dark on `#0d1117` | 8.16 |
| orange-dark on navy | 6.44 |

## Type

| Use | Font |
|---|---|
| Wordmark | IBM Plex Sans Medium (500), as outlines |
| Subtitle in the collections lockup | IBM Plex Sans Regular (400), as outlines |
| Text and interface | IBM Plex Sans |
| Headings on the spec site | IBM Plex Serif |
| Code | IBM Plex Mono |

## Geometry

- The mark is drawn on a 256-unit square.
- Strokes: 7 units for the mast, cat-head and jib chords; 5 units for the lattice, jib web, ties, hoist cable and sling; 7 units for the load glyphs. Round caps and joins.
- The load hangs under the hook: hook and platform share the same centre line.
- In the lockups the cap height of the wordmark is centred on the mark. The gap between mark and wordmark is 44 units, about one fifth of the mark height.
- `favicon.svg` is a separate drawing on a 32-unit grid with solid shapes. It is not the mark scaled down.

## Clear space and minimum size

- Clear space around a lockup: at least the cap height of the wordmark on every side. That is about a quarter of the logo height.
- Clear space around the mark alone: at least one eighth of its width.
- `asb-logo.svg`: at least 48 px tall (about 250 px wide). Below that the three blocks merge.
- `asb-collections-lockup.svg`: at least 280 px wide. Below that the subtitle falls under 8 px cap height.
- `asb-mark.svg`: at least 48 px. At 32 px and below use `favicon.svg`.

Do not stretch, rotate, outline or recolour the files. Do not add shadows or gradients. Do not put the light files on dark grounds. Do not reset the wordmark in another font.

## GitHub README snippet

The `<picture>` element picks the source that matches `prefers-color-scheme`. The `<img>` falls back to the light file.

asb-skill-collections (`README.md` at the repository root):

```html
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/brand/asb-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/brand/asb-logo.svg">
    <img alt="AgenticScienceBuilder" src="assets/brand/asb-logo.svg" width="320">
  </picture>
</p>
```

For the collections lockup, replace `asb-logo` with `asb-collections-lockup` in the three paths and use `alt="ASB Skill Collections"`.

AgenticScienceBuilder (`README.md` at the repository root):

```html
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/brand/asb-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/assets/brand/asb-logo.svg">
    <img alt="AgenticScienceBuilder" src="docs/assets/brand/asb-logo.svg" width="320">
  </picture>
</p>
```

Keep `width` between 320 and 480 for a README header.
