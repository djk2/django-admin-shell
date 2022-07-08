import django

# for django >= 3.1
if django.VERSION[:3] >= (3, 1):
    from django.urls import re_path

# for django < 3.1
else:
    from django.conf.urls import url as re_path


from django.contrib.admin.views.decorators import staff_member_required
from .views import ShellView

app_name = 'django_admin_shell'

urlpatterns = [
    re_path(r'^$', staff_member_required(ShellView.as_view()), name="shell"),
]
