# CHANGELOG for django-admin-shell

## 2.0.1 (2023-11-20)

    * Add missing `bootstrap.min.css.map` file - refer to issue #8

## 2.0.0 (2023-05-10)

    * Support for Django 4.0 and Django 4.2
    * Tests for Python 3.10
    * Replaced test via tox from Python 3.6 to 3.7
    * Verified support for latest webbrowsers
    * Drop support for Django 1.10 and 1.11
    * Drop support for Python 2.7

## 1.1.0 (2022-07-02)

    * Added flag `ADMIN_SHELL_CLEAR_SCOPE_ON_CLEAR_HISTORY` to
      to enable the gargabe collector on the declared variables
      from the shell (author: Rodrigo Castro - rodrigondec)

## 1.0.0 (2021-06-10)

    * Auto import of models and Django tools (like shell_plus).
      More details in `README.rst` in section about `ADMIN_SHELL_IMPORT_DJANGO` and
     `ADMIN_SHELL_IMPORT_MODELS` settings - refer to issue #1
    * Support for Django 3.1 and Django 3.2
    * Tests for Python 3.8
    * Django" instead of "Djang" in titlebar - refer to issue #2
    * Drop support for Django 1.9
    * Remove integration with Travis

## 0.1.2 (2020-06-08)

    * Added MANIFEST.in - Issue #2

## 0.1.1 (2020-02-03)

    * Added support for python 3.6
    * Added support  Django 3.0
    * Verified support for latest webbrowsers

## 0.1 (2016-12-27)

    * Initial version
