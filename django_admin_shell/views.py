# encoding: utf-8
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
except:
    # For python 3
    from io import StringIO

from .settings import (
    ADMIN_SHELL_SESSION_KEY,
    ADMIN_SHELL_OUTPUT_SIZE,
    ADMIN_SHELL_ENABLE,
    ADMIN_SHELL_ONLY_DEBUG_MODE,
    ADMIN_SHELL_ONLY_FOR_SUPERUSER,
)

import django
import sys
import traceback


def run_code(code):
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
        exec(code)
    except:
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


class Shell(FormView):

    template_name = "django_admin_shell/shell.html"
    form_class = ShellForm
    success_url = "."

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
            return HttpResponseForbidden("Forbidden: To access Django admin shell you must have access the admin site")
        elif ADMIN_SHELL_ONLY_DEBUG_MODE and settings.DEBUG is False:
            return HttpResponseForbidden("Forbidden :Django admin shell require DEBUG mode")
        elif ADMIN_SHELL_ONLY_FOR_SUPERUSER and request.user.is_superuser is False:
            return HttpResponseForbidden("Forbidden: To access Django admin shell you must be superuser")
        return super(Shell, self).dispatch(request, *args, **kwargs)

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

    def get(self, request, *args, **kwargs):
        # Clear output history - set empty list and save
        if request.GET.get("clear_history", "no") == "yes":
            self.clear_output()
        return super(Shell, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        code = form.cleaned_data.get("code", "")
        if len(code.strip()) > 0:
            result = run_code(code)
            self.add_to_outout(result)
            self.save_output()
        return super(Shell, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """Add output to context"""
        ctx = super(Shell, self).get_context_data(**kwargs)
        ctx['site_header'] = "Djang admin shell"
        ctx['has_permission'] = True
        ctx['output'] = self.get_output()
        ctx['python_version'] = get_py_version()
        return ctx
