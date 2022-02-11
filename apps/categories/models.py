from django.db import models
from apps.core.models import TimeStampedAbstractModel
from django.template.defaultfilters import slugify


class Category(TimeStampedAbstractModel):
    name = models.CharField(max_length=125)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
