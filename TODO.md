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
- [x] ~~**Portainer** (core integration, no HACS) — Docker on jack-sparrow~~
      Added 2026-08-13, the same day the container was deployed. HA config is
      written: `entities/templates/portainer.yaml`,
      `dashboards/jack-sparrow/views/05-containers.yaml`. Board is at
      **`/jack-sparrow/containers`**. No automations — see the reasoning below.
  - [ ] ⚠️ **Verify the entity-ID suffixes.** Everything in both files is
        derived from the integration's `strings.json` translation keys, not
        from the live instance. Run this in Developer Tools → Template and
        check the sibling suffixes against what the sensors are actually
        called:

        ```jinja
        {{ integration_entities('portainer') | sort | list }}
        ```

        A suffix regex that matches nothing does not error — `sensor.docker_health`
        reads OK forever. This is the same failure mode flagged on
        `scrutiny.yaml` and it is worth ten minutes now.
  - [ ] Confirm Portainer surfaces the three UGOS projects as **stacks**. The
        Stacks card is `show_empty: false`, so if UGOS labels its projects in
        a way Portainer does not read as a stack, the card is simply absent
        and nothing tells you which it was.
  - [ ] Decide on a "container down" automation **after** watching the board
        for a week. Deliberately not written yet: Uptime Kuma already alerts
        on all three of these services from outside, so a naive container-down
        automation double-notifies for every real outage. The two shapes worth
        having are the ones Kuma structurally cannot see —
        `sensor.docker_health` attribute `restarting` being non-`none` for
        more than a few minutes (a crash loop rebinds its port often enough
        that a Kuma check passes on the retry), and `container_count`
        *dropping* (a removed container has no status left to be down).
  - [ ] Known upstream bug, [core#160907](https://github.com/home-assistant/core/issues/160907),
        **closed as not planned**: stopping a container from HA returns an
        error even though the stop succeeds, and a container already stopped
        when HA started cannot be started from HA at all. Documented in the
        Controls section header. Re-check on each HA release.
- [x] ~~**Uptime Kuma** (core integration, no HACS) — lab-wide availability~~
      Added 2026-08-13. 16 monitors / 178 entities. HA config is written and
      live: `entities/templates/uptime_kuma.yaml`, `dashboards/lab.yaml` +
      `dashboards/lab/views/01-uptime.yaml`,
      `automations/lab/uptime_kuma_monitor_down.yaml`. Deploy steps live in
      the **servers** repo at `hosts/jack-sparrow/uptime-kuma-runbook.md`.
  - [ ] Set up the Kuma-native ntfy channel (runbook Part 3) and attach it to
        exactly `Internet`, `Gateway`, `homeassistant`. Until then those three
        outages are **unalerted** — HA cannot notify you that HA is down, and
        the down automation deliberately skips them.
  - [x] ~~Recovery notification~~ — an **all-clear** branch in the same
        automation, firing once when `down_count` returns to zero, on the same
        notification tag so the green message replaces the red one. Dormant
        until Portainer / lil-bit / poat-seedbox are up.
  - [ ] Board is at **`/home-lab/uptime`**, not `/lab/uptime` — HA requires a
        hyphen in a YAML dashboard's URL path and rejects the whole config
        without one. Source files still live under `dashboards/lab/`.
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
