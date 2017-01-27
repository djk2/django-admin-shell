# encoding: utf-8
import django
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from django.test import (
    TestCase,
    Client,
)

from django_admin_shell.settings import ADMIN_SHELL_SESSION_KEY
import mock

if django.VERSION < (1, 10):
    from django.core.urlresolvers import reverse
else:
    from django.urls.base import reverse


class ShellViewTest(TestCase):

    url = None
    user = None

    def setUp(self):

        self.url = reverse("django_admin_shell:shell")

        username = "test"
        password = "test"

        self.user = get_user_model()(username=username)
        self.user.set_password(password)
        self.user.save()

        self.client_auth = Client()
        self.client_auth.login(username=username, password=password)

    def test_shell_unauth(self):
        """If user isn't authenticated then should be redirect to login admin site"""
        client = Client()
        response = client.get(self.url)
        assert response.status_code == 302

    def test_shell_notstuff(self):
        """If user not is stuff then don"t have access to shell view"""
        response = self.client_auth.get(self.url)
        assert response.status_code == 302

    def test_shell_enable(self):
        """
        Test ADMIN_SHELL_ENABLE is True / False
        but, default shell is only for superuser.
        """
        self.user.is_staff = True
        self.user.save()

        # Default ADMIN_SHELL_ENABLE is True
        # but, default shell is only for superuser.
        response = self.client_auth.get(self.url)
        assert response.status_code == 403

        # Test settings.ADMIN_SHELL_ENABLE is False
        with mock.patch("django_admin_shell.views.ADMIN_SHELL_ENABLE", False):
            response = self.client_auth.get(self.url)
            assert response.status_code == 404

    @override_settings(DEBUG=True)
    def test_only_for_superuser(self):
        """
        Test ADMIN_SHELL_ONLY_FOR_SUPERUSER is True / False
        Default user must be superuser
        """
        self.user.is_staff = True
        self.user.save()

        # ADMIN_SHELL_ONLY_FOR_SUPERUSER = True
        # User.is_superuser = False
        response = self.client_auth.get(self.url)
        assert response.status_code == 403

        # ADMIN_SHELL_ONLY_FOR_SUPERUSER = False
        # User.is_superuser = False
        with mock.patch("django_admin_shell.views.ADMIN_SHELL_ONLY_FOR_SUPERUSER", False):
            response = self.client_auth.get(self.url)
            assert response.status_code == 200

        # ADMIN_SHELL_ONLY_FOR_SUPERUSER = True
        # User.is_superuser = True
        self.user.is_superuser = True
        self.user.save()
        response = self.client_auth.get(self.url)
        assert response.status_code == 200

    def test_only_debug_mode(self):
        """
        Test ADMIN_SHELL_ONLY_DEBUG_MODE is True / False
        Default user must be authenticated and is_stuff and superuser
        """
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

        # ADMIN_SHELL_ONLY_DEBUG_MODE = True
        # DEBUG = False
        response = self.client_auth.get(self.url)
        assert response.status_code == 403

        # ADMIN_SHELL_ONLY_DEBUG_MODE = True
        # DEBUG = True
        with self.settings(DEBUG=True):
            response = self.client_auth.get(self.url)
            assert response.status_code == 200

        # ADMIN_SHELL_ONLY_DEBUG_MODE = False
        # DEBUG = False
        with mock.patch("django_admin_shell.views.ADMIN_SHELL_ONLY_DEBUG_MODE", False):
            response = self.client_auth.get(self.url)
            assert response.status_code == 200

    @override_settings(DEBUG=True)
    def test_output(self):
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

        # First get on admin shell site
        response = self.client_auth.get(self.url)
        assert response.status_code == 200
        assert response.context["output"] == []
        assert ADMIN_SHELL_SESSION_KEY not in self.client_auth.session

        # Send simple code nothing to do
        code = "a = 1"
        response = self.client_auth.post(self.url, {"code": code})
        session = self.client_auth.session[ADMIN_SHELL_SESSION_KEY]
        assert response.status_code == 302
        assert len(session) == 1
        assert session[0]["code"] == code
        assert session[0]["status"] == "success"

        # get django admin shell site after run simple code
        response = self.client_auth.get(self.url)
        assert response.status_code == 200
        assert len(response.context["output"]) == 1
        result = response.context["output"][0]
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == ""

        # Send incorrect python code
        code = "1/0"
        response = self.client_auth.post(self.url, {"code": code})
        session = self.client_auth.session[ADMIN_SHELL_SESSION_KEY]
        assert response.status_code == 302
        assert len(session) == 2
        assert session[0]["code"] == code
        assert session[0]["status"] == "error"
        assert session[1]["status"] == "success"

        # get shell site after send incorrect code
        response = self.client_auth.get(self.url)
        assert response.status_code == 200
        assert len(response.context["output"]) == 2
        result = response.context["output"][0]
        assert result["code"] == code
        assert result["status"] == "error"
        assert "ZeroDivisionError" in result["out"]

        # Clear all outputs (run history)
        response = self.client_auth.get(self.url, {"clear_history": "yes"})
        assert response.status_code == 200
        assert response.context["output"] == []
        assert ADMIN_SHELL_SESSION_KEY in self.client_auth.session
        assert self.client_auth.session[ADMIN_SHELL_SESSION_KEY] == []
