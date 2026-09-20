# Prose type

## Goal

Chat prose should be readable at a glance: body 16px, comfortable line-height, headings one step up, wrapping code.

## Properties

- **T1** Body font-size is `16px` (not `rem`, not `0.875rem`).
- **T2** Body line-height is `1.5`.
- **T3** Headings: h1 `22px`, h2 `18px`, h3 `16px`.
- **T4** Fenced code uses `white-space: pre-wrap`.
- **T5** Paragraph `margin-bottom` is `0.5em` or less.
- **T6** Adjacent block gap is `0.65em` or less.

## Tokens

See `tokens.json`. Implement these values in whatever CSS/theme system the harness has.

## Not in scope

- Cloning another product’s color palette, serif, or chrome
- Shipping a patched `dist/webview.js` as “the module”

## Adapter job

Map `tokens.json` onto the harness markdown surface. The Kilo reference is `adapters/kilo/kilo-claude-markdown.css`.
