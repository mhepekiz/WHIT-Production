# WHIT UI Theme

This project features a modern light theme with vibrant green accents, providing a clean, professional appearance perfect for a tech job board application.

## Color Palette

### Primary Colors
- **Primary Green** (`#00c853`): Primary action color, used for buttons, links, and accents
- **Primary Green Light** (`#69f0ae`): Hover states and highlights
- **Primary Green Dark** (`#00a843`): Active states and borders

### Secondary Colors
- **Orange** (`#ff6b35`): Secondary accent for errors and warnings
- **Accent Blue** (`#0099ff`): Tertiary accent for special highlights

### Light Theme Base
- **Light Background** (`#f8f9fa`): Main page background
- **Surface** (`#ffffff`): Card and container backgrounds
- **Light Gray** (`#e9ecef`): Borders and dividers
- **Gray** (`#dee2e6`): Hover states

### Text Colors
- **Primary Text** (`#212529`): Main text color
- **Secondary Text** (`#495057`): Subtitles and labels
- **Muted Text** (`#6c757d`): Placeholder text

## Design Features

### Modern Light Theme
- Clean, professional light interface
- Excellent readability and contrast
- Comfortable for extended viewing

### Vibrant Green Accents
- Vibrant green highlights for primary actions
- Gradient effects on buttons and interactive elements
- Green border accents on focus states

### Interactive Elements
- Smooth transitions and hover effects
- Elevated shadows on hover
- Transform animations for better UX feedback

### Typography
- System font stack for optimal performance
- Uppercase labels with letter-spacing for clarity
- Font weight hierarchy for content organization

## Component Styling

### Buttons
```css
/* Primary Button */
background: linear-gradient(135deg, #00c853 0%, #00a843 100%);
box-shadow: 0 6px 16px rgba(0, 200, 83, 0.4); /* on hover */

/* Secondary Button */
border: 2px solid #00c853;
color: #00c853;
```

### Input Fields
```css
background: var(--splunk-gray-dark);
border: 2px solid var(--border-color);
/* Focus state adds green border and glow */
```

### Tables
```css
/* Header */
background: var(--splunk-gray-dark);
border-bottom: 2px solid var(--splunk-primary);

/* Rows hover with elevation effect */
```

### Cards
```css
background: var(--surface);
border: 1px solid var(--border-color);
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
```

## CSS Variables

All colors are defined as CSS custom properties in `/frontend/src/styles/splunk-theme.css` (note: file will be renamed):

```css
:root {
  --splunk-primary: #00c853;
  --splunk-secondary: #ff6b35;
  --background: #0f1419;
  --surface: #1a2332;
  --text-primary: #ffffff;
  /* ... and more */
}
```

## Usage

The theme is automatically applied through the import in `App.css`:

```css
@import './styles/splunk-theme.css';
```

### Custom Components

To use the theme colors in your components:

```css
.my-component {
  background: var(--surface);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.my-button {
  background: var(--gradient-primary);
}
```

### Utility Classes

Available utility classes from `splunk-theme.css`:

```css
.text-primary     /* White text */
.text-secondary   /* Gray text */
.text-accent      /* Green text */
.bg-surface       /* Dark card background */
.shadow           /* Standard shadow */
.shadow-lg        /* Large shadow */
```

## Customization

To customize the theme:

1. Open `/frontend/src/styles/splunk-theme.css`
2. Modify the CSS custom properties in `:root`
3. Changes will apply globally across all components

### Example: Change Primary Color

```css
:root {
  --splunk-primary: #ff6b35; /* Change from green to orange */
  --gradient-primary: linear-gradient(135deg, #ff6b35 0%, #ff8552 100%);
}
```

## Responsive Design

The theme includes responsive breakpoints:

```css
@media (max-width: 768px) {
  /* Mobile-friendly adjustments */
}
```

## Accessibility

- High contrast ratios for WCAG compliance
- Focus states clearly visible with green outlines
- Consistent spacing and sizing for touch targets

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- CSS Custom Properties support required
- Fallbacks provided for older browsers where needed

---

**Note**: This theme provides a modern, professional appearance with vibrant green accents, optimized for a tech job board application that conveys professionalism and reliability.
