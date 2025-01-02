# My Home Assistant Configuration 🏠

![Home Assistant](https://img.shields.io/badge/home%20assistant-%2341BDF5.svg?style=for-the-badge&logo=home-assistant&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![YAML](https://img.shields.io/badge/yaml-%23ffffff.svg?style=for-the-badge&logo=yaml&logoColor=151515)

![stars](https://img.shields.io/github/stars/warmfire540/home-assistant-config-public.svg?style=for-the-badge)
![home](https://img.shields.io/github/last-commit/warmfire540/home-assistant-config-public.svg?style=for-the-badge)
![commits](https://img.shields.io/github/commit-activity/y/warmfire540/home-assistant-config-public?style=for-the-badge)

## Table of Contents

- [Overview](#overview)
- [Hardware](#hardware)
- [Integrations](#integrations)
- [Configuration Layout](#configuration-layout)
- [Missing Files](#missing-files)
- [Screenshots](#screenshots)

## Overview

This repository contains my personal Home Assistant configuration files. I maintain this configuration to automate and control various aspects of my smart home, focusing on reliability and ease of use. The setup includes lighting control, climate management, and security monitoring.

## Hardware

Core infrastructure:

- Home Assistant instance running on a Raspberry Pi 4 (8GB)
- Z-Wave Controller: 800LR
- Sonoff RF Bridge 433 - Tasmota

Connected devices:

- Lots of Zooz Z-Wave Devices
- LG (fridge, TVs, etc)
- Petkit
- Vacuums
- Garage

## Integrations

Key integrations used in this configuration:

- **Core Integrations**

  - Alert
  - Bluetooth
  - Change device type of a switch
  - Command Line
  - Counter
  - DLNA Digital Media Renderer
  - Group
  - Home Assistant Supervisor
  - iBeacon Tracker
  - Input Boolean
  - Input Button
  - Input Datetime
  - Input Number
  - Input Select
  - Input Text
  - Local Calendar
  - Local To-do
  - Meteorologisk institutt (Met.no)
  - Mobile App
  - MQTT
  - Ping (ICMP)
  - Python Scripts
  - Raspberry Pi Power Supply Checker
  - Schedule
  - Shopping List
  - Sun
  - System Monitor
  - Template
  - Timer
  - UPnP/IGD
  - Xbox
  - Z-Wave

- **Device Integrations**

  - Brother Printer
  - Browser mod
  - eero
  - Emporia Vue
  - Google Generative AI
  - Google Nest
  - HACS
  - LG ThinQ
  - LG webOS Smart TV
  - Motionblinds
  - Neato Botvac
  - PetKit
  - Pi-hole
  - Plex Media Server
  - Speedtest.net
  - Tasmota
  - Tile
  - Tuya
  - UI Lovelace Minimalist

## Configuration Layout

I'm using the README files as a way to keep track of areas that I'm revamping for 2025 to clean up my instance and make things more reusable and wife friendly.

### Structure

```
.github/
automations/
└── systems/
blueprints/
themes/
ui_lovelace_minimalist/
└── custom_cards/
    └── templates/
        ├── styles/
        └── variables/
```

- [`.github/`](.github/) - GitHub workflows
- [`automations/`](automations/) - automations of course
  - [`systems/`](automations/systems/) - automations related to core system functionality
- [`blueprints/`](blueprints/) - HA Blueprints - I don't have a use for these
- [`themes/`](themes/) - themes for the UI, I don't customize these
- [`ui_lovelace_minimalist/`](ui_lovelace_minimalist/) - main dashboard framework
  - [`custom_cards/`](ui_lovelace_minimalist/custom_cards) - custom cards for the layout
    - [`templates/`](ui_lovelace_minimalist/custom_cards/templates) - templates for cards
      - [`styles/`](ui_lovelace_minimalist/custom_cards/templates/styles) - templates for visual aspects
      - [`variables/`](ui_lovelace_minimalist/custom_cards/templates/variables) - templates to handle common variables

### Automations

The following automations I have created to for various reasons. See [`automations/`](automations/) for more info.

- systems - Automations related to core system, notifications, and alerts.
  - `alert_to_persistent.yaml` - Handles peristent alerts when alert entity is triggered
  - `auto_close_alerts.yaml` - Handles closing some low value alerts
  - `ha_log_event_trigger.yaml` - Triggers when there is new warning or error
  - `unmute_people.yaml` - Handles unmuting people after an hour

## Missing Files

For security reasons, the following files have been excluded from this repository:

- `secrets.yaml` - Contains sensitive information like passwords and tokens
- `.storage/*` - Home Assistant internal storage
- `known_devices.yaml` - Device tracker entries
- `ip_bans.yaml` - IP ban list
- `*.db` - Database files
- `*.log` - Log files
- `.ssh` - ssh related secrets
- `custom_components` - HACS downloaded integrations

## Screenshots

Examples of some pages and where to find the code.

> [!NOTE]  
> The dashboard is highly evolving and thus these screenshots may not be an accurate representation of the current state.

### Responsiveness

- [ui_lovelace_minimalist/dashboard/views/01-home.yaml](ui_lovelace_minimalist/dashboard/views/01-home.yaml)

Full Screen Dashboard
![full screen](assets/views/home/the-matrix_full.png 'Full Screen Dashboard')

Portrait Monitor Dashboard
![portrait screen](assets/views/home/the-matrix_portrait.png 'Portrait Screen Dashboard')

Mobile Dashboard
![mobile screen](assets/views/home/the-matrix_mobile.png 'Mobile Screen Dashboard')
