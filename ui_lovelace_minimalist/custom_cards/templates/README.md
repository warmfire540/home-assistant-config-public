# Templates

This folder contains reusable card templates for Home Assistant, organized into style definitions and common variables.

## Structure

```
templates/
├── README.md
├── styles/
│   ├── README.md
│   ├── ...
└── variables/
    ├── README.md
    └── ...
```

## Overview

The templates are split into two main categories:

### 🎨 Styles

Located in [`styles/`](styles/), these templates handle visual aspects like:

- Color schemes
- Typography
- Spacing
- Card layouts
- Animations

See the [styles README](styles/README.md) for detailed usage.

### 🔧 Variables

Located in [`variables/`](variables/), these templates contain common values like:

- Entity references
- State mappings
- Icon definitions
- Reusable conditions

See the [variables README](variables/README.md) for implementation details.

## Usage

Import templates in your Lovelace cards using the following syntax:

```yaml
---
my_card:
  template:
    - discovery_variables
    - grid_two_columns
    - no_click
```

## Tips

- Styles can be combined and overridden
- Use the provided templates to maintain consistent look and behavior across cards
- Check individual README files in each subfolder for specific implementation examples
