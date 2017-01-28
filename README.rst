django-admin-shell
------------------

.. image:: https://travis-ci.org/djk2/django-admin-shell.svg?branch=master
    :target: https://travis-ci.org/djk2/django-admin-shell

.. image:: https://requires.io/github/djk2/django-admin-shell/requirements.svg?branch=master
    :target: https://requires.io/github/djk2/django-admin-shell/requirements/?branch=master
    :alt: Requirements Status


Django application can execute python code in your project's environment on django admin site.
You can use similar as `python manage shell` without reloading the environment.


* Tested by tox with:
    - Python :2.7, 3.4
    - Django : 1.9, 1.10, 1.11, 2.0-dev

* Require:
    - Django >= 1.9

* Tested on browsers
    - OK - Firefox 50.1.0 - Ubuntu 14.04
    - OK - Firefox 31.1 - CentOS 6.4
    - OK - Chromium 53.0 - Ubuntu 14.04
    - OK - Microsoft Edge 38 - Windows 10
    - OK - Internet Explorer 11.0 - Windows 8.1
    - OK - Internet Explorer 10.0 - Windows 7
    - OK - Internet Explorer 9.0 - Windows 7
    - ERR - Internet Explorer 8.0 - Windows 7 (javascripts not working / console work properly)



Screens
-------
.. image:: https://raw.githubusercontent.com/djk2/django-admin-shell/master/doc/static/screen1.png
    :alt: Django admin shell view



Install
--------

1. Install::

    pip install django-admin-shell

    or

    pip install git+https://github.com/djk2/django-admin-shell.git

    or after download zip

    pip install django-admin-shell.zip


2. Add `django_admin_shell` to your INSTALLED_APPS setting

 *settings.py* ::

    INSTALLED_APPS = [
        ...
        'django_admin_shell',
        ...
    ]

3. Add the `django_admin_shell` urls to your root url patterns (above admin/) :

 *urls.py* ::

    urlpatterns = [
        url(r'^admin/shell/', include('django_admin_shell.urls')),
        ...
        url(r'^admin/', admin.site.urls),
    ]


Usage
------
* shell is available on url: **/admin/shell**
* On default settings user must be authenticated to django admin site and
  User must have superuser permission and DEBUG mode must be set on True.

.. note::

  Make sure that in your project session is enable

  More about session and how enabling session read here :
  https://docs.djangoproject.com/en/dev/topics/http/sessions/

  Usualy default session in django project is enable

Settings
---------

ADMIN_SHELL_ENABLE
^^^^^^^^^^^^^^^^^^^
*type* : **bool**

*default* : **True**

If shell is enable or disable. When application is disable then url: /admin/shell return Http404 Not found


ADMIN_SHELL_ONLY_DEBUG_MODE
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
*type* : **bool**

*default* : **True**

If flag is set on True, then shell is available only in DEBUG mode.

If debug mode is required and debug mode is disabled then url: /admin/shell will return Http 403 Forbidden

ADMIN_SHELL_ONLY_FOR_SUPERUSER
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
*type* : **bool**

*default* : **True**

If flag is set on True, then shell is available only for user with superuser permission.

If superuser is required and user not have permission then url: /admin/shell will return Http 403 Forbidden

ADMIN_SHELL_OUTPUT_SIZE
^^^^^^^^^^^^^^^^^^^^^^^^
*type* : **integer**

*default* : **250**

Flag determines how many outputs can be remember.



ADMIN_SHELL_SESSION_KEY
^^^^^^^^^^^^^^^^^^^^^^^^
*type* : **string**

*default* : **django_admin_shell_output**

Name for key in session where is stored history last executed codes.


Code examples
-------------

* show django settings::

    from django.conf import settings

    for key in dir(settings):
        val = getattr(settings, key, None)
        print(key, "=", val)


* run command in operating system and take output::

    import os

    os.system('date > /tmp/admin_console.tmp')
    os.system('echo ------- >> /tmp/admin_console.tmp')
    os.system('who >> /tmp/admin_console.tmp')
    os.system('echo ------- >> /tmp/admin_console.tmp')
    os.system('ps aux | grep python >> /tmp/admin_console.tmp')

    with open('/tmp/admin_console.tmp', 'r') as f:
        print(f.read())


* run big python code (get python source from website)::

    import requests

    req = requests.get('http://foo.bar.com/example.py')
    if req.status_code == 200:
        code = req.text
        print(code, '\n------------\n')
        exec(code)


Useful for me:
---------------
* https://docs.djangoproject.com/
* https://jquery.com/
* http://alan.blog-city.com/jquerylinedtextarea.htm

Similar projects:
-----------------
* https://github.com/onrik/django-webshell
