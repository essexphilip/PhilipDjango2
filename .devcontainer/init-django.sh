#!/bin/bash

# Init Django project
name="mysite"
if test ! -e "${name}"; then
    django-admin startproject "${name}" .
fi

# Modify settings.py to include Gitpod/Ona port hosts
settings="${name}/settings.py"
if test -e "${settings}" && ! grep -q 'GITPOD_WORKSPACE_URL' "${settings}" 2>/dev/null; then
    cat >> "${settings}" << 'SCRIPT'

if __import__('os').environ.get('GITPOD_WORKSPACE_URL'):
    try:
        gp = __import__('subprocess').run(["gp", "url", "8000"], capture_output=True, text=True)
        if gp.returncode == 0 and gp.stdout:
            ALLOWED_HOSTS += [gp.stdout.strip().split('//', 1)[-1]]
    except:
        ALLOWED_HOSTS += ['*']

SCRIPT
fi

# Install requirements if they exist
if test -e requirements.txt; then
    pip install -r requirements.txt
fi

# Run migrations
python manage.py migrate

echo ""
echo "Django environment ready!"
echo "Run: python manage.py runserver"
echo ""
