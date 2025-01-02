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

### ha_log_event_trigger.yaml
Monitors Home Assistant logs for important events.

**Purpose:**
- Detects and notifies about system warnings and errors
- Helps maintain system health through early detection

**Key Features:**
- Monitors warning and error level log events
- Triggers notifications for system issues
- Enables proactive system maintenance

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
