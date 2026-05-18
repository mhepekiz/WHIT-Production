"""Settings helpers for environment values and Google Cloud Secret Manager."""

import logging
import os
from functools import lru_cache

from decouple import config

logger = logging.getLogger(__name__)

_TRUE_VALUES = {'1', 'true', 'yes', 'on'}


def _env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in _TRUE_VALUES


def _cast_value(value, cast):
    if cast is bool:
        return str(value).strip().lower() in _TRUE_VALUES
    return cast(value)


GCP_SECRET_MANAGER_ENABLED = config('GCP_SECRET_MANAGER_ENABLED', default=False, cast=bool)
GCP_PROJECT_ID = config('GCP_PROJECT_ID', default=os.environ.get('GOOGLE_CLOUD_PROJECT'))
GCP_SECRET_NAME_PREFIX = config('GCP_SECRET_NAME_PREFIX', default='').strip()
GCP_SECRET_VERSION = config('GCP_SECRET_VERSION', default='latest')
GOOGLE_APPLICATION_CREDENTIALS = config('GOOGLE_APPLICATION_CREDENTIALS', default='')
if GOOGLE_APPLICATION_CREDENTIALS:
    os.environ.setdefault('GOOGLE_APPLICATION_CREDENTIALS', GOOGLE_APPLICATION_CREDENTIALS)


@lru_cache(maxsize=1)
def _secret_manager_client():
    if not GCP_SECRET_MANAGER_ENABLED:
        return None

    if not GCP_PROJECT_ID:
        raise RuntimeError('GCP_SECRET_MANAGER_ENABLED is true, but GCP_PROJECT_ID is not set.')

    try:
        from google.cloud import secretmanager
    except ImportError as exc:
        raise RuntimeError(
            'GCP Secret Manager is enabled, but google-cloud-secret-manager is not installed.'
        ) from exc

    return secretmanager.SecretManagerServiceClient()


def _secret_id(name):
    return f'{GCP_SECRET_NAME_PREFIX}{name}' if GCP_SECRET_NAME_PREFIX else name


@lru_cache(maxsize=128)
def get_gcp_secret(name, default=None):
    """Return a secret value from GCP Secret Manager, or default when disabled/missing."""
    secret_id = _secret_id(name)

    try:
        client = _secret_manager_client()
        if client is None:
            return default

        resource_name = f'projects/{GCP_PROJECT_ID}/secrets/{secret_id}/versions/{GCP_SECRET_VERSION}'
        response = client.access_secret_version(request={'name': resource_name})
        return response.payload.data.decode('utf-8')
    except Exception as exc:
        if default is not None:
            logger.warning('Unable to read GCP secret %s; using fallback value.', secret_id)
            return default
        raise RuntimeError(f'Unable to read required GCP secret {secret_id}') from exc


def setting(name, default=None, cast=None, secret=False):
    """Read a setting from GCP Secret Manager when requested, otherwise from env/.env.

    Environment variables still override Secret Manager to make emergency server fixes and
    local development straightforward.
    """
    env_value = os.environ.get(name)
    if env_value is not None:
        return config(name, default=default, cast=cast) if cast else env_value

    if secret and GCP_SECRET_MANAGER_ENABLED:
        value = get_gcp_secret(name, default=default)
        if cast and value is not None:
            return _cast_value(value, cast)
        return value

    return config(name, default=default, cast=cast) if cast else config(name, default=default)


def setting_list(name, default=''):
    value = setting(name, default=default)
    if not value:
        return []
    return [item.strip() for item in str(value).split(',') if item.strip()]
