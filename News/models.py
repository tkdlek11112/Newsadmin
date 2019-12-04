from django.db import models
from django.utils.timezone import now

# Create your models here.
class NewsManager(models.Manager):
    def create_news(self, date, time, title, tokens, target):
        real_news = self.create(date=date, time=time, title=title, tokens=tokens, target=target)
        return real_news


class News(models.Model):
    date = models.DateField(default=now)
    time = models.TimeField(default=now)
    title = models.TextField(default='')
    tokens = models.TextField(default='')
    target = models.IntegerField(default=0)

    objects = NewsManager()


class UserDic(models.Model):
    word = models.CharField(max_length=20)

class StopWord(models.Model):
    word = models.CharField(max_length=20)


