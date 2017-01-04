from django.db import models

from django.contrib.auth import models as auth_models

class QuestionManager(models.Manager):
    def new(self):
        return all().order_by('-added_at')

    def popular(self):
        return all().order_by('-rating')

class Question(models.Model):
    objects = QuestionManager()

    title = models.CharField(max_length=140)
    text = models.TextField()
    added_at = models.DateField()
    rating = models.IntegerField()
    author = models.ForeignKey(auth_models.User)
    likes = models.ManyToManyField(auth_models.User)

class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateField()
    question = models.ForeignKey(Question)
    author = models.ForeignKey(auth_models.User)

