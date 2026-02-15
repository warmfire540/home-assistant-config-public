# Systems Automations

This directory contains automations related to core system functionality, notifications, and alerts.

## Automations

### alert_to_persistent.yaml

Converts alert entities to persistent notifications.

**Purpose:**

- Creates persistent UI notifications when alert entities are triggered
- Ensures important alerts remain visible until addressed

**Key Features:**

- Triggers on alert entity state changes
- Maintains alert visibility in the UI
- Prevents critical alerts from being missed

### auto_close_alerts.yaml

Automatically manages and closes low-priority alerts.

**Purpose:**

- Reduces notification noise by auto-closing non-critical alerts
- Prevents alert buildup in the system

**Key Features:**

- Identifies low-priority alerts
- Implements automated cleanup
- Helps prevent alert fatigue

### calendar_maintenance_tracker.yaml

Unified calendar-based maintenance tracking system.

**Purpose:**

- Consolidates all calendar-based maintenance tasks into a single automation
- Triggers input_boolean entities when calendar events start
- Provides a DRY approach to maintenance scheduling

**Key Features:**

- Maps calendar events to corresponding input_boolean entities
- Easily extensible for new maintenance tasks
- Single point of maintenance for all calendar-based triggers
- Currently handles: Katchy cleaning, air filter changes, and dishwasher maintenance

### ha_log_event_trigger.yaml

Monitors Home Assistant logs for important events.

**Purpose:**

- Detects and notifies about system warnings and errors
- Helps maintain system health through early detection

**Key Features:**

- Monitors warning and error level log events
- Triggers notifications for system issues
- Enables proactive system maintenance

### event_entity_to_alert.yaml

Creates AI-generated alerts from event entity state changes.

**Purpose:**

- Monitors event entities (e.g. event.washy_error) for state changes
- Event entities use timestamps as state—any change means the event fired
- Generates notifications when configured event entities trigger

**Key Features:**

- Triggers on any state change (excludes unavailable/unknown)
- Uses notify.family_ai for consistent alert delivery
- Add event entities to the entity_id list to enable notifications
- See: https://home-assistant.io/integrations/event/

### sensor_state_to_alert.yaml

Creates AI-generated alerts from sensor state changes.

**Purpose:**

- Monitors configured sensors for state changes to "on"
- Generates contextual notifications using AI when sensors activate
- Provides intelligent alerting for security, maintenance, and monitoring sensors

**Key Features:**

- Generic automation for any sensor that changes to "on" state
- Rich context provided to AI for intelligent notification generation
- Includes sensor details, timing, battery level, and device class
- Integrates with existing notify.family_ai system
- Easily configurable sensor list
- Optional minimum duration to prevent rapid-fire notifications

### unmute_people.yaml

Manages temporary notification muting for household members.

**Purpose:**

- Provides temporary muting of notifications
- Automatically restores notifications after one hour

**Key Features:**

- One-hour automatic unmute timer
- Prevents indefinite notification muting
- Maintains household communication flow

## Configuration

Each automation in this directory can be configured through its respective YAML file. Key configuration points:

1. Alert thresholds and priorities
2. Notification delivery methods
3. Timing parameters
4. User-specific settings

## Dependencies

These automations may depend on:

- Alert entities being properly configured
- Notification services being set up
- Proper user presence detection
