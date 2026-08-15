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
| `scrutiny.yaml` | ✅ polished — 2026-08-13 | Per-drive SMART rollups from ha_scrutiny: health, hottest drive, reallocated-sector total. Entity list derived via `integration_entities('scrutiny')` + `expand()`, so an RMA'd drive needs no edit. **The `realloc.*_raw` / `pending.*_raw` regexes are unverified against the live instance** — see the header. |
| `uptime_kuma.yaml` | ✅ polished — 2026-08-13 | `sensor.lab_availability` + `binary_sensor.lab_wan_down` from the core `uptime_kuma` integration. Entity list derived via `integration_entities('uptime_kuma')`. **Group monitors are filtered out** by reading each device's `_monitor_type` sibling — without it every outage double-counts. Verified against the live instance: 16 monitors, 3 groups, 13 leaves. |
| `portainer.yaml` | ⚠️ written, unverified — 2026-08-13 | `sensor.docker_health` + `sensor.docker_image_updates` from the core `portainer` integration. Container list derived via `integration_entities('portainer')` filtered to `^binary_sensor` — the integration's container-only platform, so no group filtering is needed the way `uptime_kuma.yaml` needs it. **Every sibling suffix (`_state`, `_health`, `_cpu_usage_total`, …) is predicted from `strings.json` translation keys and has NOT been checked against the live instance.** A regex matching nothing reads healthy forever. |
| `duplicati.yaml` | ⚠️ written, unverified — 2026-08-15 | `sensor.duplicati_backup_health` rollup from the HACS `hass-duplicati` (txxa/hass-duplicati) integration. Job list derived via `integration_entities('duplicati')` filtered to `^binary_sensor.*_status$`, one job today ("Scrutiny Backup"). **Suffixes are predicted from upstream `const.py`/entity descriptions and have NOT been checked against the live instance.** ⚠️ `binary_sensor.*_status` is `device_class: problem` — on means a problem, off means healthy — opposite of the Scrutiny/Portainer "on = healthy" convention; see the file header. |
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
