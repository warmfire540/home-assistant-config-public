# Headers

Collection of reusable layout templates for card headers.

```yaml
title: 'Cats'
path: 'cats'
subview: true
cards:
  - type: custom:button-card
    template: mainview_header
```

```yaml
title: 'T1D'
path: 't1d'
subview: true
cards:
  - type: custom:button-card
    template: subview_header
    variables:
      image: /local/img/medtronic.png
      image_nav: https://www.diabetes.shop/homepage
```