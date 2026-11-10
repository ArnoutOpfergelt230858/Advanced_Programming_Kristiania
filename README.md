# The Little Vlog

A Django vlog-sharing app for **PGR211**.
It provides public browsing, search, staff sign-in, and staff-managed content,
with a new vlog collection and complete create/read/update/delete workflows.

## Run locally

From this directory, with Python 3.12+ and [uv](https://docs.astral.sh/uv/) installed:

```powershell
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

Open **http://127.0.0.1:8000/**. If port 8000 is occupied, use
`uv run python manage.py runserver 8001`.

Existing accounts in this copy's SQLite database still work. For a fresh database,
create an administrator:

```powershell
uv run python manage.py createsuperuser
```

Use **Staff sign in** on the home page, then **Share a vlog**. A title, valid HTTP(S)
video URL, description of at least 20 characters, and category are required. Tags
are optional. The signed-in staff member is automatically recorded as the author.
Open a vlog's detail page to watch its linked video, edit it, or confirm deletion.
Videos open on their original provider; this application stores links, not uploads.

## Features and routes

| Page | URL | Access |
| --- | --- | --- |
| Searchable, category-filtered, paginated list | `/` | Public |
| Vlog detail and video link | `/vlogs/<id>/` | Public |
| Publish vlog | `/vlogs/new/` | Staff |
| Edit vlog | `/vlogs/<id>/edit/` | Staff |
| Confirm/delete vlog | `/vlogs/<id>/delete/` | Staff |
| Administration | `/admin/` | Staff with model permissions; superusers have all permissions |

Staff are trusted collection editors and can manage all
posts through the public-facing forms. Regular accounts cannot publish/edit/delete.
GET on the delete page only displays confirmation; deletion requires a CSRF-protected POST.
The newest publication appears first, with six posts per page.

## Project layout

`vlogsite/` contains the Django project settings and server entry points.
`vlogs/` contains the application models, migrations, views, forms, templates,
static files, admin configuration, and tests. Vlogs are stored in the `VlogPost`
table in the local SQLite database; existing login accounts remain usable.

## Verification

```powershell
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py test
```

Tests use a temporary database and cover public browsing/search, pagination,
staff-only CRUD, author assignment, validation, safe deletion, CSRF, escaped
content, missing records, and admin operations.

See [REPORT.md](REPORT.md) for the architecture, course concepts, requirement map,
and manual evidence checklist. Deployment is outside the requested scope; the
settings and instructions here target local development.

## Source submission

Include `manage.py`, `vlogsite/`, `vlogs/` (including migrations, templates and static
files), `src/`, `pyproject.toml`,
`uv.lock`, `.python-version`, and the documentation in your source ZIP. Exclude
`.venv/`, `.git/`, `__pycache__/`, local secrets, and personal database files.
Extract the ZIP into a separate directory and run the setup/check commands above
before submission. Add your own screenshots and review the technical explanation.
