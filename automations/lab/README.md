# 📁 lab/

Automations for the home lab itself — the NAS, the Pis, the containers and the
network — as opposed to the house. Everything here alerts on **infrastructure**
that has no user-visible symptom until it is already a problem.

The lab's own documentation lives in the **`servers`** repo. This folder holds
only the HA side; the runbooks that explain *why* each backing sensor exists are
cross-referenced per file.

## The rule these all follow

Every automation here exists because **the failure it detects is otherwise
silent**. That is the bar for adding one. A failure you would notice anyway —
Plex not loading, the lights not responding — does not need an automation, it
needs nothing. These cover the failures where the system keeps looking healthy:

| File | Detects | Silent because |
|---|---|---|
| `cert_expiry.yaml` | Wildcard cert inside 21 days, **or** the TLS handshake failing right now | certbot renews unattended over DNS-01; a broken renewal produces no error anywhere until everything goes red at once |
| `diun_not_running.yaml` | The Diun container in any state but `running` | A stopped update-notifier and one with nothing to report are indistinguishable |
| `scrutiny_drive_failed.yaml` | Any drive's SMART overall status leaving *Passed* | RAID 5 keeps serving reads from a degraded array without complaint |
| `scrutiny_drive_temperature.yaml` | Hottest drive sustained above 122 °F for an hour | Heat shortens life without ever producing an error |
| `scrutiny_sectors_reallocated.yaml` | The first reallocated sector on any drive, `> 0` | The earliest actionable storage signal, long before anything reports "failed" |
| `seedbox_vpn_off.yaml` | Seedbox VPN not running | Torrents keep flowing, just not through the tunnel |
| `uptime_kuma_monitor_down.yaml` | Any Kuma monitor down, plus a real all-clear | — (this is the broad net the others sit inside) |

## House patterns

Worth matching when adding a file here, because each one was learned from a
specific failure:

- **`for:` on every trigger, usually 10 minutes.** This is not flap control —
  it rides out a Home Assistant restart. Backing sensors read `unavailable`
  while integrations and templates reload, and without the delay a routine
  restart pages you. ⚠️ On 2026-08-14 a stale template listener after an
  integration reconfigure made every rollup on the lab board read zero; a
  restart fixed it, and nothing was logged.
- **A `not / state: [unknown, unavailable]` condition.** Same reason, belt and
  braces. Note what it costs: it also hides an entity that is *permanently*
  unavailable because the thing was deleted. Say so in the file when it matters.
- **An all-clear branch.** Recovery closes the loop so nobody has to go and
  look. Gate it so it cannot fire on a restart — `uptime_kuma_monitor_down.yaml`
  requires a non-empty `was_down` list for exactly this reason.
- **`notify.persistent_notification` always; mobile push gated on
  `input_boolean.poat_mute`.** The persistent notification is the record, the
  push is the interrupt, and only the interrupt should be muteable.
- **⚠️ Never predict an entity ID.** Verify it in Developer Tools → States
  first. A template or regex matching nothing renders *healthy forever* rather
  than erroring — this has already happened in this lab with the Portainer
  template entities, and it is the most expensive mistake in the folder.
- **Prefer `!= healthy` over a list of bad states.** A match-list silently
  misses any value that wasn't anticipated, which is the same
  reads-healthy-forever bug wearing a different hat.

## Two independent paths, on purpose

Most of these overlap with an Uptime Kuma monitor, and the overlap is
deliberate rather than an oversight: **Kuma is what tells you when Home
Assistant is down, so HA cannot be the only thing watching.** Neither system is
trusted to report its own death.

⚠️ **`diun_not_running.yaml` is the documented exception** — one path only. The
Kuma monitor type that would cover it requires mounting the Docker socket into
Uptime Kuma, which upstream warns "gives that full control over the Docker
daemon on the host". That trade was declined. See the file header and
`servers/hosts/jack-sparrow/diun-dozzle-runbook.md` §4.2.

## Related

- `servers/hosts/jack-sparrow/HOST.md` — the NAS, ports, change log
- `servers/hosts/jack-sparrow/uptime-kuma-runbook.md`
- `servers/hosts/jack-sparrow/scrutiny-runbook.md`
- `servers/hosts/jack-sparrow/npm-runbook.md`
- `servers/hosts/jack-sparrow/diun-dozzle-runbook.md`
- `servers/_template/new-container-checklist.md` — the eight gates every new
  container clears; gates 5 and 6 are what land in this folder
