# encoding: utf-8
import mock
from django.test import TestCase
from django_admin_shell.views import Importer
from django_admin_shell.tests.models import TestModel


class ImporterTest(TestCase):

    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO", False)
    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_MODELS", False)
    def test_autoimport_disable(self):
        imp = Importer()
        assert imp.get_modules() == {}
        assert imp.get_scope() == {}

    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO", True)
    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_MODELS", False)
    @mock.patch(
        "django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO_MODULES",
        {
            'django.conf': ['settings', 'non_exist_attr'],
            'non_exist_mod': ['foo_bar_baz'],
        }
    )
    def test_autoimport_django(self):
        from django.conf import settings
        imp = Importer()
        assert imp.get_modules() == {'django.conf': ['settings']}
        assert imp.get_scope() == {'settings': settings}

    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO", False)
    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_MODELS", True)
    def test_autoimport_models(self):
        imp = Importer()
        assert imp.get_modules()['django_admin_shell.tests.models'] == ['TestModel']
        assert issubclass(imp.get_scope()['TestModel'], TestModel)

    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO", True)
    @mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_MODELS", False)
    @mock.patch(
        "django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO_MODULES",
        {
            'django_admin_shell.views': ['Importer', 'Runner', 'ShellView', 'XYZ'],
            'non_exist_mod': ['foo_bar_baz'],
        }
    )
    def test_autoimport_str(self):
        imp = Importer()
        assert str(imp) == "from django_admin_shell.views import Importer, Runner, ShellView\n"
