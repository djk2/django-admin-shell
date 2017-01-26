django-admin-shell
------------------

Django/Python shell in django admin site. You can use as ./manage shell without reloading the environment.


Project not finish yet.
===========================

* Application work correctly but not have setup / tests / docs
* This documentation is only temporary and was very quickly created


- Django : 1.9, 1.10
- Python 3.x
- Not full tested yet


Install
--------

1. Install::

    pip install git+https://github.com/djk2/django-admin-shell.git


2. Add `django_admin_shell` to your INSTALLED_APPS setting::

    INSTALLED_APPS = [
        ...,
        'django_admin_shell',
        ...,
    ]

3. Add the `django_admin_shell` urls to your root url patterns (above admin/) ::

    urlpatterns = [
        url(r'^admin/shell/', include('django_admin_shell.urls')),
        url(r'^admin/', admin.site.urls),
    ]


Run
----
* shell is available on url: /admin/shell

* On default setttings you must be authenticated to admin site
* You must have superuser permission
* DEBUG must be set on True.
* Session on your app must be turn on.

..note:: You can change default settings modify settings using django_admin_shell/settigs.py as example



Useful for me:
---------------

* https://docs.djangoproject.com/
* https://jquery.com/
* http://alan.blog-city.com/jquerylinedtextarea.htm
