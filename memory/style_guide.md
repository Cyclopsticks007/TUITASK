# Bagels Style Guide

## Visual Philosophy
"State of the Art", Premium, Cyberpunk/Neon Ledger.
- **Background**: Deep Dark (`#181820`).
- **Text**: Crisp Grey (`#E0E0E0`) with Muted accents (`#9AA0B5`).

## Grid Architecture (New 0.3.2)
- **Columns**: 6-column Grid (`12fr 11fr 23fr 18fr 18fr 18fr`).
- **Structure**:
    - **Left**: A (12fr) + B (11fr) → Accounts & Insights.
    - **Center**: C (23fr) → Calendar (Featured).
    - **Right**: D+E+F (54fr total) → Templates & Records.

## Color Palette (tcss)
- `$bg`: `#181820`
- `$panel-0`: `#181820` (Base)
- `$panel-1`: `#302840` (Highlight)
- `$border`: `#404868` (Standard)
- `$accent-orange`: `#F89860` (Primary Action / Records)
- `$accent-blue`: `#6078B8` (Info / Templates)
- `$accent-purple`: `#BB9AF7` (Active Tabs / Badges)

## Component Standards

### Panels
- **Border**: `round $border` (Default).
- **Colors**: Use specific branded borders for functional areas (Orange for Data/Records, Blue for Templates).
- **Padding**: Standard is `0 1` or `1`.

### Navigation
- **TopNav**: Height 3.
- **Brand**: `-> Bagels` icon style.
- **Tabs**: Transparent inactive, Purple background active.

### Typography
- **Headers**: Bold, `$text-muted` or `$text`.
- **Numbers**: Monospaced or aligned for data.

### Buttons
- **Primary**: No background, Border colored? Or `$panel-0` with colored border.
- **Flat**: Transparent background, textual interaction.
