# Variables

Common variables and configurations for card templates.

## Available Variables

### Discovery

- `anchor` - anchor of the current URL

### Responsiveness

- `is_mobile` - if we're on mobile or not

## Usage Example

```yaml
type: custom:button-card
template:
    - responsive_variables
    - discovery_variables

  styles:
    custom_fields:
      item1:
        - margin-bottom: '[[[ if (variables.is_mobile) return "20px" ]]]'

```

## Notes

- Use `variables.` to access variables.
- Variables can be overridden in individual cards
