# Home Assistant cleanup

Working notes for streamlining dashboards, entities, backups, and log noise.

## Dashboards

- [ ] Polish and reconcile `lab.yaml` (start here)
- [ ] Walk other mainviews / subviews and clean up unused or low-value cards
- [ ] Streamline layouts so status, controls, and alerts are easier to scan
- [ ] Surface backup status more clearly on Lab / related views

## Backups

- [ ] Confirm every important service has a last-backup sensor
- [ ] Add alerts (and supporting entities) when backups go stale or missing
- [ ] Make backup health visible on the dashboard, not just buried in entity lists

## Config reconciliation

- [ ] Go through pending README / HAS checklist items and close or update what’s stale
- [ ] Find unused or rarely used entities, automations, scripts, and dashboard bits
- [ ] Remove or archive what’s no longer needed; keep what’s still useful lean

## Logs

- [ ] Review Home Assistant warnings / errors in the system log
- [ ] Fix root causes (or silence true noise) so the log stays clean

## Integrations

- [ ] EcoFlow (BLE or Cloud... need to decide)
- [ ] **Scrutiny** (`vitals5/ha_scrutiny`, HACS default catalog) — drive SMART
      health from jack-sparrow. Config written and waiting on the Scrutiny
      container: `entities/templates/scrutiny.yaml`,
      `dashboards/jack-sparrow/views/04-drives.yaml`,
      `automations/lab/scrutiny_*.yaml`. Deploy steps live in the **servers**
      repo at `hosts/jack-sparrow/scrutiny-runbook.md`.
  - [ ] Verify the `realloc.*_raw` / `pending.*_raw` regexes in
        `entities/templates/scrutiny.yaml` against real entity IDs. A regex
        matching nothing reads 0 forever instead of erroring.
  - [ ] Turn on **Critical SMART attribute sensors** + **Enable raw value
        sensors** in the integration options, or the sector totals stay empty.

## Notes

- Existing backup sensors live in `entities/command_line/sensors/pi_backups.yaml` (HA, Pi-hole, Deluge, Plex).
- Lab view: `ui_lovelace_minimalist/dashboard/views/mainviews/lab.yaml`
