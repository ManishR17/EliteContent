# EliteContent Frontend Design System

## 🎨 Design Philosophy

**CRITICAL RULE**: When adding new features, you MUST use the existing styles and patterns defined in this document. Do NOT create new CSS classes or styling patterns.

---

## Color Palette

### Primary Colors
```css
--primary-dark: #0a0a0a;        /* Main background */
--primary-black: #000000;        /* Pure black accents */
--primary-white: #ffffff;        /* Text and highlights */
```

### Accent Colors
```css
--accent-purple: #6366f1;        /* Primary CTA buttons */
--accent-purple-dark: #4f46e5;   /* Hover states */
--accent-purple-light: #818cf8;  /* Links and highlights */
```

### Neutral Grays
```css
--gray-100: #f8f9fa;
--gray-200: #e2e8f0;
--gray-300: #cbd5e1;
--gray-400: #94a3b8;
--gray-500: #64748b;
--gray-600: #475569;
--gray-700: #334155;
--gray-800: #1e293b;
--gray-900: #0f172a;
```

### Semantic Colors
```css
--success: #10b981;
--warning: #f59e0b;
--error: #ef4444;
--info: #3b82f6;
```

---

## Typography

### Font Family
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

### Font Sizes
```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
```

### Font Weights
```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

---

## Spacing System

Use these values for margin, padding, gaps:
```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

---

## Component Patterns

### 1. Page Container
```css
.page-container {
  min-height: 100vh;
  background: radial-gradient(circle at top right, #1e1b4b, #000);
  padding: 2rem;
}
```

### 2. Content Card (Glassmorphism)
```css
.content-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}
```

### 3. Form Input
```css
.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #6366f1;
}
```

### 4. Primary Button
```css
.btn-primary {
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  border: none;
  border-radius: 8px;
  color: #fff;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-primary:hover {
  opacity: 0.9;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### 5. Secondary Button
```css
.btn-secondary {
  padding: 0.75rem 1.25rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #fff;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: #fff;
}
```

### 6. Section Header
```css
.section-header {
  font-size: 1.8rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.5rem;
}

.section-subheader {
  font-size: 1rem;
  color: #94a3b8;
  margin-bottom: 2rem;
}
```

### 7. Grid Layout (2-column)
```css
.grid-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

@media (max-width: 768px) {
  .grid-2col {
    grid-template-columns: 1fr;
  }
}
```

### 8. Loading Spinner
```css
.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### 9. Error Message
```css
.error-message {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #ef4444;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
```

### 10. Success Message
```css
.success-message {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  color: #10b981;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
```

---

## Animation Standards

### Fade In
```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.3s ease-out;
}
```

### Slide In
```css
@keyframes slideIn {
  from {
    transform: translateX(-20px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.slide-in {
  animation: slideIn 0.4s ease-out;
}
```

---

## Layout Patterns

### Feature Page Layout
```
┌─────────────────────────────────────┐
│  Page Header (h1 + description)     │
├─────────────────┬───────────────────┤
│                 │                   │
│  Input Form     │  Output Preview   │
│  (Left 50%)     │  (Right 50%)      │
│                 │                   │
└─────────────────┴───────────────────┘
```

### Dashboard Layout
```
┌─────────────────────────────────────┐
│  Dashboard Header                   │
├───────┬───────┬───────┬─────────────┤
│ Stat  │ Stat  │ Stat  │  Stat       │
├───────┴───────┴───────┴─────────────┤
│  Quick Actions Grid                 │
├─────────────────────────────────────┤
│  Recent Activity List               │
└─────────────────────────────────────┘
```

---

## Component Checklist

When adding a new feature component, ensure:

- [ ] Uses `page-container` for the outer wrapper
- [ ] Uses `content-card` for glassmorphism panels
- [ ] Uses `form-input` for all text inputs
- [ ] Uses `btn-primary` or `btn-secondary` for buttons
- [ ] Uses `section-header` and `section-subheader` for titles
- [ ] Uses `grid-2col` for two-column layouts
- [ ] Uses `spinner` for loading states
- [ ] Uses `error-message` or `success-message` for feedback
- [ ] Uses `fade-in` animation for new content
- [ ] Follows the color palette (no custom colors)
- [ ] Uses spacing system values (no arbitrary padding/margin)
- [ ] Uses typography scale (no custom font sizes)

---

## File Structure

```
frontend/src/app/
├── features/
│   ├── [feature-name]/
│   │   ├── [feature-name].component.ts
│   │   ├── [feature-name].component.html
│   │   └── [feature-name].component.css
│   └── ...
├── shared/
│   └── components/
│       ├── navbar/
│       └── preview/
└── core/
    └── services/
```

---

## DO NOT DO

❌ Create new CSS color variables  
❌ Add custom font sizes outside the scale  
❌ Use arbitrary spacing values  
❌ Create new button styles  
❌ Use different border-radius values  
❌ Add new animation patterns  
❌ Break the glassmorphism aesthetic  
❌ Use different background gradients  

---

## DO THIS INSTEAD

✅ Reuse existing CSS classes  
✅ Copy patterns from existing components  
✅ Use the defined color palette  
✅ Follow the spacing system  
✅ Maintain consistent animations  
✅ Keep the dark glassmorphism theme  
✅ Use the typography scale  

---

## Example: Adding a New Feature

### ❌ WRONG WAY
```css
/* DON'T create new custom styles */
.my-new-feature {
  background: #123456;
  padding: 15px;
  border-radius: 5px;
  font-size: 17px;
}
```

### ✅ RIGHT WAY
```css
/* DO use existing patterns */
.my-new-feature {
  /* Reuse content-card pattern */
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 2rem;  /* Use spacing system */
}
```

---

## Quick Reference

**Need a container?** → Use `.page-container`  
**Need a card?** → Use `.content-card`  
**Need a button?** → Use `.btn-primary` or `.btn-secondary`  
**Need an input?** → Use `.form-input`  
**Need spacing?** → Use spacing system values  
**Need a color?** → Use color palette variables  
**Need animation?** → Use `.fade-in` or `.slide-in`  

---

## Enforcement

This design system is **MANDATORY** for all new features. Any PR that introduces custom styling outside this system will be rejected.

**Last Updated**: December 1, 2025
