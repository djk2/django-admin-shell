from django.conf.urls import (
    url,
    include,
)
from django.contrib import admin


urlpatterns = [
    url(r'^admin/shell/', include('django_admin_shell.urls')),
    url(r'^admin/', admin.site.urls),
]
