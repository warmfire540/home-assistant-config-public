# Python Scripts

This directory contains custom Python scripts that extend Home Assistant's functionality.

## Current Scripts

### rfbridge_demux.py

- Handles integration with Tasmota RF Bridge
- Demultiplexes RF signals for processing
- Enables breaking up MQTT signals into entity updates.

## Usage

Place Python scripts in this directory and they will be available to call from automations using the `python_script.script_name` service.
