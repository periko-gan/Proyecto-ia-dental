# Design System Specification: Dark Mode Technical & Aesthetic Guidelines

## 1. Overview & Creative North Star: "The Clinical Nocturne"

The objective of this design system is to translate medical precision into a high-end, dark-mode environment. We are
moving away from the "standard dashboard" aesthetic toward **The Clinical Nocturne**. This North Star defines a
workspace that feels like a high-tech surgical suite: silent, focused, and impeccably organized.

To achieve this, we reject "flat" design in favor of **Tonal Depth**. We break the rigid, boxed-in layout of traditional
medical software by using intentional asymmetry and "Floating Data Architecture." Instead of containment, we use
breathing room; instead of borders, we use light.

## 2. Colors & Surface Philosophy

The palette is rooted in deep obsidian tones with a clinical blue "pulse."

### The "No-Line" Rule

**Explicit Instruction:** Designers are prohibited from using 1px solid borders to section content. Boundaries must be
defined through background color shifts or subtle tonal transitions.

- Use `surface-container-low` for secondary content sitting on a `surface` background.
- Use `surface-container-high` to draw the eye to interactive modules.

### Surface Hierarchy & Nesting

Treat the UI as a series of physical layers—like stacked sheets of surgical grade glass.

* **Base:** `surface` (#121416)
* **Secondary Layer:** `surface-container-low` (#1a1c1e)
* **Interactive/Elevated Layer:** `surface-container-high` (#282a2c)
* **Active/Modal Layer:** `surface-container-highest` (#333537)

### The "Glass & Gradient" Rule

To avoid a "flat" digital feel, floating elements (modals, dropdowns) should utilize **Glassmorphism**.

- **Recipe:** Apply `surface-variant` at 60% opacity with a `backdrop-blur` of 12px.
- **Signature Texture:** Primary CTAs should not be flat. Use a subtle linear gradient from `primary` (#a7c8ff) to
  `primary-container` (#0059a8) at a 135-degree angle to provide a "lit-from-within" clinical glow.

## 3. Typography: The Manrope Scale

Manrope was chosen for its geometric precision and modern terminal cuts, reflecting surgical accuracy.

| Level        | Token         | Size      | Weight | Intent                                            |
|:-------------|:--------------|:----------|:-------|:--------------------------------------------------|
| **Display**  | `display-lg`  | 3.5rem    | 700    | Impactful data visualizations or hero stats.      |
| **Headline** | `headline-md` | 1.75rem   | 600    | Section entry points; authoritative and clear.    |
| **Title**    | `title-sm`    | 1rem      | 500    | Component headers and card titles.                |
| **Body**     | `body-md`     | 0.875rem  | 400    | Standard clinical notes and patient data.         |
| **Label**    | `label-sm`    | 0.6875rem | 600    | All-caps metadata; high-contrast "Surgical" tags. |

**Editorial Note:** Use `display-lg` sparingly to create "Visual Anchors" in an otherwise dense data environment.

## 4. Elevation & Depth

In a dark clinical interface, shadows must be felt, not seen.

* **The Layering Principle:** Achieve hierarchy by "stacking." A `surface-container-lowest` card placed on a
  `surface-container-low` section creates a natural "recessed" look without a single pixel of stroke.
* **Ambient Shadows:** For floating elements, use a shadow with a 40px blur and 6% opacity. The shadow color must be
  derived from `on-surface` (#e2e2e5) to simulate real-world light refraction.
* **The "Ghost Border":** If a boundary is required for accessibility, use the `outline-variant` (#424752) at **15%
  opacity**. Never use 100% opaque borders.
* **Surgical Glow:** Use a 1px inner-glow (box-shadow inset) on primary buttons using `primary-fixed-dim` at 20% opacity
  to simulate a chamfered edge.

## 5. Components

### Buttons

* **Primary:** Gradient fill (`primary` to `primary-container`). Roundedness: `md` (0.375rem).
* **Secondary:** No fill. `Ghost Border` (15% opacity `outline`). Text color: `primary`.
* **Tertiary:** Text only. Use `label-md` for a technical, precise feel.

### Input Fields

* **Visual State:** Use `surface-container-highest` for the background.
* **Active State:** No thick border. Instead, use a 2px bottom-bar in `primary` (#a7c8ff).
* **Error State:** Background shifts to a subtle `error_container` (#93000a) wash at 10% opacity.

### Cards & Lists

* **Constraint:** Forbid divider lines.
* **Separation:** Use `spacing-8` (2rem) of vertical white space or a subtle shift from `surface-container-low` to
  `surface-container-high`.
* **Interactive Hover:** On hover, a card should shift from its base color to `surface-bright` (#38393c) with a
  transition speed of 200ms.

### Diagnostic Tooltips

* **Style:** Dark `inverse-surface` (#e2e2e5) with `inverse-on-surface` (#2f3033) text.
* **Corner:** Use `sm` (0.125rem) for a sharp, surgical precision.

## 6. Do’s and Don’ts

### Do

* **DO** use `primary-fixed-dim` for icons to ensure they don't "vibrate" against deep backgrounds.
* **DO** use `surface-container-lowest` for deep background areas to create a sense of "infinite" space.
* **DO** treat patient data as editorial content: use high-contrast typography scales to emphasize critical vitals.

### Don’t

* **DON'T** use pure black (#000000). It kills the "Medical Glass" depth. Stick to `surface` (#121416).
* **DON'T** use standard 1px dividers. If you feel the need for a line, increase your spacing scale by two increments
  instead.
* **DON'T** use high-saturation reds for errors. Use the provided `error` (#ffb4ab) which is tuned for eye comfort in
  dark environments.