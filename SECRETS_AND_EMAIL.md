# Secrets And Email Setup

This guide explains how WHIT reads production secrets from Google Cloud Secret Manager and sends system emails through Brevo SMTP.

## Runtime Behavior

Django settings now use `backend/whit/secrets.py`.

Resolution order:

1. Environment variable, including values from `/var/www/whit/backend/.env`.
2. Google Cloud Secret Manager, when `GCP_SECRET_MANAGER_ENABLED=True` and the setting is marked as a secret.
3. Local default value.

This keeps local development simple while allowing staging/production secrets to live in GCP.

## Bootstrap Environment Variables

The server still needs a few non-secret bootstrap values in `/var/www/whit/backend/.env` or the `whit.service` environment:

```bash
DEBUG=False
GCP_SECRET_MANAGER_ENABLED=True
GCP_PROJECT_ID=your-gcp-project-id
GCP_SECRET_NAME_PREFIX=WHIT_
GCP_SECRET_VERSION=latest
GOOGLE_APPLICATION_CREDENTIALS=/var/www/whit/secrets/gcp-secret-manager.json
```

`GCP_SECRET_NAME_PREFIX` is optional. If set to `WHIT_`, Django reads `SECRET_KEY` from the GCP secret named `WHIT_SECRET_KEY`.

Environment variables override GCP secrets. That is intentional for emergency fixes, but production should keep actual secret values in GCP, not in `.env`.

## Recommended GCP Secrets

Create these secrets in Google Cloud Secret Manager. If you use `GCP_SECRET_NAME_PREFIX=WHIT_`, create them with the `WHIT_` prefix.

```text
SECRET_KEY
DATABASE_ENGINE
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
DATABASE_HOST
DATABASE_PORT
EMAIL_HOST
EMAIL_PORT
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL
SERVER_EMAIL
```

Optional config values that can remain in `.env` because they are not secrets:

```text
DEBUG
ALLOWED_HOSTS
CORS_ALLOWED_ORIGINS
STATIC_URL
MEDIA_URL
EMAIL_USE_TLS
EMAIL_USE_SSL
```

## Create Secrets With gcloud

Example using a `WHIT_` prefix:

```bash
gcloud secrets create WHIT_SECRET_KEY --replication-policy=automatic
echo -n 'replace-with-django-secret-key' | gcloud secrets versions add WHIT_SECRET_KEY --data-file=-

gcloud secrets create WHIT_DATABASE_PASSWORD --replication-policy=automatic
echo -n 'replace-with-db-password' | gcloud secrets versions add WHIT_DATABASE_PASSWORD --data-file=-

gcloud secrets create WHIT_EMAIL_HOST_PASSWORD --replication-policy=automatic
echo -n 'replace-with-brevo-smtp-key' | gcloud secrets versions add WHIT_EMAIL_HOST_PASSWORD --data-file=-
```

Repeat for the full list above.

## Service Account Permissions

The server must authenticate to GCP with a service account that can read secrets.

Grant this role to the service account:

```text
Secret Manager Secret Accessor
```

Then store the service account JSON on the server, outside the repository, for example:

```text
/var/www/whit/secrets/gcp-secret-manager.json
```

Set ownership/permissions tightly:

```bash
sudo mkdir -p /var/www/whit/secrets
sudo chown -R www-data:www-data /var/www/whit/secrets
sudo chmod 700 /var/www/whit/secrets
sudo chmod 600 /var/www/whit/secrets/gcp-secret-manager.json
```

## Brevo SMTP Settings

Django is configured for Brevo SMTP by default:

```text
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-relay.brevo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=<Brevo SMTP login>
EMAIL_HOST_PASSWORD=<Brevo SMTP key>
DEFAULT_FROM_EMAIL=WhoIsHiringInTech <noreply@whoishiringintech.com>
```

Use the SMTP login and SMTP key from Brevo SMTP/API settings. For port `587`, keep `EMAIL_USE_TLS=True`. If you choose Brevo port `465`, use SSL instead by setting `EMAIL_USE_TLS=False` and `EMAIL_USE_SSL=True`.

## Test Email

After deployment, test from the server:

```bash
cd /var/www/whit/backend
source venv/bin/activate
python manage.py send_test_email your@email.com
```

If it succeeds, Django prints:

```text
Test email sent to your@email.com
```

## Deployment Checklist

1. Create GCP secrets.
2. Grant the server service account `Secret Manager Secret Accessor`.
3. Put the service account JSON on the server outside the repo.
4. Set bootstrap values in `/var/www/whit/backend/.env`.
5. Deploy `main` so `google-cloud-secret-manager` installs.
6. Run `python manage.py check`.
7. Run `python manage.py send_test_email your@email.com`.
8. Remove secret values from `.env` after confirming GCP access works.
