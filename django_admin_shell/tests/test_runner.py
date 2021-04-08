# encoding: utf-8
import mock
import django
from django.test import TestCase
from django_admin_shell.views import Runner
from django_admin_shell.tests.models import TestModel


class RunnerTest(TestCase):

    def setUp(self):
        self.runner = Runner()

    def test_single_code(self):
        """
        Run simple code in pure python
        """
        code = "1 + 1"
        result = self.runner.run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == ""

        code = "print(1 + 1)"
        result = self.runner.run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == "2\n"

        # !!! Warning
        # Not use: """ because indention will be incorect
        code = "class Test(object):\n"
        code += "   def pow(self, a, b):\n"
        code += "       return a**b\n"
        code += "test = Test()\n"
        code += "ret = test.pow(2, 10)\n"
        code += "print(ret)"

        result = self.runner.run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == "1024\n"

    def test_interact_with_env(self):
        """
        Run code having access to something from environ, settings etc.
        Heck if code runing in django environ
        """

        code = "from django.conf import settings\n"
        code += "print(settings.DEBUG)"

        # Default in test DEBUG is False
        result = self.runner.run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == "False\n"

        with self.settings(DEBUG=True):
            result = self.runner.run_code(code)
            assert result["code"] == code
            assert result["status"] == "success"
            assert result["out"] == "True\n"

        code = "from django.conf import settings\n"
        code += "print(settings.SECRET_KEY)"

        result = self.runner.run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == "__secret__key__\n"

        code = "import django\n"
        code += "print(django.VERSION)"
        result = self.runner.run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == "{0}\n".format(str(django.VERSION))

    def test_interact_with_db(self):
        """
        Execute code modify django database
        Queries and operation on queryset
        """
        code = "from django_admin_shell.tests.models import TestModel \n"
        code += "print(TestModel.objects.count())"

        result = self.runner.run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == "0\n"

        code = "from django_admin_shell.tests.models import TestModel \n"
        code += "test_model1 = TestModel(foo='bar') \n"
        code += "test_model1.save() \n"
        code += "test_model2 = TestModel(foo='bas') \n"
        code += "test_model2.save() \n"
        code += "print(TestModel.objects.count())"

        result = self.runner.run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == "2\n"
        assert TestModel.objects.count() == 2

        code = "from django_admin_shell.tests.models import TestModel \n"
        code += "qs = TestModel.objects.filter(foo='bar') \n"
        code += "test_model = qs[0] \n"
        code += "print(test_model.foo) \n"
        code += "test_model.delete()"

        result = self.runner.run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == "bar\n"
        assert TestModel.objects.count() == 1

    def test_errors(self):
        """
        Testing incorect code
        """
        code = "a = 1 / 0"
        result = self.runner.run_code(code)
        assert result["code"] == code
        assert result["status"] == "error"
        assert "ZeroDivisionError" in result["out"]

        code = "a = "
        result = self.runner.run_code(code)
        assert result["code"] == code
        assert result["status"] == "error"
        assert "SyntaxError" in result["out"]

        code = " a = 1"
        result = self.runner.run_code(code)
        assert result["code"] == code
        assert result["status"] == "error"
        assert "IndentationError" in result["out"]

        code = "raise ValueError"
        result = self.runner.run_code(code)
        assert result["code"] == code
        assert result["status"] == "error"
        assert "ValueError" in result["out"]

    def test_runcode_with_autoimport_django(self):
        """
        If ADMIN_SHELL_IMPORT_DJANGO is True then we should have
        access to call "django.contrib.auth.get_user_model" directly.
        django.contrib.auth.get_user_model is one of autoimported function
        """
        code = "print(get_user_model().__name__)"

        with mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO", True):
            runner = Runner()
            result = runner.run_code(code)
            assert result["code"] == code
            assert result["status"] == "success"
            assert result["out"] == "User\n"

        with mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_DJANGO", False):
            runner = Runner()
            result = runner.run_code(code)
            assert result["code"] == code
            assert result["status"] == "error"
            assert "NameError: name 'get_user_model' is not defined" in result["out"]

    def test_runcode_with_autoimport_models(self):
        """
        If ADMIN_SHELL_IMPORT_MODELS is True then we should have
        access to call "django_admin_shell.tests.models.TestModel" directly.
        django.contrib.auth.get_user_model is one of autoimported function
        """
        TestModel(foo='foo').save()
        code = "print(TestModel.objects.count())"

        with mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_MODELS", True):
            runner = Runner()
            result = runner.run_code(code)
            assert result["code"] == code
            assert result["status"] == "success"
            assert result["out"] == "1\n"

        with mock.patch("django_admin_shell.views.ADMIN_SHELL_IMPORT_MODELS", False):
            runner = Runner()
            result = runner.run_code(code)
            assert result["code"] == code
            assert result["status"] == "error"
            assert "NameError: name 'TestModel' is not defined" in result["out"]
