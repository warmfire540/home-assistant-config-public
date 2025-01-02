# My Home Assistant Configuration 🏠

![Home Assistant](https://img.shields.io/badge/home%20assistant-%2341BDF5.svg?style=for-the-badge&logo=home-assistant&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![YAML](https://img.shields.io/badge/yaml-%23ffffff.svg?style=for-the-badge&logo=yaml&logoColor=151515)

## Table of Contents

- [Overview](#overview)
- [Hardware](#hardware)
- [Integrations](#integrations)
- [Configuration Layout](#configuration-layout)
- [Missing Files](#missing-files)

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
automations/
└── systems/
themes/
ui_lovelace_minimalist/
└── custom_cards/
    └── templates/
        ├── styles/
        └── variables/
```

- [`automations/`](automations/) - automations of course
  - [`systems/`](automations/systems/) - automations related to core system functionality
- [`themes/`](themes/) - themes for the UI, I don't customize these
- [`ui_lovelace_minimalist/`](ui_lovelace_minimalist/) - main dashboard framework
  - [`custom_cards/`](ui_lovelace_minimalist/custom_cards) - custom cards for the layout
    - [`templates/`](ui_lovelace_minimalist/custom_cards/templates) - templates for cards
      - [`styles/`](ui_lovelace_minimalist/custom_cards/templates/styles) - templates for visual aspects
      - [`variables/`](ui_lovelace_minimalist/custom_cards/templates/variables) - templates to handle common variables

## Missing Files

For security reasons, the following files have been excluded from this repository:

- `secrets.yaml` - Contains sensitive information like passwords and tokens
- `.storage/*` - Home Assistant internal storage
- `known_devices.yaml` - Device tracker entries
- `ip_bans.yaml` - IP ban list
- `*.db` - Database files
- `*.log` - Log files
