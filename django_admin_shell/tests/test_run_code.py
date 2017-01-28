# encoding: utf-8
import django
from django.test import TestCase
from django_admin_shell.views import run_code
from django_admin_shell.tests.models import TestModel


class RunCodeTest(TestCase):

    def test_single_code(self):
        """
        Run simple code in pure python
        """
        code = "1 + 1"
        result = run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == ""

        code = "print(1 + 1)"
        result = run_code(code)
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

        result = run_code(code)
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
        result = run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == "False\n"

        with self.settings(DEBUG=True):
            result = run_code(code)
            assert result["code"] == code
            assert result["status"] == "success"
            assert result["out"] == "True\n"

        code = "from django.conf import settings\n"
        code += "print(settings.SECRET_KEY)"

        result = run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == "{0}\n".format("x" * 55)

        code = "import django\n"
        code += "print(django.VERSION)"
        result = run_code(code)
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

        result = run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == "0\n"

        code = "from django_admin_shell.tests.models import TestModel \n"
        code += "test_model1 = TestModel(foo='bar') \n"
        code += "test_model1.save() \n"
        code += "test_model2 = TestModel(foo='bas') \n"
        code += "test_model2.save() \n"
        code += "print(TestModel.objects.count())"

        result = run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == "2\n"
        assert TestModel.objects.count() == 2

        code = "from django_admin_shell.tests.models import TestModel \n"
        code += "qs = TestModel.objects.filter(foo='bar') \n"
        code += "test_model = qs[0] \n"
        code += "print(test_model.foo) \n"
        code += "test_model.delete()"

        result = run_code(code)
        assert result["code"] == code
        assert result["status"] == "success"
        assert result["out"] == "bar\n"
        assert TestModel.objects.count() == 1

    def test_errors(self):
        """
        Testing incorect code
        """
        code = "a = 1 / 0"
        result = run_code(code)
        assert result["code"] == code
        assert result["status"] == "error"
        assert "ZeroDivisionError" in result["out"]

        code = "a = "
        result = run_code(code)
        assert result["code"] == code
        assert result["status"] == "error"
        assert "SyntaxError" in result["out"]

        code = " a = 1"
        result = run_code(code)
        assert result["code"] == code
        assert result["status"] == "error"
        assert "IndentationError" in result["out"]

        code = "raise ValueError"
        result = run_code(code)
        assert result["code"] == code
        assert result["status"] == "error"
        assert "ValueError" in result["out"]
