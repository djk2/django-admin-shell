from django.conf import settings


def from_settings_or_default(name, default):
    """Get attribute from settings by name or return default value"""
    return getattr(settings, name, default)


DEFAULT_IMPORT = {
    'django.db.models': [
        'Avg',
        'Case',
        'Count',
        'F',
        'Max',
        'Min',
        'Prefetch',
        'Q',
        'Sum',
        'When',
    ],
    'django.conf': [
        'settings',
    ],
    'django.core.cache': [
        'cache',
    ],
    'django.contrib.auth': [
        'get_user_model',
    ],
    'django.utils': [
        'timezone',
    ],
    'django.urls': [
        'reverse'
    ],
}

ADMIN_SHELL_ENABLE = from_settings_or_default(
    'ADMIN_SHELL_ENABLE',
    True
)
ADMIN_SHELL_ONLY_DEBUG_MODE = from_settings_or_default(
    'ADMIN_SHELL_ONLY_DEBUG_MODE',
    True
)
ADMIN_SHELL_ONLY_FOR_SUPERUSER = from_settings_or_default(
    'ADMIN_SHELL_ONLY_FOR_SUPERUSER',
    True
)
ADMIN_SHELL_OUTPUT_SIZE = from_settings_or_default(
    'ADMIN_SHELL_OUTPUT_SIZE',
    250
)
ADMIN_SHELL_SESSION_KEY = from_settings_or_default(
    'ADMIN_SHELL_SESSION_KEY',
    'django_admin_shell_output'
)
ADMIN_SHELL_IMPORT_DJANGO = from_settings_or_default(
    'ADMIN_SHELL_IMPORT_DJANGO',
    True
)
ADMIN_SHELL_IMPORT_DJANGO_MODULES = from_settings_or_default(
    'ADMIN_SHELL_IMPORT_DJANGO_MODULES',
    DEFAULT_IMPORT
)
ADMIN_SHELL_IMPORT_MODELS = from_settings_or_default(
    'ADMIN_SHELL_IMPORT_MODELS',
    True
)
ADMIN_SHELL_CLEAR_SCOPE_ON_CLEAR_HISTORY = from_settings_or_default(
    'ADMIN_SHELL_CLEAR_SCOPE_ON_CLEAR_HISTORY',
    False
)
