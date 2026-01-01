# Django Dev Container Setup

This document explains the Dev Container configuration for Django development in Ona.

## Files Created/Modified

### 1. `.devcontainer/Dockerfile`
Installs Python 3, pip, and venv on Ubuntu 24.04 base image.

### 2. `.devcontainer/devcontainer.json`
Configures the development environment with:
- Python package installation (Django)
- Django project initialization
- Port forwarding (8000)
- VS Code extensions (Python, Pylance)

### 3. `.devcontainer/init-django.sh`
Automation script that:
- Creates Django project named "mysite"
- Configures ALLOWED_HOSTS for Ona/Gitpod URLs
- Installs requirements.txt if present
- Runs database migrations

## How It Works

### Container Lifecycle

1. **Build** - Dockerfile installs Python and dependencies
2. **postCreateCommand** - Runs once after container creation
   - Upgrades pip, wheel, setuptools
   - Installs Django
3. **postStartCommand** - Runs every time container starts
   - Executes init-django.sh
   - Creates Django project if needed
   - Configures settings
   - Runs migrations

### Port Configuration

Port 8000 is automatically forwarded and opens in preview mode when Django server starts.

### ALLOWED_HOSTS Configuration

The init script automatically configures Django's ALLOWED_HOSTS to work with Ona's dynamic URLs:

```python
if __import__('os').environ.get('GITPOD_WORKSPACE_URL'):
    try:
        gp = __import__('subprocess').run(["gp", "url", "8000"], capture_output=True, text=True)
        if gp.returncode == 0 and gp.stdout:
            ALLOWED_HOSTS += [gp.stdout.strip().split('//', 1)[-1]]
    except:
        ALLOWED_HOSTS += ['*']
```

## Usage

### First Time Setup

When you open this project in Ona:
1. Dev Container builds automatically
2. Django is installed
3. Project "mysite" is created
4. Migrations run automatically

### Starting the Django Server

```bash
python manage.py runserver
```

Or use Ona Automations to create a service.

### Creating Django Apps

```bash
python manage.py startapp myapp
```

### Running Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating Superuser

```bash
python manage.py createsuperuser
```

## Customization

### Installing Additional Packages

**Option 1: Add to Dockerfile**
```dockerfile
RUN apt-get install -y postgresql-client
```

**Option 2: Create requirements.txt**
```
Django>=4.2
psycopg2-binary
djangorestframework
```

The init script automatically installs from requirements.txt.

### Changing Project Name

Edit `.devcontainer/init-django.sh`:
```bash
name="myproject"  # Change from "mysite"
```

### Adding VS Code Extensions

Edit `.devcontainer/devcontainer.json`:
```json
"customizations": {
  "vscode": {
    "extensions": [
      "ms-python.python",
      "ms-python.vscode-pylance",
      "ms-python.black-formatter"
    ]
  }
}
```

## Rebuilding the Container

If you modify Dockerfile or devcontainer.json:

1. Use Command Palette: "Dev Containers: Rebuild Container"
2. Or use Ona CLI: `gitpod environment devcontainer rebuild`

## Troubleshooting

### Python not found
- Rebuild the container to ensure Dockerfile changes are applied

### Django not installed
- Check postCreateCommand ran successfully
- Manually run: `pip install Django`

### Port 8000 not accessible
- Ensure Django server is running
- Check port forwarding in devcontainer.json
- Verify ALLOWED_HOSTS configuration

### Migrations fail
- Check database configuration in settings.py
- Default SQLite should work out of the box

## Next Steps

1. Start developing your Django application
2. Add apps with `python manage.py startapp`
3. Configure database settings if needed
4. Set up static files and media handling
5. Add authentication and authorization
6. Create API endpoints or views

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Dev Container Specification](https://containers.dev/)
- [Ona Documentation](https://www.gitpod.io/docs)
