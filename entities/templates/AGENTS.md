# entities/templates/ — agent notes

Template sensors and binary sensors, loaded via
`template: !include_dir_merge_list ../entities/templates` in
[integrations/template.yaml](../../integrations/template.yaml).

Because it is `include_dir_merge_list`, **every file must be a YAML list** —
top-level `- sensor:` / `- binary_sensor:`, not a bare mapping.

## Polish status

| File | Status | Notes |
| --- | --- | --- |
| `jack_sparrow.yaml` | ✅ polished — 2026-08-13 | NAS volume-used %, plus a rolled-up health sensor. Watched entities are matched by regex, not hardcoded. |
| `battery_low_devices.yaml` | ⬜ not reviewed | |
| `cat_devices_problems.yaml` | ⬜ not reviewed | |
| `dead_zwave_nodes.yaml` | ⬜ not reviewed | |
| `devices_offline.yaml` | ⬜ not reviewed | |
| `last_scene.yaml` | ⬜ not reviewed | |
| `litter_robots_waste_full.yaml` | ⬜ not reviewed | |
| `pi_statistics.yaml` | ⬜ not reviewed | |
| `power_in_kw.yaml` | ⬜ not reviewed | |
| `printer_left_on.yaml` | ⬜ not reviewed | |
| `seedbox_vpn_on.yaml` | ⬜ not reviewed | |
| `testing.yaml` | ⬜ not reviewed | Scratch file — candidate for removal. |
| `updates_available.yaml` | ⬜ not reviewed | |
| `washy_needs_cleaned.yaml` | ⬜ not reviewed | |

## Conventions

- Start files with `---`, then a `#####` header block saying what the sensors
  are for and, where it matters, why they exist at all (usually: the
  integration does not expose the number you actually want).
- Every sensor gets a stable `unique_id` (UUID) so it stays editable in the UI
  and survives renames.
- Set `unit_of_measurement` + `state_class: measurement` on anything numeric
  you want history/statistics for.
- Guard division with `availability:` rather than letting the state go
  `unknown` — e.g. `total_raw | float(0) > 0`.
- Note downstream consumers (dashboards, automations) in the header so a
  rename does not silently break a card.

## Jinja notes for this repo

- **Use the `search` test, not `match`.** The repo standardizes on `search`
  with an explicit `^...$` when a full match is wanted.
- **`zip` does not exist** in HA's Jinja. To pair two lists, loop with
  `{% set ns = namespace(...) %}` and append — that pattern is used throughout
  this directory.
- **Don't hardcode a list of entities in two places.** If a `state` and an
  attribute both need the same set, derive it by pattern in both, or the two
  will drift. `jack_sparrow.yaml` shows the regex approach.
- **`this` refers to the entity's own state object.** Use it in `icon:` rather
  than `state_attr('sensor.self', ...)`, which deadlocks the template.
- Attributes meant for humans (notifications, more-info dialogs) should render
  as joined strings, not raw list reprs like `['a', 'b']`.

## Before marking a file polished

1. `yamllint <file>` is clean.
2. Templates verified against real entity IDs — check the regex does not catch
   near-misses (e.g. `_temperature` when you meant `_status`).
3. `unique_id` present on every entity.
4. Update the table above.
