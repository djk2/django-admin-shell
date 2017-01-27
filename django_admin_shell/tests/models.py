from django.db import models


class TestModel(models.Model):
    """Model only for tests"""
    foo = models.CharField(max_length=32)

    class Meta:
        verbose_name = "Test Model"
