# Home Assistant cleanup

Working notes for streamlining dashboards, entities, backups, and log noise.

## Dashboards

- [x] ~~Polish and reconcile Matrix `lab.yaml`~~ — retired 2026-08-22.
      `/the-matrix/lab` and `/the-matrix/z-wave` are gone. Home's
      server-closet card lands on `/home-lab/uptime`. Pi-hole is
      `/home-lab/pi-hole`; Z-Wave is `/home-lab/z-wave` (grouped by type);
      Pi graphs + Tasmota + reboot/shutdown + printer are `/home-lab/hosts`.
      Share-space graphs (aristodemos / odysseus) were not moved;
      the `share_sizes.yaml` command_line sensors behind them were
      deleted 2026-08-25 with the share Pi.
- [x] ~~Walk other mainviews / subviews and clean up unused or low-value cards~~
      — 2026-08-22. Lights view gone (welcome pill → Cameras). Lab pill
      → `/home-lab/uptime`. Network dropped the duplicate rate/Wi-Fi
      graphs. House dumps (batteries / idle alerts / GPS) sit behind
      folds. Vacation lost the people cards. Patio owns its eero.
      `rooms/test.yaml` and `card_wifi_signal` removed.
- [x] ~~Streamline layouts so status, controls, and alerts are easier to scan~~
      — 2026-08-22. House is alerts → climate/blinds → status (cameras +
      graphs); firing alerts sit above mutes; phones stacked with a
      glanceable row + More fold. Vacation opens on away checks / mode,
      cameras under that. Hosts shows Pi graphs before reboot controls.
      Network and Lab Uptime were already scan-first.
- [x] ~~Surface backup status more clearly on Lab / related views~~
      — 2026-08-22. One card, `dashboards/cards/backup-glance.yaml`,
      `!include`d on Uptime / Backups / Hosts. Tiles are Duplicati
      only (rollup + each job's `_date`). Command_line share-find
      sensors are off the glance.

## Backups

- [ ] Confirm every important service is a **Duplicati job** — HA
      already has Date + Status per job (`integration_entities('duplicati')`).
      Do not add more `command_line` finds. Legacy share-find sensors in
      `entities/command_line/sensors/pi_backups.yaml` were removed 2026-08-24
      (paths were gone; they were flooding `command_line` logs). Remaining
      work is confirming every job shows on `/home-lab/backups` after a
      Duplicati integration reload.
- [ ] Add alerts (and supporting entities) when backups go stale or missing
- [x] ~~Make backup health visible on the dashboard, not just buried in entity lists~~
      — 2026-08-22 with the Lab backup tiles above. Stale/missing
      *alerts* and Healthchecks are still open.
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
        until Portainer / lil-bit are up.
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

**Not a mechanical swap.** The legacy sensors used to be *conditions* on
the Matrix Lab view (now retired). `ping_interval.yaml` and
`binary_sensor.poat_hole_local` were removed 2026-08-25 — Kuma
`poat-hole - DNS` / `poat-hole - admin` already watch the service, not
ICMP. Remaining YAML consumer is `binary_sensor.poat_plex_local` as a
visibility gate on `/home-lab/hosts` (plus its customization).

| Legacy | Kuma monitor | Same thing? |
| --- | --- | --- |
| ~~`binary_sensor.poat_hole_local`~~ | `poat-hole - DNS` / `poat-hole - admin` | YAML gone 2026-08-25. Disable the ping config entry. Kuma is better — checks resolution, not ICMP. |
| ~~`binary_sensor.poat_share_local`~~ | ~~`poat-share - SMB (IP)` + `(name)`~~ | Share Pi gone 2026-08-25. YAML gone. Pause/delete the two Kuma monitors; disable the ping config entry; MQTT `rpi_monitor` + eero client are leftovers. |
| ~~`binary_sensor.poat_seedbox_local`~~ | ~~`poat-seedbox - Deluge`~~ | Seedbox Pi gone 2026-08-25. YAML gone (`seedbox_vpn_on` + alert). Pause/delete the Kuma monitor; disable the ping config entry; MQTT `rpi_monitor` + eero client are leftovers. |
| `binary_sensor.poat_plex_local` | `lil-bit - Plex` | ⚠️ **probably different hosts** — confirm before swapping. Still used on `/home-lab/hosts`. |

- [ ] Confirm whether `poat-plex` and `lil-bit` are the same machine. Kuma
      monitors `192.168.4.161`.
- [ ] Then swap `binary_sensor.poat_plex_local` on `/home-lab/hosts` (and
      its customization) to the matching `sensor.*_status` `up`.
- [x] ~~Retire `automations/sensors/ping_interval.yaml`~~ — deleted
      2026-08-25 with `poat_hole_local`. It only existed to work around
      home-assistant/core#105041 (ping sensors not honouring an update
      interval).
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

- Existing backup sensors are Duplicati (`sensor.duplicati_backup_health`
  plus per-job `_date` / `_status`). The old command_line share-find
  sensors in `pi_backups.yaml` were deleted 2026-08-24.
- Lab dashboard: `dashboards/lab.yaml` (`/home-lab/uptime`)

## Retired Pis (share + seedbox) — leftover outside YAML

HA YAML for both hosts was removed 2026-08-25 (VPN template + alert,
customizations, `share_sizes.yaml` command_line sensors, ping_interval,
offline-list filters). Remaining work is registry / Kuma / servers repo.
NordVPN-on-the-Pi is replaced by gluetun on the NAS.

### Home Assistant UI — ping, eero, MQTT

- [ ] Disable/delete ping config entries: `binary_sensor.poat_share_local`,
      `binary_sensor.poat_seedbox_local`, `binary_sensor.poat_hole_local`
- [ ] Remove leftover MQTT `rpi_monitor` devices for both hosts
- [ ] Remove leftover eero clients
- [ ] Template `sensor.seedbox_vpn_on` and command_line Odysseus /
      Aristodemos sensors will linger in the entity registry until purged

### Kuma / servers repo

- [ ] Pause or delete `poat-share - SMB (IP)` + `(name)` (they sit red on
      `/home-lab/uptime` until then)
- [ ] Pause or delete `poat-seedbox - Deluge` (`192.168.4.109:58846`)
- [ ] Mark `servers/hosts/poat-seedbox/HOST.md` retired; leave discovery
- [ ] Close `servers/TODO.md` "poat-seedbox — VPN resiliency & no-leak"
      (superseded by gluetun; do not finish the Nord kill-switch work)
- [ ] Retarget `servers/plex-automation-plan.md` ("Deluge stays on rpi1")
- [ ] Update jack-sparrow `HOST.md` topology (poat-seedbox is no longer the
      Deluge completer) and `servers/README.md` host table
