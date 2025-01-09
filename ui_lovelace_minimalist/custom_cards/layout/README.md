# Layouts

This folder contains reusable card templates for Home Assistant, organized into header definitions.

## Structure

```
layout/
├── README.md
├── headers/
│   ├── README.md
│   ├── ...
```

## Overview

The templates are split into one main category:

### 🎨 headers

Located in [`headers/`](headers/), these templates handle layouts for the headers for views:

- Common Careds
- Status Chips

See the [headers README](headers/README.md) for detailed usage.

## Usage

Import layouts in your Lovelace cards using the following syntax:

```yaml
title: 'Cats'
path: 'cats'
subview: true
cards:
  - type: custom:button-card
    template: mainview_header
```

## Tips

- Header layouts should usually be placed at the top via grid templates
- Use the provided templates to maintain consistent look and behavior across cards
- Check individual README files in each subfolder for specific implementation examples
