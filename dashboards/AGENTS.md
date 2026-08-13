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
| `lab.yaml` | ✅ polished — 2026-08-13 | Lab-wide monitoring. Entry stub only; header explains why it is not a jack-sparrow view and why it deliberately has **no** `button_card_templates:` block. |
| `lab/views/01-uptime.yaml` | ✅ polished — 2026-08-13 | Uptime Kuma availability board. **Names no monitor anywhere** — every card is an `auto-entities` Jinja template over `integration_entities('uptime_kuma')`, so the page tracks Kuma with no edits. Core cards + mushroom, so no `[[[ ]]]` and no bracket counting. |
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
- **A card in a `sections` view defaults to HALF the section's 12-column grid.**
  Without `grid_options: {columns: full, rows: auto}` a nested 2-up grid renders
  at a quarter width each and leaves the right half of the section empty — it
  reads as "auto-entities matched nothing" when it actually matched fine. Every
  card in `jack-sparrow/views/` carries that pair for this reason.
- **Markdown with a table needs a literal block (`|`), not folded (`>-`).**
  Folding joins consecutive lines with spaces, so a table collapses into
  `| | | |---|---| | Drives seen | 7 |`. Blank lines survive folding, so
  headings and paragraphs still look right and only the table gives it away.
- **This instance uses US customary units, so HA converts temperatures before a
  template ever reads them.** A source sensor that is natively °C arrives as
  `114.8` with `unit_of_measurement: °F`. Declaring `°C` on a derived sensor
  tells HA the value is Celsius and it converts a *second* time — 46 °C became
  239 °F on a card, which is believable enough to ship. Read the real unit in
  Developer Tools → States before declaring one, and remember the unit, the
  dashboard thresholds and any automation thresholds have to move together.
- **Check the unit on duration sensors too.** `power_on_time` carries
  `unit_of_measurement: d` — dividing it by 24 to "convert hours to days"
  turned 354 days into 15 and made a healthy refurb drive look like it had had
  its SMART counters reset.

## Before marking a file polished

1. `yamllint <file>` is clean.
2. Every non-obvious construct has a comment saying *why*.
3. Referenced entities actually exist on the instance (or the absence is
   explained, as with gitignored HACS assets).
4. Update the table above.
