# High-Fidelity Mockup Descriptions (Nova Design System)

## Theme: Nova Dark
The Nova Design System uses a deep space palette with high-vibrancy accent colors.

### 1. Global Background
- **Token**: `nova-surface-background`
- **Value**: `#0B0E14` (Deep Charcoal)
- **Texture**: Subtle noise overlay to reduce banding and add depth.

### 2. Activity Cards
- **Token**: `nova-surface-card`
- **Value**: `#161B22` (Slightly lighter than background)
- **Border**: `1px solid nova-border-subtle` (`#30363D`)
- **Corner Radius**: `8px`
- **Shadow**: `nova-shadow-md` (Soft deep glow)

### 3. Typography
- **Headings**: `nova-font-sans`, Medium weight, `nova-text-primary` (`#F0F6FC`).
- **Code**: `nova-font-mono`, `13px`, `nova-text-code` (Syntax highlighting follows Nova-Dark-Vivid theme).
- **Metadata**: `nova-font-sans`, Small, `nova-text-secondary` (`#8B949E`).

### 4. Interactive Elements (Nova Accents)
- **Primary Action (Proceed)**: `nova-color-accent-blue` (`#58A6FF`) with glassmorphism hover effect.
- **Warning Action (Pause)**: `nova-color-accent-gold` (`#D29922`).
- **Danger Action (Cancel)**: `nova-color-accent-red` (`#F85149`).

### 5. Code Visualization
- **Diff Additions**: Background: `rgba(46, 160, 67, 0.15)`, Text: `#3FB950`.
- **Diff Deletions**: Background: `rgba(248, 81, 73, 0.15)`, Text: `#F85149`.
- **Syntax Highlighting**: Deep blues, vibrant purples, and neon cyans for a "cybernetic" feel.

### 6. Feedback Input
- **State: Focused**: Border color changes to `nova-color-accent-blue`, subtle inner glow.
- **Placeholder**: `nova-text-disabled` (`#484F58`).

## Component states in Nova System
- **Hover**: 5% white overlay to indicate depth change.
- **Active**: 10% black overlay + subtle scale down (`0.98x`).
- **Disabled**: 50% opacity, `cursor: not-allowed`.
