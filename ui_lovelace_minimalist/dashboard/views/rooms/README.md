# Rooms

One view per room, opened by tapping that room's `room-summary-card` on
Home. Every room follows the same standard so they look and behave the
same. Progress is tracked in the "Room views" section of `/TODO.md`.

## The standard

Each room is two files:

| File | Path | What's on it |
| --- | --- | --- |
| `<room>.yaml` | `/the-matrix/<room>` | Daily controls only |
| `<room>-details.yaml` | `/the-matrix/<room>-details` | Everything else |

### Room view (`<room>.yaml`)

`type: sections`, `max_columns: 3`, `subview: true`,
`back_path: /the-matrix/home`. Native cards (`tile`, `heading`,
`picture-entity`) plus `toolbar-status-chips`, so the main page cannot
break on a ULM template update.

1. **Status** — `toolbar-status-chips` (full width, auto rows) shows
   every entity in the area labelled `status`: doors, smoke, CO, leaks.
   What shows is decided by labels in Settings, not YAML. If the room
   has occupancy sensors, an `Occupancy` heading over a
   `mushroom-chips-card` of template chips (icon coloured only while
   `on`, short label, tap for more-info). Tiles, glance and heading
   badges were all tried on Office and were too big or badly placed. Below it, a
   `Climate` heading, then temperature (`color: red`) and humidity (`color: blue`) tiles with a
   24 h `trend-graph`, in a nested 2-column `grid`. Entities that should
   count toward the Home tile's problem badge get the `problem` label.
2. **Lights** — light and fan tiles with `tap_action: toggle`, plus
   blinds with open/close and position. Lights get `light-brightness`.
3. **Media** — TVs and speakers as `media-control` (shows the app /
   artwork). Consoles as a plain tile.
4. **Camera** — `picture-entity`, `camera_view: auto` (snapshot, not a
   live stream on every wall tablet). Tap for live.
5. **All devices & details** — a heading with `tap_action` navigate to
   the details subview.

Skip any section the room doesn't have. Keep the order.

**Balance the columns.** Sections lay out in rows: the next row starts
below the tallest section, so an uneven row leaves a gap. Group the
headings into three one-column sections of similar height rather than
one section per heading. Office is Status + Media | Lights & blinds |
Camera, then the details link spanning all three.

A battery worth glancing at (blinds) is a ring in the tile's top-right
corner, drawn by `card_mod` as `ha-card::after` — copy the block from
the Office blinds tile and change the sensor. A tile cannot show a
second entity's state any other way.

### Details view (`<room>-details.yaml`)

`back_path: /the-matrix/<room>`. Anything integration-specific or
rarely used: full Frigate card (`frigate_camera`), energy
(`area-energy-card`), integration cards (whisker, petkit, vacuum...),
remotes.

Keep the camera large, but not a 2+1 section split: that left Z-Wave
at one-third and the cards collapsed. Put camera and Z-Wave in one
span-3 `layout-card` (`columns: full`) with
`minmax(0, 1.3fr) minmax(560px, 1fr)` so Z-Wave never drops below the
width last-seen / alive need. Stack below 1100px. Z-Wave still uses
`use_icons_instead_of_names`. Last section is always `room_devices`
spanning 3, which skips any device that has a `zwave_js` entity so
Zooz nodes are not listed twice. `room_devices` is 3-up on a monitor.

## Rules

- **The area registry is the source of truth.** If a device shows on the
  wrong room's detail page, fix its area in Settings, not the YAML.
- **Prefer existing cards.** Core cards first, then a HACS card built
  for that integration, and only then a decluttering template.
- **Shared blocks go in `card_declutter/`**, not copied between rooms.
  `room_devices` and `xbox_remote` started there.
