# Design System Strategy: The Clinical Precision Framework

## 1. Overview & Creative North Star: "The Digital Surgeon"

This design system moves away from the "friendly startup" aesthetic of rounded bubbles and flat primary colors. Our
Creative North Star is **The Digital Surgeon**: a visual language that feels as precise, sterilized, and high-tech as a
modern operatory.

To break the "template" look, we employ **Intentional Asymmetry**. Instead of centered, balanced grids, we use weighted
sidebars and overlapping "X-ray" layers. By pairing the technical rigor of `Inter` with the high-end editorial feel of
`Manrope`, we establish a hierarchy that feels both authoritative and cutting-edge. We reject the "boxed-in" web; we
embrace an interface that feels like a fluid, heads-up display (HUD).

---

## 2. Colors: Tonal Depth & The "No-Line" Rule

The palette is rooted in `Clinical Blue` and `Tech Cyan`, but its sophistication comes from how we layer these tones.

### The "No-Line" Rule

**Explicit Instruction:** Do not use `1px solid` borders to define sections. Traditional borders create visual noise
that feels dated. Instead, boundaries must be defined by:

- **Tonal Shifts:** Placing a `surface-container-low` component on a `surface` background.
- **Negative Space:** Using the `12` (3rem) or `16` (4rem) spacing tokens to create mental boundaries.

### Surface Hierarchy & Nesting

Treat the UI as a series of physical layers—stacked sheets of medical-grade frosted glass.

- **Base:** `surface` (#f8f9fa)
- **Primary Layout Blocks:** `surface-container-low` (#f3f4f5)
- **Interactive Cards:** `surface-container-lowest` (#ffffff) for a "lifted" feel.
- **Overlays/Modals:** `surface-bright` with 80% opacity and a `20px` backdrop-blur.

### The "Glass & Gradient" Rule

To signal "AI Scanning," use `Tech Cyan` gradients. A linear gradient from `secondary` (#006877) to
`secondary-container` (#75e7fe) at a 45-degree angle should be reserved for high-intent AI elements, like scan progress
bars or diagnosis highlights. This adds "visual soul" that flat HEX codes cannot provide.

---

## 3. Typography: The Editorial Scale

We use a dual-typeface system to balance clinical data with high-end brand authority.

* **Display & Headlines (Manrope):** This is our "Editorial Voice." `display-lg` (3.5rem) should be used sparingly for
  hero statements, creating a high-contrast shift against the dense data of a dental app.
* **Interface & Data (Inter):** All functional elements (labels, body, titles) use `Inter`. This typeface is engineered
  for legibility at small sizes, crucial for reading dental charts and AI confidence scores.
* **Intentional Contrast:** Pair a `headline-sm` (Manrope, 1.5rem) with a `label-sm` (Inter, 0.6875rem) in all caps with
  `0.05em` letter spacing to create a "technical manual" aesthetic.

---

## 4. Elevation & Depth: Tonal Layering

We do not use shadows to represent "importance"; we use them to represent "float."

* **The Layering Principle:** Depth is achieved by stacking. A `surface-container-lowest` card sitting on a
  `surface-container-high` background provides a natural, soft lift.
* **Ambient Shadows:** For floating AI modules, use a custom shadow: `0 20px 40px rgba(0, 86, 179, 0.06)`. Note the use
  of `primary` color in the shadow—this mimics natural light refracting through blue-tinted medical glass rather than a
  dead grey shadow.
* **The "Ghost Border" Fallback:** If a container needs a hard edge (e.g., a high-density data table), use a
  `Ghost Border`. This is the `outline-variant` token at **15% opacity**. It should be felt, not seen.
* **Glassmorphism:** AI insight panels must use `backdrop-filter: blur(12px)` over a semi-transparent
  `surface-container-lowest`. This ensures the user never loses context of the dental scan beneath the data.

---

## 5. Components: Precision Primitives

### Buttons: The "Tactile Command"

- **Primary:** Background `primary` (#003f87), `on-primary` text. Use `rounded-md` (0.375rem). The hover state is not a
  color change, but a slight expansion of the ambient blue shadow.
- **Secondary (AI Action):** Background `secondary-container`, text `on-secondary-container`. Use this for "Run AI
  Analysis" to distinguish from "Save/Submit."

### Input Fields: The "Technical Entry"

- **Style:** No bottom border or full box. Use a subtle `surface-container-high` background with `rounded-sm`. On focus,
  transition the background to `surface-container-lowest` and add a `2px` `secondary` left-accent bar.

### Cards & Lists: The "Fluid Flow"

- **Rule:** **Strictly forbid horizontal divider lines.**
- Separate patient records or tooth data using `spacing-4` (1rem) and subtle alternating background shifts (Zebra
  striping using `surface` and `surface-container-low`). This keeps the interface "breathable."

### AI Scanning Chips

- **Interactive:** Use `rounded-full` with a `secondary` (Tech Cyan) glow. When an AI scan is "Active," the chip should
  pulse with a `4px` blur of the `secondary` color.

---

## 6. Do's and Don'ts

### Do:

- **Use Vertical Rhythm:** Stick strictly to the `4` (1rem) and `8` (2rem) spacing tokens for all margins.
- **Embrace White Space:** Allow the "Clinical Blue" to breathe. A high-density dental app needs "visual silence" to
  prevent user fatigue.
- **Subtle Motion:** AI elements should fade in with a `200ms` ease-out; they shouldn't just "pop" into existence.

### Don't:

- **Don't use 100% Black:** Use `on-surface` (#191c1d) for text. Pure black is too harsh for a medical context.
- **Don't use "Default" Shadows:** Avoid the standard Tailwind `shadow-lg`. Use our Ambient Shadow spec for a premium,
  custom feel.
- **Don't Over-round:** Never use `rounded-xl` or `full` for main containers. It looks too "consumer-tech." Stick to
  `md` (0.375rem) for a professional, engineered look.
- **No Divider Clutter:** If you feel the need to add a line, add `16px` of space instead. 