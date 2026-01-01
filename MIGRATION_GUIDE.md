# Migration Guide: .gitpod.yml to Dev Container

This guide explains how to migrate from Gitpod Classic (`.gitpod.yml`) to Dev Container configuration for Ona.

## Overview

**Before (Gitpod Classic):**
- Configuration in `.gitpod.yml`
- Uses pre-built workspace images
- Tasks defined in YAML format

**After (Dev Container):**
- Configuration in `.devcontainer/devcontainer.json`
- Custom Dockerfile for environment setup
- Lifecycle hooks for automation

## Configuration Mapping

### 1. Image Configuration

**Gitpod Classic:**
```yaml
image: axonasif/workspace-python@sha256:f5ba627a31505ea6cf100abe8e552d7ff9e0abd6ba46745b6d6dab349c001430
```

**Dev Container:**
```json
{
  "build": {
    "context": ".",
    "dockerfile": "Dockerfile"
  }
}
```

**Dockerfile:**
```dockerfile
FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv
```

### 2. Task Automation

**Gitpod Classic:**
```yaml
tasks:
  - name: Init project and run server
    init: |
      pip install Django
      django-admin startproject mysite .
    command: |
      python manage.py runserver
```

**Dev Container:**
```json
{
  "postCreateCommand": "pip install Django",
  "postStartCommand": "bash .devcontainer/init-django.sh"
}
```

### 3. Port Configuration

**Gitpod Classic:**
```yaml
ports:
  - port: 8000
    onOpen: open-preview
```

**Dev Container:**
```json
{
  "forwardPorts": [8000],
  "portsAttributes": {
    "8000": {
      "label": "Django Dev Server",
      "onAutoForward": "openPreview"
    }
  }
}
```

### 4. VS Code Extensions

**Gitpod Classic:**
```yaml
vscode:
  extensions:
    - ms-python.python
```

**Dev Container:**
```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
      ]
    }
  }
}
```

## Lifecycle Hooks Comparison

| Gitpod Classic | Dev Container | Purpose |
|----------------|---------------|---------|
| `init` | `postCreateCommand` | Run once after container creation |
| `before` | `initializeCommand` | Run before container starts (on host) |
| `command` | `postStartCommand` | Run every time container starts |
| N/A | `postAttachCommand` | Run when attaching to container |

## Key Differences

### Environment Variables

**Gitpod Classic:**
- `GITPOD_WORKSPACE_URL` automatically available
- `gp` CLI tool pre-installed

**Dev Container:**
- Same environment variables available in Ona
- `gp` CLI tool available in Ona environments

### ALLOWED_HOSTS Configuration

Both approaches use the same logic to configure Django's `ALLOWED_HOSTS`:

```python
if __import__('os').environ.get('GITPOD_WORKSPACE_URL'):
    try:
        gp = __import__('subprocess').run(["gp", "url", "8000"], capture_output=True, text=True)
        if gp.returncode == 0 and gp.stdout:
            ALLOWED_HOSTS += [gp.stdout.strip().split('//', 1)[-1]]
    except:
        ALLOWED_HOSTS += ['*']
```

## Migration Steps

1. **Create `.devcontainer/` directory**
   ```bash
   mkdir -p .devcontainer
   ```

2. **Create Dockerfile**
   - Install Python and system dependencies
   - Set up Python symlinks if needed

3. **Create devcontainer.json**
   - Map tasks to lifecycle hooks
   - Configure ports and extensions
   - Add automation commands

4. **Create initialization scripts**
   - Extract complex logic from YAML to shell scripts
   - Make scripts executable

5. **Test the configuration**
   - Rebuild the Dev Container
   - Verify all automation runs correctly
   - Check that ports are forwarded

6. **Optional: Keep .gitpod.yml**
   - For backward compatibility
   - Or remove once migration is complete

## Running Django Server

**Gitpod Classic:**
- Automatically starts via `command` in tasks

**Dev Container:**
- Use `postStartCommand` for auto-start, or
- Manually run: `python manage.py runserver`
- Or use Ona Automations (services)

## Advantages of Dev Container

- Standard format (works in VS Code, GitHub Codespaces, Ona)
- More control over environment setup
- Better separation of concerns (Dockerfile vs config)
- Supports features from containers.dev

## Next Steps

After migration:
1. Test the Dev Container thoroughly
2. Update documentation
3. Consider using Ona Automations for services
4. Remove `.gitpod.yml` if no longer needed
