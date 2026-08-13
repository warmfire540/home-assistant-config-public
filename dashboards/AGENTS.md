# dashboards/ — agent notes

Standalone YAML dashboards registered in [integrations/lovelace.yaml](../integrations/lovelace.yaml).
These live outside `ui_lovelace_minimalist/` on purpose: anything needing its own
`button_card_templates:` block cannot use UML's template dir, which is
HACS-managed and overwritten on update.

## Polish status

Files marked polished have been read end-to-end, linted, and carry comments
explaining anything non-obvious. Treat them as reference for style.

| File | Status | Notes |
| --- | --- | --- |
| `jack-sparrow.yaml` | ✅ polished — 2026-08-13 | UGREEN NASync DXP4800 Pro. Entry stub only; header comment explains the split, the button-card wrapper pattern, the two `selected_slug` fallbacks, and why the anchors live in the view file. |
| `jack-sparrow/templates/*.yaml` | ✅ polished — 2026-08-13 | One `button_card_template` per file, merged by `!include_dir_merge_named`. |
| `jack-sparrow/views/*.yaml` | ✅ polished — 2026-08-13 | One view per file, ordered by the `NN-` prefix. |
| `jack-sparrow/views/04-drives.yaml` | ✅ polished — 2026-08-13 | Scrutiny SMART health per disk. **The one view with no `ugreen_tpl_host` wrapper** — nothing on it is keyed to the NAS selector, so `auto-entities` sits at view level and its `options:` templates use THREE brackets, not four. |
| `room-summary-card/*.yaml` | ⬜ not reviewed | Scratch dashboards for testing the custom card. Hidden from sidebar. Candidates for pruning. |

## Splitting a dashboard

Past ~400 lines, split it the way `the-matrix` and `jack-sparrow` are:

```
foo.yaml                 entry stub — title, theme, includes only
foo/templates/*.yaml     one button_card_template per file
foo/views/NN-*.yaml      one view per file
```

- `button_card_templates: !include_dir_merge_named foo/templates`
- `views: !include_dir_list foo/views` — sorted by filename, hence `NN-`.
- `!include` paths are relative to the *including* file.
- **Keep the entry stub where `lovelace.yaml` already points.** That `filename:`
  key is only read at startup, so moving the entry file costs a Home Assistant
  restart; splitting views out of it only costs a page refresh.

## Conventions

- Start files with `---`.
- Header comment block (`#####`) stating what the dashboard is, why it exists
  where it does, and anything that will bite an editor later.
- Section banners inside `views:` using the wide `####…` rule.
- Prefer theme vars (`var(--primary-text-color)`, `var(--error-color)`) over
  hardcoded colors so both light and dark themes work. Upstream examples often
  hardcode `white`; that is usually worth converting.

## Gotchas that have already cost time

- **`[[[ ... ]]]` JS templates only evaluate inside `custom:button-card`.**
  A `mini-graph-card`, `entities`, or `auto-entities` card that needs a
  templated `entity_id` must be nested under a button-card `custom_fields:`
  wrapper (see the `ugreen_tpl_host` template). Without the wrapper the
  template is passed through as a literal string and the card throws
  "Configuration error". The redundant-looking wrappers are load-bearing.
- **Nesting depth changes the bracket count.** Templates one level deeper
  inside an `auto-entities` `options:` block use `[[[[ ... ]]]]`.
- **Put the wrapper's chrome in the template, not the call site.** The
  single-cell grid belongs in the host template with a fixed `item1` field
  name; naming the field per-card forces the grid block to be repeated at
  every call site for no benefit.
- **YAML anchors do not cross an `!include` boundary.** An `&anchor` and every
  `*alias` that uses it have to end up in the same file. Plan the split around
  the anchors, or hoist the shared value into a `button_card_templates` entry.
- **Integration attribute names drift.** The UGREEN pool/volume/disk summary
  entities expose `Size` / `Used` / `Free`, not `Total Size` / `Used Size` /
  `Available Size`. Reading a name that no longer exists does not error — the
  card renders an em-dash and looks like a dead sensor. Check Developer Tools
  before assuming the integration broke.
- **YAML anchors work for repeated values, templates for repeated cards.**
  Anchors (`&percent_thresholds`) cannot parameterize, so anything varying
  by more than nothing wants a `button_card_templates` entry with
  `variables:` instead.
- **`/local/community/...` assets are gitignored.** They ship with the HACS
  integration and exist on the live instance only. Do not "fix" those paths.
- **`device_id` values are opaque.** The comment above each card is the only
  label; keep them in sync.

## Before marking a file polished

1. `yamllint <file>` is clean.
2. Every non-obvious construct has a comment saying *why*.
3. Referenced entities actually exist on the instance (or the absence is
   explained, as with gitignored HACS assets).
4. Update the table above.
