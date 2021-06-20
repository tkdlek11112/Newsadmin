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


class RealNewsManager(models.Manager):
    def create_news(self, title, tokens, target):
        real_news = self.create(title=title, tokens=tokens, target=target)
        return real_news


class RealNews(models.Model):
    date = models.DateField(default=now)
    time = models.TimeField(default=now)
    title = models.TextField(default='')
    tokens = models.TextField(default='')
    target = models.IntegerField(default=0)

    objects = RealNewsManager()


class LearnLogManager(models.Manager):
    def create_learnlog(self):
        llog = self.create()
        llog.save()
        return llog.pk

    def update_learnlog(self, pk):
        llog = LearnLog.objects.get(pk=pk)
        llog.learn_status = 'S'
        llog.save()
        return llog

    def update_apply(self,pk):
        llogs = LearnLog.objects.all()
        llogs.update(apply_status='N')

        llog = LearnLog.objects.get(pk=pk)
        llog.apply_status = 'Y'
        llog.apply_date = now()
        llog.apply_time = now()
        llog.save()
        return llog


class LearnLog(models.Model):
    learn_date = models.DateField(default=now)
    learn_time = models.TimeField(default=now)
    learn_status = models.CharField(default='P', max_length=1)
    apply_date = models.DateField(default=now)
    apply_time = models.TimeField(default=now)
    apply_status = models.CharField(default='N', max_length=1)
    objects = LearnLogManager()
