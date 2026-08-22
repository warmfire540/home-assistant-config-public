# Mainviews

The mainviews directory contains YAML configurations for primary dashboard views that cover general categories of your home automation system.

## Configuration Files

- `cats.yaml` - Pet monitoring and automation
- `house.yaml` - General house controls and status
- `network.yaml` - WAN, Wi-Fi, disconnected / connected devices

Cameras lives under `subviews/` and is a welcome pill (it replaced Lights).

Lab (Pi-hole, Z-Wave, uptime, backups) lives on the standalone
`/home-lab` dashboard (`dashboards/lab.yaml`), not here.

These views represent the main categories accessible from the dashboard's primary navigation.
