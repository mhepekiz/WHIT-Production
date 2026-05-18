# WHIT System Documentation

Last updated: May 17, 2026
Repository documented: `mhepekiz/WHIT-Production`
Primary staging URL: `https://staging.whoishiringintech.com/`

This document is the practical operating guide for WHIT, also known as Who Is Hiring In Tech. It explains how the system is structured, how staging deploys, how the public homepage works, where admin settings live, and what commands are useful when maintaining the server.

## Quick Summary

WHIT is a full-stack web app for listing tech companies and jobs.

- Backend: Django 4.2, Django REST Framework, token/session auth, PostgreSQL in staging.
- Frontend: React 18, Vite, React Router.
- Staging server code path: `/var/www/whit`.
- Active staging deployment branch: `main` in `WHIT-Production`.
- Main public URL: `https://staging.whoishiringintech.com/`.
- API base URL in staging frontend builds: `https://staging.whoishiringintech.com/api`.
- Django admin: `https://staging.whoishiringintech.com/admin/`.

## Repositories And Branches

There are multiple local folders/repositories, so be careful before editing or pushing.

- `whit-release`: release/deployment repo for `mhepekiz/WHIT-Production`.
- `whit`: separate development repo for `mhepekiz/WHIT`.

For staging work, use `whit-release` unless there is a specific reason to work elsewhere.

The active GitHub Actions staging pipeline in `WHIT-Production` deploys from `main`, not `develop`. The `develop` branch may contain older workflow behavior and may not affect the live staging site.

Before working:

```bash
cd /Users/mustafahepekiz/Desktop/whit-release
git status --short --branch
git pull origin main
```

Do not commit unrelated local files such as `.DS_Store`.

## High-Level Architecture

The app has three main layers.

- Browser frontend served by Nginx from `/var/www/whit/frontend`.
- Django backend served by Gunicorn on localhost port `8003`.
- Nginx routes `/api/`, `/admin/`, `/static/`, and `/media/` to the backend/static directories, while normal page routes fall back to the React SPA.

Important paths:

```text
backend/                    Django project and apps
backend/whit/settings.py    Django settings
backend/companies/          Companies, settings, ad slots, homepage sections, sponsor logic
backend/accounts/           Job seeker auth/profile/preferences
backend/recruiters/         Recruiter auth, jobs, candidates, analytics
frontend/src/App.jsx        Frontend route definitions
frontend/src/pages/         Main React page screens
frontend/src/components/    Shared UI components
frontend/src/services/      API client helpers
nginx.conf                  Staging Nginx config copied during deploy
.github/workflows/deploy.yml Active staging deploy workflow
```

## Backend Overview

The backend is a Django project named `whit`.

Installed local apps:

- `companies`: company directory, function tags, work environments, ad slots, site settings, homepage sections, sponsor campaigns.
- `accounts`: normal user registration/login, profile, dashboard, job preferences.
- `recruiters`: recruiter registration/login, recruiter dashboard, jobs, candidates, applications, messages, analytics.

Core dependencies are listed in `backend/requirements.txt`:

- Django
- Django REST Framework
- django-cors-headers
- django-filter
- psycopg2-binary
- python-decouple
- gunicorn
- whitenoise
- Pillow

### Database Settings

Django chooses database type from environment variables in `backend/whit/settings.py`.

Important variables:

```text
DEBUG
SECRET_KEY
ALLOWED_HOSTS
DATABASE_ENGINE
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
DATABASE_HOST
DATABASE_PORT
CORS_ALLOWED_ORIGINS
STATIC_URL
MEDIA_URL
```

If `DATABASE_ENGINE=postgresql`, Django uses PostgreSQL. Otherwise it falls back to SQLite.

### Authentication

Django REST Framework uses both token authentication and session authentication.

Default API permission is authenticated, but some viewsets override this. For example, company list/retrieve endpoints are public at the API layer, while the frontend decides which full pages require login.

### Main API Routes

All of these are under `/api/` on staging.

Company app routes:

```text
/api/companies/
/api/companies/{id}/
/api/companies/filters/
/api/companies/stats/
/api/companies/sponsored/impression/
/api/companies/sponsored/click/
/api/functions/
/api/work-environments/
/api/ad-slots/
/api/site-settings/
/api/form-layouts/
/api/homepage-sections/
/api/debug-status/
```

Account routes:

```text
/api/accounts/register/
/api/accounts/login/
/api/accounts/dashboard/
/api/accounts/profile/
/api/accounts/job-preferences/
```

Recruiter routes:

```text
/api/recruiters/register/
/api/recruiters/login/
/api/recruiters/packages/
/api/recruiters/profile/
/api/recruiters/jobs/
/api/recruiters/job-board/
/api/recruiters/applications/
/api/recruiters/candidates/
/api/recruiters/messages/
/api/recruiters/dashboard/
/api/recruiters/export/{company_id}/
```

## Frontend Overview

The frontend is a React/Vite app in `frontend/`.

Useful commands:

```bash
cd frontend
npm install
npm run dev
npm run build
npm run lint
npm run preview
```

The active route map is in `frontend/src/App.jsx`.

Public pages:

```text
/                  Homepage company preview
/register          Job seeker registration
/login             Job seeker login
/recruiter/register
/recruiter/login
```

Protected job seeker pages:

```text
/all-companies
/jobs
/jobs/:id
/add-company
/dashboard
/dashboard/profile
/dashboard/preferences
/dashboard/resume
```

Protected recruiter pages:

```text
/recruiter/dashboard
/recruiter/dashboard/profile
/recruiter/dashboard/jobs
/recruiter/dashboard/jobs/new
/recruiter/dashboard/jobs/:id/edit
/recruiter/dashboard/analytics
/recruiter/dashboard/candidates
/recruiter/dashboard/applications
/recruiter/dashboard/messages
```

## Homepage Behavior

The homepage is intentionally public. Visitors can see a limited preview before logging in.

Current behavior:

- The homepage loads a random company sample.
- The number of displayed companies follows the admin Site Settings value `Companies per page`; if unavailable, it falls back to `Homepage companies`, then `10`.
- The frontend requests page `1`, sends `page_size` equal to the configured homepage count, and sends `ordering=?` for random ordering.
- The frontend still hard-caps the rendered list to the configured count so sponsored/extra API results cannot cause more than the intended number to appear.
- A fade overlay appears at the end of the preview list.
- The `SHOW ALL COMPANIES` button links to `/all-companies`, which requires login.

Files involved:

```text
frontend/src/pages/CompanyList.jsx
frontend/src/pages/CompanyList.css
frontend/src/App.jsx
backend/companies/views.py
backend/companies/models.py
```

The backend supports random ordering in `CompanyViewSet.list()` by checking `ordering=?` and applying `order_by('?')` to organic companies.

## Admin Settings

Site-wide settings are stored in the singleton `SiteSettings` model in `backend/companies/models.py`.

Important fields:

```text
jobs_per_page          Jobs shown per page on jobs listing pages
companies_per_page     Companies shown per page and currently used for homepage preview count
homepage_companies     Legacy/homepage-specific count fallback
companies_per_group    Company grouping between ad slots
homepage_sort_order    Stored setting, but homepage currently forces random selection
label_size             Size of function/work-environment labels
```

In Django admin, go to:

```text
/admin/companies/sitesettings/1/change/
```

For the public homepage preview, set `Companies per page` to `10` if the desired homepage count is 10.

## Superadmin / Admin User Maintenance

On the server, always activate the backend virtual environment before running Django commands. If `python` is not found or Django cannot be imported, use `python3` and activate `venv` first.

```bash
cd /var/www/whit/backend
source venv/bin/activate
python manage.py shell
```

List current superusers:

```bash
cd /var/www/whit/backend
source venv/bin/activate
python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); print(list(User.objects.filter(is_superuser=True).values('id','username','email','is_active')))"
```

Reset an existing superuser username/email/password:

```bash
cd /var/www/whit/backend
source venv/bin/activate
python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); u=User.objects.get(username='OLD_USERNAME'); u.username='NEW_USERNAME'; u.email='admin@example.com'; u.is_staff=True; u.is_superuser=True; u.is_active=True; u.set_password('NEW_STRONG_PASSWORD'); u.save(); print('updated', u.id, u.username)"
```

Create a new superuser interactively:

```bash
cd /var/www/whit/backend
source venv/bin/activate
python manage.py createsuperuser
```

Never commit real passwords or secrets to the repository.

## Staging Deployment

The active staging workflow is `.github/workflows/deploy.yml`.

It runs on pushes and pull requests to `main`. For pushes to `main`, it performs:

1. Backend tests against PostgreSQL 15.
2. Frontend install, test command, and build.
3. Docker image build and push to GitHub Container Registry.
4. SSH deployment to the staging server.
5. Health check for frontend and API.

During deployment, the workflow SSHes into the server and uses this path:

```bash
cd /var/www/whit
```

It then fetches and resets server code to `origin/main`:

```bash
sudo -u www-data git fetch origin main
sudo -u www-data git reset --hard origin/main
```

Then it:

- Activates `backend/venv`.
- Installs backend requirements.
- Runs migrations.
- Runs `collectstatic`.
- Attempts analytics population.
- Rebuilds the frontend with `VITE_API_URL=https://staging.whoishiringintech.com/api`.
- Copies `frontend/dist` to `/var/www/whit/frontend`.
- Copies `nginx.conf` into `/etc/nginx/sites-available/staging.whoishiringintech.com`.
- Restarts `whit` systemd service.
- Reloads Nginx.

To deploy a normal code change to staging:

```bash
cd /Users/mustafahepekiz/Desktop/whit-release
git status --short --branch
git add path/to/changed/files
git commit -m "Describe the change"
git push origin main
```

Then watch GitHub Actions for the staging deploy.

## Server Runtime

Nginx serves and proxies staging:

- `/` serves the React build from `/var/www/whit/frontend`.
- SPA fallback uses `/index.html`.
- `/api/` proxies to `http://127.0.0.1:8003`.
- `/admin/` proxies to `http://127.0.0.1:8003`.
- `/static/` aliases `/var/www/whit/backend/staticfiles/`.
- `/media/` aliases `/var/www/whit/backend/media/`.

Useful service commands on the server:

```bash
sudo systemctl status whit
sudo systemctl restart whit
sudo systemctl reload nginx
sudo nginx -t
```

Useful log commands:

```bash
sudo journalctl -u whit -n 100 --no-pager
sudo tail -n 100 /var/log/nginx/staging.whoishiringintech.com.error.log
sudo tail -n 100 /var/log/nginx/staging.whoishiringintech.com.access.log
```

## Local Development

Backend local setup:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Frontend local setup:

```bash
cd frontend
npm install
npm run dev
```

Common local URLs:

```text
Frontend: http://localhost:5173/
Backend:  http://localhost:8000/
Admin:    http://localhost:8000/admin/
API:      http://localhost:8000/api/
```

## Testing And Verification

Backend tests:

```bash
cd backend
source venv/bin/activate
python manage.py test
```

Frontend build:

```bash
cd frontend
npm run build
```

Frontend lint:

```bash
cd frontend
npm run lint
```

Staging health checks:

```bash
curl -f https://staging.whoishiringintech.com/
curl -f https://staging.whoishiringintech.com/api/companies/
```

Known current build warnings as of this document:

- Vite reports that `NODE_ENV=production` in `.env` is not supported by Vite for production builds.
- `frontend/src/pages/CompanyBrowse.jsx` contains a JSX comment typo around `Show ad slot after second group`.
- CSS minification reports a malformed `border-radius` declaration and a nearby unexpected brace in existing CSS.
- The frontend bundle is slightly above the default 500 kB chunk warning threshold.

These warnings did not block `npm run build` during the latest homepage changes, but they are good cleanup candidates.

## Common Maintenance Tasks

### Change Homepage Preview Count

1. Open Django admin.
2. Go to Site Settings.
3. Set `Companies per page` to the desired preview count, for example `10`.
4. Save.
5. Refresh the homepage.

### Confirm Homepage Random API Behavior

Use the API with random ordering and a page size:

```bash
curl "https://staging.whoishiringintech.com/api/companies/?page=1&page_size=10&ordering=?"
```

Refresh the command to see whether the company order changes.

### Add Or Edit Companies

Use Django admin under Companies, or use the frontend add-company flow if appropriate.

Important fields:

- Name
- Logo
- Jobs page URL
- Reviews URL
- Location
- Work environment
- Function tags
- Status
- Sponsored flag/order

### Add Or Edit Function Tags

Use Django admin under Functions. Each function has:

- Name
- Background color
- Text color

### Manage Ad Slots

Use Django admin under Ad Slots. Slots can be code-based or image-banner-based. The model supports desktop/mobile images, link URL, alt text, active state, and new-tab behavior.

### Reset Staging After A Bad Deploy

Usually the safest fix is another commit to `main` and another push. The deploy workflow resets the server to `origin/main`.

If manual server repair is needed:

```bash
cd /var/www/whit
sudo -u www-data git fetch origin main
sudo -u www-data git reset --hard origin/main
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
sudo systemctl restart whit
sudo nginx -t
sudo systemctl reload nginx
```

Be careful with `git reset --hard`: it deletes uncommitted server-side changes.

## Troubleshooting

### `python: command not found`

Use `python3`, or activate the virtual environment first:

```bash
cd /var/www/whit/backend
source venv/bin/activate
python --version
```

### `ModuleNotFoundError: No module named 'django'`

The virtual environment is not active, or dependencies are missing.

```bash
cd /var/www/whit/backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py check
```

### Homepage Shows Too Many Companies

Check these places:

- Django admin Site Settings: `Companies per page` should be the intended count.
- `frontend/src/pages/CompanyList.jsx`: homepage should request `page_size` equal to the configured count and slice rendered companies to that count.
- Browser cache/CDN cache: hard refresh after deploy.
- Confirm the deployed branch is `WHIT-Production/main`.

### Homepage Requires Login

Check `frontend/src/App.jsx`.

`/` should render `CompanyList` without `ProtectedRoute`. `/all-companies` should be inside `ProtectedRoute`.

### API Works But Frontend Does Not

Check:

```bash
curl -f https://staging.whoishiringintech.com/api/companies/
curl -f https://staging.whoishiringintech.com/
sudo nginx -t
sudo systemctl status whit
```

Also inspect frontend built files for the API URL if needed:

```bash
grep -R "VITE_API_URL\|whoishiringintech" /var/www/whit/frontend/assets || true
```

### Admin Static Or Media Files Missing

Run:

```bash
cd /var/www/whit/backend
source venv/bin/activate
python manage.py collectstatic --noinput --clear
sudo systemctl reload nginx
```

## Safe Git Practices

Before committing:

```bash
git status --short
git diff -- path/to/file
```

Stage only intended files:

```bash
git add frontend/src/pages/CompanyList.jsx frontend/src/pages/CompanyList.css
```

Avoid committing machine files:

```text
.DS_Store
backend/.env
local database dumps
venv directories
node_modules
```

## Recent Relevant Changes

May 17, 2026:

- Homepage made public while `/all-companies` requires login.
- Homepage preview changed to show only the configured number of companies.
- Homepage company selection changed to random ordering.
- Fade effect restored at the end of the capped homepage preview.
- Changes were pushed to `WHIT-Production/main`, which is the active staging deployment branch.

Relevant commits:

```text
ba1b735 Limit homepage companies to random preview
57a9e67 Restore homepage preview fade
```

## Future Cleanup Ideas

These are not required for normal operation, but would make the codebase healthier:

- Fix the JSX comment typo in `CompanyBrowse.jsx`.
- Fix the malformed CSS warning around `border-radius`.
- Decide whether `homepage_companies` or `companies_per_page` should be the single source of truth for homepage count, then update admin labels accordingly.
- Split large frontend bundles with dynamic imports.
- Add focused tests for guest homepage preview, authenticated all-company access, and homepage count capping.
- Remove duplicate/legacy docs or consolidate them behind this document.
