from django.conf import settings


def from_settings_or_default(name, default):
    """Get attribute from settings by name or return default value"""
    return getattr(settings, name, default)


ADMIN_SHELL_ENABLE = from_settings_or_default('ADMIN_SHELL_ENABLE', True)
ADMIN_SHELL_ONLY_DEBUG_MODE = from_settings_or_default('ADMIN_SHELL_ONLY_DEBUG_MODE', True)
ADMIN_SHELL_ONLY_FOR_SUPERUSER = from_settings_or_default('ADMIN_SHELL_ONLY_FOR_SUPERUSER', True)
ADMIN_SHELL_OUTPUT_SIZE = from_settings_or_default('ADMIN_SHELL_OUTPUT_SIZE', 250)
ADMIN_SHELL_SESSION_KEY = from_settings_or_default('ADMIN_SHELL_SESSION_KEY', 'django_admin_shell_output')
