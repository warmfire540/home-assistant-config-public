# Entities

This directory contains entity configurations organized by domain (like lights, switches, sensors, etc.).

## Purpose

- Organizes entities by their respective domains
- Makes it easier to locate and modify specific entity configurations
- Improves maintainability of large configurations
- Facilitates better organization of complex setups

## Structure

Each folder corresponds to a specific Home Assistant domain (e.g., `lights/`, `alerts/`, `notify/`).

## Usage

Entity configurations are automatically loaded through includes in the main configuration.yaml file.
