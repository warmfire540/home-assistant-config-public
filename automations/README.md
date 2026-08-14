# Automations

This folder contains all of the automations I use.
As with everything, some things could still be optimized, but that's work in progress.

Each automation YAML file also contains a description, but here is a brief overview.

## Directory Structure

The automations are organized into the following subdirectories:

### 📁 systems/

Contains core system automations focusing on:

- System alerts and notifications
- System monitoring and logging
- User notification management

For detailed information about the system automations, see the README in the ['systems/'](systems/) directory.

### 📁 lab/

Home lab infrastructure — the NAS (`jack-sparrow`), the Pis, the containers and
the network. Drive health, certificate expiry, container liveness, uptime
monitoring.

Everything in there follows one rule: it exists because **the failure it
detects is otherwise silent**. See the README in the ['lab/'](lab/) directory
for the full table and the house patterns.

## Adding New Automations

When adding new automations to this directory:

1. Place them in the appropriate subdirectory
2. Follow the existing naming convention
3. Update the corresponding README
4. Test thoroughly before deploying

## Best Practices

- Keep automations organized by function
- Use clear, descriptive filenames
- Document any dependencies
- Include comments in automation files
