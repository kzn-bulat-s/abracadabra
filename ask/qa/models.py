from django.db import models

from django.contrib.auth import models as auth_models

class QuestionManager(models.Manager):
    def new(self):
        return self.all().order_by('-pk')

    def popular(self):
        return self.all().order_by('-rating')

class Question(models.Model):
    objects = QuestionManager()

    title = models.CharField(max_length=140)
    text = models.TextField()
    added_at = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(auth_models.User, null=True)
    likes = models.ManyToManyField(auth_models.User, related_name='question_likes')

class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateField(auto_now_add=True)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(auth_models.User, null=True)

