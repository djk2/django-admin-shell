# encoding: utf-8
from django.test.utils import override_settings
from django.test import (
    TestCase,
    Client,
)

import django

if django.VERSION < (1, 10):
    from django.core.urlresolvers import reverse
else:
    from django.urls.base import reverse


class BVTest(TestCase):

    client = None

    def setUp(self):
        self.client = Client()


class ShellViewStatusTest(BVTest):

    url = reverse("django_admin_shell:shell")

    @override_settings(ADMIN_SHELL_ENABLE=False)
    def test_shell_is_disable(self):
        response = self.client.get(self.url)
        status = response.status_code
        print(status, "XXXXXXXX")
        assert status == 404
