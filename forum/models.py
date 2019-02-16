from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    title = models.CharField(max_length=80)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now_add=True)
    last_poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='last_poster')

    def __str__(self):
        return self.title

class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(blank=True, null=True)
    father = models.ForeignKey("self", on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return self.text
