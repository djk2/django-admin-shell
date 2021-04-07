
import django

# for django >= 3.1
if django.VERSION[:3] >= (3, 1):
    from django.urls import re_path, include

# for django < 3.1
else:
    from django.conf.urls import include, url as re_path


from django.contrib import admin


urlpatterns = [
    re_path(r'^admin/shell/', include('django_admin_shell.urls')),
    re_path(r'^admin/', admin.site.urls),
]
