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
- [ ] **Healthchecks for backup freshness** — replaces the retired Kuma
      Backups group. A check detects a thing that *didn't happen*, which is
      the shape of "the nightly backup silently stopped running three weeks
      ago"; a last-backup sensor only tells you the date if something is
      still writing one. Empty Healthchecks portal first; one check per job
      during the per-container pass. Ping URL is
      `http://192.168.5.8:8002/ping/<uuid>` (IP, not the hostname). Runbook:
      servers repo `hosts/jack-sparrow/duplicati-runbook.md`.

## Config reconciliation

- [ ] Go through pending README / HAS checklist items and close or update what’s stale
- [ ] Find unused or rarely used entities, automations, scripts, and dashboard bits
- [ ] Remove or archive what’s no longer needed; keep what’s still useful lean

## Logs

- [ ] Review Home Assistant warnings / errors in the system log
- [ ] Fix root causes (or silence true noise) so the log stays clean

## Integrations

- [ ] ⏸️ **Deluge** (core, no HACS) —
      https://www.home-assistant.io/integrations/deluge/
      **Do not add yet.** Empty client on jack-sparrow is live; liveness is
      already `sensor.deluge_state` via Portainer. This integration talks
      to the daemon and is only worth it once there are torrents.
      Trigger: jack-sparrow TODO → Deluge phase 1b, after Pool 1 path +
      arr + cutover. Then: host `192.168.5.8`, port `58846` (daemon, not
      WebUI, not the hostname). Auth from
      `/volume2/docker/deluge/config/auth` on the NAS.
- [ ] EcoFlow (BLE or Cloud... need to decide)
- [x] ~~**Portainer** (core integration, no HACS) — Docker on jack-sparrow~~
      Added 2026-08-13, the same day the container was deployed. HA config is
      written: `entities/templates/portainer.yaml`,
      `dashboards/jack-sparrow/views/05-containers.yaml`. Board is at
      **`/jack-sparrow/containers`**. No automations — see the reasoning below.
  - [x] ~~⚠️ **Verify the entity-ID suffixes**~~ — done 2026-08-15 against the
        live instance. **All correct**: `_state`, `_health`, `_image`,
        `_cpu_usage_total`, `_memory_usage_percentage`. `_health` exists on
        only `gluetun` and `uptime_kuma`, exactly as the "only images declaring
        a HEALTHCHECK" caveat predicted — the defensive `| list`-then-truth-test
        was right.
        **The dump found a different bug the suffixes hid:**
        `binary_sensor.local_status` is the **endpoint** device, not a
        container. `portainer.yaml` asserted endpoints have no binary sensor;
        they do. `container_count` read **11 for 10 containers** and
        `running_count` was inflated to match. Fixed by filtering on a `_state`
        sibling — structural, since containers have one and the endpoint does
        not, so it survives the environment being renamed off "local". The
        endpoint is now surfaced separately as `endpoint_ok`.
  - [x] ~~🐛 **Orphaned Duplicati device**~~ — deleted 2026-08-15. A full
        duplicate set under `*.e1a4ef9e3497_duplicati_*`, container-ID-prefixed,
        left behind when Duplicati was recreated to add the docker socket and
        scripts mounts. **Confirmed absent from Portainer itself** — purely an
        HA registry leftover. It had no `binary_sensor`, so container counts
        escaped, but `update.e1a4ef9e3497_duplicati_image_update_available` was
        double-counting Duplicati in `sensor.docker_image_updates`.

        ⚠️ **Pattern worth remembering — this is the second one.** The paused
        Kuma monitor left the same kind of ghost. HA cannot distinguish a
        device that no longer exists from one that has merely gone quiet, so it
        never cleans up on its own. **Recreating a container can mint a new
        device and strand the old one**, and the symptom is a silently inflated
        count rather than an error. After any container recreate, check
        Settings → Devices & Services for a duplicate — or compare
        `container_count` against `sudo docker ps` on the NAS.
  - [ ] Confirm Portainer surfaces the three UGOS projects as **stacks**. The
        Stacks card is `show_empty: false`, so if UGOS labels its projects in
        a way Portainer does not read as a stack, the card is simply absent
        and nothing tells you which it was.
  - [x] ~~Decide on a "container down" automation~~ — **written 2026-08-15**,
        `automations/lab/portainer_container_down.yaml`. The double-notify
        concern was right and is respected: it stays deliberately silent about
        ordinary container-down, and covers only what Kuma structurally cannot
        see. **Three** shapes, not the two predicted here:
        - `restarting` for 5+ min (crash loop — rebinds its port often enough
          that a Kuma check passes on the retry)
        - `container_count` *dropping* (a removed container has no status left
          to be down; compares against its own previous value, so no expected
          count goes stale)
        - **`uptime-kuma` itself stopped or missing** — the case that made this
          urgent rather than nice-to-have. The nightly Duplicati job now
          *stops* that container to copy its SQLite/WAL data dir consistently;
          if the restart fails, Kuma cannot report its own death, Healthchecks
          only sees the backup, and `sensor.lab_availability` goes
          *unavailable* rather than down so the Kuma automation declines to
          fire. `for: 10 minutes` clears the seconds-long healthy stop without
          hardcoding the 3am schedule.
        ⚠️ "Cannot find the container" alerts rather than passing — a search
        matching nothing must not read healthy.
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
  - [x] ~~Set up the Kuma-native channel (runbook Part 3)~~ — **done and
        tested.** **Discord**, not ntfy: it is already the lab's out-of-band
        path (Healthchecks alerts through it too), so this avoided a second
        dependency for one channel's worth of alerts. Attached to exactly
        `Internet`, `Gateway`, `homeassistant` — the three HA cannot report on,
        because HA cannot notify you that HA is down. **Do not attach it to
        anything else**: everything else double-notifies against
        `uptime_kuma_monitor_down.yaml`.
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
- [x] ~~**Scrutiny** (`vitals5/ha_scrutiny`, HACS default catalog) — drive SMART
      health from jack-sparrow.~~ **Done.** Live since 2026-08-13;
      `entities/templates/scrutiny.yaml`,
      `dashboards/jack-sparrow/views/04-drives.yaml` and
      `automations/lab/scrutiny_*.yaml` are all deployed and rendering real
      values. Servers-side runbook: `hosts/jack-sparrow/scrutiny-runbook.md`.
  - [x] ~~Verify the `realloc.*_raw` / `pending.*_raw` regexes against real
        entity IDs~~ — done 2026-08-13, and the suffixes were **tightened** as
        a result. `realloc.*_raw$` matched both
        `_reallocated_sectors_count_raw` (attribute 5, wanted) and
        `_reallocation_event_count_raw` (attribute 196, a different
        attribute) — silently double-counting, and reading fine only while
        everything was zero. Both are now anchored to the full name. Do not
        loosen them; see the header comment in the file.
  - [x] ~~Turn on **Critical SMART attribute sensors** + **Enable raw value
        sensors**~~ — both on. Raw sensors are the point: the text sensors are
        enums HA cannot plot, the raw companions are numeric and land in
        long-term statistics.
  - [x] ~~Integration URL~~ — moved onto
        `https://scrutiny.home.masterscrib.net` 2026-08-14. ⚠️ **This is the
        change that silently killed every template rollup until HA was
        restarted.** Reloading is not enough; nothing is logged.

## Notes

- Existing backup sensors live in `entities/command_line/sensors/pi_backups.yaml` (HA, Pi-hole, Deluge, Plex).
- Lab view: `ui_lovelace_minimalist/dashboard/views/mainviews/lab.yaml`

## After poat-seedbox is decommissioned

Do **not** start this while rpi1 still exists, even powered off. The Lab
card, ping sensor and Kuma monitor are how you would notice it came back.
Trigger: jack-sparrow Deluge has been the live seedbox long enough that the
Pi will not be powered on again. Servers-side pointer:
`servers/hosts/jack-sparrow/TODO.md` (gluetun / phase 1b).

The NordVPN-on-the-Pi stack is replaced by gluetun on the NAS. These files
are the old path (`nordlynx` in rpi_monitor attributes, ICMP ping, a backup
tree on poat-share). They will page, go stale, or render a dead host forever
if left.

### Home Assistant — delete / stop referencing

- [ ] `entities/templates/seedbox_vpn_on.yaml` — `sensor.seedbox_vpn_on`
- [ ] `automations/lab/seedbox_vpn_off.yaml` and its row in
      `automations/lab/README.md`
- [ ] `customizations/entities/entities.yaml` — `sensor.seedbox_vpn_on` and
      `binary_sensor.poat_seedbox_local`
- [ ] `entities/templates/AGENTS.md` — `seedbox_vpn_on.yaml` row
- [ ] `entities/templates/pi_statistics.yaml` — every
      `sensor.poat_seedbox_rpi_monitor_poat_seedbox` block
- [ ] `entities/command_line/sensors/pi_backups.yaml` — `sensor.deluge_last_backup`
      (`/media/pi_backups/deluge-backup`). Replace only if the new container
      has its own backup path; do not retarget this find at jack-sparrow
      without checking the path exists.
- [ ] `ui_lovelace_minimalist/dashboard/views/mainviews/lab.yaml` — the
      `poat_seedbox` mqtt_control card (`sensor.deluge_last_backup`) and the
      `sensor.poat_seedbox_rpi_monitor_poat_seedbox` row
- [ ] Ping: `binary_sensor.poat_seedbox_local` config entry, plus the
      commented line in `automations/sensors/ping_interval.yaml`
- [ ] Drop `poat-seedbox` from the legacy-vs-Kuma table in this file once
      the swap above is done

### Kuma / servers repo — same window

- [ ] Pause or delete monitor `poat-seedbox - Deluge` (`192.168.4.109:58846`)
- [ ] Mark `servers/hosts/poat-seedbox/HOST.md` retired; leave discovery
- [ ] Close `servers/TODO.md` "poat-seedbox — VPN resiliency & no-leak"
      (superseded by gluetun; do not finish the Nord kill-switch work)
- [ ] Retarget `servers/plex-automation-plan.md` ("Deluge stays on rpi1")
- [ ] Update jack-sparrow `HOST.md` topology (poat-seedbox is no longer the
      Deluge completer) and `servers/README.md` host table
