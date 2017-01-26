from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from .views import Shell

app_name = 'django_admin_shell'

urlpatterns = [
    url(r'^$',  staff_member_required(Shell.as_view()), name="shell"),
]
