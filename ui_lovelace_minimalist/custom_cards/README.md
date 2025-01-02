# Custom Button Cards

Collection of custom [button-card](https://github.com/custom-cards/button-card) configurations for UI Lovelace Minimalist theme.

## Structure

```
custom_cards/
├── templates/          # Reusable templates for styling and variables
├── README.md
```

## Card Types

### Room Cards

- Living Room Overview
- Kitchen Dashboard
- Bedroom Controls
- Office Workspace

### Entity Cards

- Smart Light Controls
- Climate Controller
- Media Player
- Security Camera Feed

### Chips

- Quick Actions
- Status Indicators
- Weather Info
- System Status

## Usage

Import cards in your dashboard configuration:

```yaml
views:
  - title: Home
    cards:
      - type: custom:button-card
        template: room_header
        variables:
          light_entity: light.living_room
```

## Templates

Common templates are available in the `templates/` directory:

- Style definitions
- Variable collections
- State mappings
- Animation configurations

## Resources

- [Button Card Documentation](https://github.com/custom-cards/button-card/blob/master/README.md)
- [UI Minimalist Custom Cards Guide](https://ui-lovelace-minimalist.github.io/UI/custom_cards)
- [Home Assistant Frontend Guidelines](https://developers.home-assistant.io/docs/frontend/custom-ui/custom-card/)
