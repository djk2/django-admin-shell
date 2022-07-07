# encoding: utf-8
from django.apps import apps
from django.views.generic import FormView
from .forms import ShellForm
from django.http import (
    HttpResponseForbidden,
    HttpResponseNotFound
)
from django.conf import settings

try:
    # Only for python 2
    from StringIO import StringIO
except ImportError:
    # For python 3
    from io import StringIO

from .settings import (
    ADMIN_SHELL_SESSION_KEY,
    ADMIN_SHELL_OUTPUT_SIZE,
    ADMIN_SHELL_ENABLE,
    ADMIN_SHELL_ONLY_DEBUG_MODE,
    ADMIN_SHELL_ONLY_FOR_SUPERUSER,
    ADMIN_SHELL_IMPORT_DJANGO,
    ADMIN_SHELL_IMPORT_DJANGO_MODULES,
    ADMIN_SHELL_IMPORT_MODELS,
    ADMIN_SHELL_CLEAR_SCOPE_ON_CLEAR_HISTORY
)

import django
import importlib
import sys
import traceback
import warnings


class Importer(object):

    def __init__(self, import_django=None, import_models=None, extra_imports=None):
        self.import_django = import_django or ADMIN_SHELL_IMPORT_DJANGO
        self.import_models = import_models or ADMIN_SHELL_IMPORT_MODELS
        self.FROM_DJANGO = ADMIN_SHELL_IMPORT_DJANGO_MODULES
        if extra_imports is not None and isinstance(extra_imports, dict):
            self.FROM_DJANGO.update(extra_imports)

    _mods = None

    def get_modules(self):
        """
        Return list of modules and symbols to import
        """
        if self._mods is None:
            self._mods = {}

            if self.import_django and self.FROM_DJANGO:

                for module_name, symbols in self.FROM_DJANGO.items():
                    try:
                        module = importlib.import_module(module_name)
                    except ImportError as e:
                        warnings.warn(
                            "django_admin_shell - autoimport warning :: {msg}".format(
                                msg=str(e)
                            ),
                            ImportWarning
                        )
                        continue

                    self._mods[module_name] = []
                    for symbol_name in symbols:
                        if hasattr(module, symbol_name):
                            self._mods[module_name].append(symbol_name)
                        else:
                            warnings.warn(
                                "django_admin_shell - autoimport warning :: "
                                "AttributeError module '{mod}' has no attribute '{attr}'".format(
                                    mod=module_name,
                                    attr=symbol_name
                                ),
                                ImportWarning
                            )

            if self.import_models:
                for model_class in apps.get_models():
                    _mod = model_class.__module__
                    classes = self._mods.get(_mod, [])
                    classes.append(model_class.__name__)
                    self._mods[_mod] = classes

        return self._mods

    _scope = None

    def get_scope(self):
        """
        Return map with symbols to module/object
        Like:
        "reverse" -> "django.urls.reverse"
        """
        if self._scope is None:
            self._scope = {}
            for module_name, symbols in self.get_modules().items():
                module = importlib.import_module(module_name)
                for symbol_name in symbols:
                    self._scope[symbol_name] = getattr(
                        module,
                        symbol_name
                    )

        return self._scope

    def clear_scope(self):
        """
        clear the scope.

        Freeing declared variables to be garbage collected.
        """
        self._scope = None

    def __str__(self):
        buf = ""
        for module, symbols in self.get_modules().items():
            if symbols:
                buf += "from {mod} import {symbols}\n".format(
                    mod=module,
                    symbols=", ".join(symbols)
                )
        return buf


class Runner(object):

    def __init__(self):
        self.importer = Importer()

    def run_code(self, code):
        """
        Execute code and return result with status = success|error
        Function manipulate stdout to grab output from exec
        """
        status = "success"
        out = ""
        tmp_stdout = sys.stdout
        buf = StringIO()

        try:
            sys.stdout = buf
            exec(code, None, self.importer.get_scope())
        except Exception:
            out = traceback.format_exc()
            status = 'error'
        else:
            out = buf.getvalue()
        finally:
            sys.stdout = tmp_stdout

        result = {
            'code': code,
            'out':  out,
            'status': status,
        }
        return result


def get_py_version():
    ver = sys.version_info
    return "{0}.{1}.{2}".format(ver.major, ver.minor, ver.micro)


def get_dj_version():
    return django.__version__


class ShellView(FormView):

    template_name = "django_admin_shell/shell.html"
    form_class = ShellForm
    success_url = "."
    runner = Runner()

    # Output - list ran code and results
    # store in session
    output = None

    def dispatch(self, request, *args, **kwargs):
        """Override to check settings"""
        if django.VERSION < (1, 10):
            is_auth = request.user.is_authenticated()
        else:
            is_auth = request.user.is_authenticated

        if not ADMIN_SHELL_ENABLE:
            return HttpResponseNotFound("Not found: Django admin shell is not enabled")
        elif is_auth is False or request.user.is_staff is False:
            return HttpResponseForbidden(
                "Forbidden: To access Django admin shell you must have access the admin site"
            )
        elif ADMIN_SHELL_ONLY_DEBUG_MODE and settings.DEBUG is False:
            return HttpResponseForbidden(
                "Forbidden :Django admin shell require DEBUG mode"
            )
        elif ADMIN_SHELL_ONLY_FOR_SUPERUSER and request.user.is_superuser is False:
            return HttpResponseForbidden(
                "Forbidden: To access Django admin shell you must be superuser"
            )
        return super(ShellView, self).dispatch(request, *args, **kwargs)

    def get_output(self):
        if self.output is None:
            output = self.request.session.get(ADMIN_SHELL_SESSION_KEY, [])
            self.output = output[:ADMIN_SHELL_OUTPUT_SIZE]
        return self.output

    def add_to_outout(self, item):
        output = self.get_output()
        output[:0] = [item]
        self.output = output
        return self.output

    def save_output(self):
        output = self.get_output()
        self.request.session[ADMIN_SHELL_SESSION_KEY] = output

    def clear_output(self):
        self.output = []
        self.save_output()
        if ADMIN_SHELL_CLEAR_SCOPE_ON_CLEAR_HISTORY:
            self.runner.importer.clear_scope()

    def get(self, request, *args, **kwargs):
        # Clear output history - set empty list and save
        if request.GET.get("clear_history", "no") == "yes":
            self.clear_output()
        return super(ShellView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        code = form.cleaned_data.get("code", "")
        if len(code.strip()) > 0:
            result = self.runner.run_code(code)
            self.add_to_outout(result)
            self.save_output()
        return super(ShellView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """Add output to context"""
        ctx = super(ShellView, self).get_context_data(**kwargs)
        ctx['site_header'] = "Django admin shell"
        ctx['has_permission'] = True
        ctx['output'] = self.get_output()
        ctx['python_version'] = get_py_version()
        ctx['django_version'] = get_dj_version()
        ctx['auto_import'] = str(self.runner.importer)
        return ctx
