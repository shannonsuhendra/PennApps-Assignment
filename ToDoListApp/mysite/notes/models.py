from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

class Subject(models.Model):
    subject_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    count = models.IntegerField()
    def __str__(self):
        return self.subject_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class List(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    list_text = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(("Date"), default=date.today)
    def __str__(self):
        return self.list_text
    class Meta:
        ordering = ('due_date',)