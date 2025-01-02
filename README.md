# My Home Assistant Configuration 🏠

![Home Assistant](https://img.shields.io/badge/home%20assistant-%2341BDF5.svg?style=for-the-badge&logo=home-assistant&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![YAML](https://img.shields.io/badge/yaml-%23ffffff.svg?style=for-the-badge&logo=yaml&logoColor=151515)

## Table of Contents

- [Overview](#overview)
- [Hardware](#hardware)
- [Integrations](#integrations)
- [Missing Files](#missing-files)

## Overview

This repository contains my personal Home Assistant configuration files. I maintain this configuration to automate and control various aspects of my smart home, focusing on reliability and ease of use. The setup includes lighting control, climate management, and security monitoring.

## Hardware

Core infrastructure:

- Home Assistant instance running on a Raspberry Pi 4 (8GB)
- Z-Wave Controller: 800LR
- Sonoff RF Bridge 433 - Tasmota

Connected devices:

- Philips Hue Bridge with various bulbs
- Aqara Temperature & Humidity Sensors
- Shelly smart switches
- Nest Thermostat
- Ring Video Doorbell

## Integrations

Key integrations used in this configuration:

- **Core Integrations**

  - MQTT
  - Z-Wave JS
  - [Ui-Minimalist Theme](https://ui-lovelace-minimalist.github.io/UI/)

- **Device Integrations**
  - tbd

## Configuration Layout

I'm using the README files as a way to keep track of areas that I'm revamping for 2025 to clean up my instance and make things more reusable and wife friendly.

### Structure

```
ui_lovelace_minimalist/
└── custom_cards/
    └── templates/
        ├── styles/
        └── variables/
```

[`ui_lovelace_minimalist/`](ui_lovelace_minimalist/)

- [`custom_cards/`](ui_lovelace_minimalist/custom_cards)
  - [`templates/`](ui_lovelace_minimalist/custom_cards/templates)
    - [`styles/`](ui_lovelace_minimalist/custom_cards/templates/styles)
    - [`variables/`](ui_lovelace_minimalist/custom_cards/templates/variables)

## Missing Files

For security reasons, the following files have been excluded from this repository:

- `secrets.yaml` - Contains sensitive information like passwords and tokens
- `.storage/*` - Home Assistant internal storage
- `known_devices.yaml` - Device tracker entries
- `ip_bans.yaml` - IP ban list
- `*.db` - Database files
- `*.log` - Log files
