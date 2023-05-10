from django import VERSION
from django.contrib import admin

if VERSION[:3] >= (3, 1):
    from django.urls import include, re_path
else:
    from django.conf.urls import include, url as re_path


urlpatterns = [
    re_path(r'^admin/shell/', include('django_admin_shell.urls')),
    re_path(r'^admin/', admin.site.urls),
]
