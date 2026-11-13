# The Little Vlog

A Django vlog-sharing app for **PGR211**.
It provides public browsing, search, staff sign-in, and staff-managed content,
with a new vlog collection and complete create/read/update/delete workflows.

## Run locally

From the repository root, with Python 3.12+ and [uv](https://docs.astral.sh/uv/) installed,
install the dependencies:

```sh
uv sync
```

Then run Django commands from the `django_project/` directory. For example:

```sh
cd django_project
uv run python manage.py migrate
uv run python manage.py runserver
```

### Activating the virtual environment (optional)

You can use `uv run` for each Django command, as shown above, without manually
activating the environment. Alternatively, activate it from the repository root,
then change to `django_project/` and use `python manage.py ...` directly.

**macOS/Linux:**

```sh
source .venv/bin/activate
cd django_project
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
cd django_project
```

**Windows (Command Prompt):**

```cmd
.venv\Scripts\activate.bat
cd django_project
```

Open **http://127.0.0.1:8000/**. If port 8000 is occupied, use
`uv run python manage.py runserver 8001` from `django_project/`
(or `python manage.py runserver 8001` with the environment activated).

The SQLite database is local and is not committed to the repository. When setting up
the project locally, apply the migrations and create a staff administrator account:

```sh
# Run from django_project/
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

Use **Staff sign in** on the home page, then **Share a vlog**. A title, valid HTTP(S)
video URL, description of at least 20 characters, and category are required. Tags
are optional. The signed-in staff member is automatically recorded as the author.
Open a vlog's detail page to watch its linked video, edit it, or confirm deletion.
Videos open on their original provider; this application stores links, not uploads.

## Features and routes

| Page                                          | URL                   | Access                                                        |
| --------------------------------------------- | --------------------- | ------------------------------------------------------------- |
| Searchable, category-filtered, paginated list | `/`                   | Public                                                        |
| Vlog detail and video link                    | `/vlogs/<id>/`        | Public                                                        |
| Publish vlog                                  | `/vlogs/new/`         | Staff                                                         |
| Edit vlog                                     | `/vlogs/<id>/edit/`   | Staff                                                         |
| Confirm/delete vlog                           | `/vlogs/<id>/delete/` | Staff                                                         |
| Administration                                | `/admin/`             | Staff with model permissions; superusers have all permissions |

Staff are trusted collection editors and can manage all
posts through the public-facing forms. Regular accounts cannot publish/edit/delete.
GET on the delete page only displays confirmation; deletion requires a CSRF-protected POST.
The newest publication appears first, with six posts per page.

## Project layout

`django_project/` contains `manage.py`, the `vlogsite/` Django project settings and
server entry points, and the `vlogs/` application (models, migrations, views, forms,
templates, static files, and admin configuration). The `pyproject.toml` and
`uv.lock` at the repository root define and lock the Python environment. Docker
files, if used, are kept separately in `docker/`.

## Verification

Run these from `django_project/`:

```sh
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py test
```

The test command uses Django's test runner. Deployment is outside the scope of these
local-development instructions.
