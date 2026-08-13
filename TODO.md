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
- [ ] **Uptime Kuma push monitors for backup freshness** — the mechanism for
      the two items above now exists but is not wired up. A push monitor
      detects a thing that *didn't happen*, which is the shape of "the nightly
      backup silently stopped running three weeks ago"; a last-backup sensor
      only tells you the date if something is still writing one. Deferred by
      decision on 2026-08-13 until the backup pass itself happens, since the
      job set is about to change. Mechanism and the exact `curl` line are in
      §2.4 of the servers repo's `hosts/jack-sparrow/uptime-kuma-runbook.md`.
      The `Backups` group already exists in Kuma, paused and empty.

## Config reconciliation

- [ ] Go through pending README / HAS checklist items and close or update what’s stale
- [ ] Find unused or rarely used entities, automations, scripts, and dashboard bits
- [ ] Remove or archive what’s no longer needed; keep what’s still useful lean

## Logs

- [ ] Review Home Assistant warnings / errors in the system log
- [ ] Fix root causes (or silence true noise) so the log stays clean

## Integrations

- [ ] EcoFlow (BLE or Cloud... need to decide)
- [x] ~~**Uptime Kuma** (core integration, no HACS) — lab-wide availability~~
      Added 2026-08-13. 16 monitors / 178 entities. HA config is written and
      live: `entities/templates/uptime_kuma.yaml`, `dashboards/lab.yaml` +
      `dashboards/lab/views/01-uptime.yaml`,
      `automations/lab/uptime_kuma_monitor_down.yaml`. Deploy steps live in
      the **servers** repo at `hosts/jack-sparrow/uptime-kuma-runbook.md`.
  - [x] ~~Set up the Kuma-native channel (runbook Part 3)~~ — Discord, created
        and tested 2026-08-13, attached to `Internet`, `Gateway`,
        `homeassistant`. Those are the three HA cannot report on. Note this
        works *without* any exclusion in the automation: the first two are
        caught by the WAN gate and the third cannot notify at all. Adding a
        fourth monitor to Discord would double-notify — `poat-hole - DNS` was
        tried and reverted for exactly that reason (runbook §3.4).
  - [ ] Decide whether a recovery ("back up") notification is wanted. Only the
        down alert exists today, so a resolved outage is silent.
  - [ ] Tag monitors in Kuma (runbook §4.5) if the rollup should ever cover a
        subset rather than everything.
  - [ ] Remove the stale HA device left behind by the paused `Backups` group —
        the API does not expose paused monitors, so HA cannot tell paused from
        deleted and will not clean it up itself.

## Legacy ping monitoring — decide what Uptime Kuma replaces

Kuma now checks these hosts from outside Home Assistant, which is strictly
better: a `binary_sensor.*_local` ping sensor cannot tell you HA itself is
down, and it answers "does the host reply to ICMP" rather than "is the service
working". `poat-hole - DNS` is the clearest example — the Pi can ping fine
while resolving nothing.

**Not a mechanical swap.** The legacy sensors are used as *conditions* on the
Lab view, and at least one pair is not equivalent:

| Legacy | Kuma monitor | Same thing? |
| --- | --- | --- |
| `binary_sensor.poat_hole_local` | `poat-hole - DNS` / `poat-hole - admin` | Kuma is better — checks resolution, not ICMP |
| `binary_sensor.poat_share_local` | `poat-share - SMB (IP)` + `(name)` | Kuma is better — checks the port and the name chain |
| `binary_sensor.poat_seedbox_local` | `poat-seedbox - Deluge` | Kuma checks the daemon RPC port, not the host |
| `binary_sensor.poat_plex_local` | `lil-bit - Plex` | ⚠️ **probably different hosts** — confirm before swapping |

- [ ] Confirm whether `poat-plex` and `lil-bit` are the same machine. The Lab
      view still points `custom:plex-meets-homeassistant` at `poat-plex.local`
      while Kuma monitors `192.168.4.161`.
- [ ] Then swap the conditions in
      `ui_lovelace_minimalist/dashboard/views/mainviews/lab.yaml` and
      `.../card_declutter/pi_details.yaml` from `binary_sensor.*_local` `on`
      to the matching `sensor.*_status` `up`.
- [ ] Then retire `automations/sensors/ping_interval.yaml` and the ping config
      entries. That automation only exists to work around
      home-assistant/core#105041 (ping sensors not honouring an update
      interval); Kuma polls on its own schedule, so the workaround goes with
      the sensors.
- [ ] Keep whatever still has no Kuma equivalent rather than deleting for
      symmetry.
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
