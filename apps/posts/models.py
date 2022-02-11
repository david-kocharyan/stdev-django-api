import os
import time
from django.db import models
from apps.core.models import TimeStampedAbstractModel
from apps.categories.models import Category
from apps.users.models import User


def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / uploads/ posts/ post_time
    upload_to = 'uploads/posts/'
    ext = filename.split('.')[-1]
    filename = 'post_{}.{}'.format(int(time.time()), ext)
    return os.path.join(upload_to, filename)


class Post(TimeStampedAbstractModel):
    title = models.CharField(verbose_name='Title', max_length=125)
    description = models.TextField(verbose_name='Description')
    image = models.ImageField(verbose_name="Image", upload_to=post_directory_path)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
