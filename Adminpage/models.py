from django.db import models
from django.utils.timezone import now


# Create your models here.

class LearnNewsManager(models.Manager):
    def create_news(self, date, time, title, tokens, target):
        learn_news = self.create(date=date, time=time, title=title, tokens=tokens, target=target)
        return learn_news


class LearnNews(models.Model):
    date = models.DateField(default=now)
    time = models.TimeField(default=now)
    title = models.TextField(default='')
    tokens = models.TextField(default='')
    target = models.IntegerField(default=0)

    objects = LearnNewsManager()
