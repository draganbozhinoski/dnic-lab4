from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class CustomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    biography = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username


class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=50)
    fajlovi = models.FileField(upload_to='images/')
    date_created = models.DateField()
    last_modified = models.DateField()

    def __str__(self):
        return self.title


class Blocked(models.Model):
    user_blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_blocker', null=True, blank=True)
    user_blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_blocked', null=True, blank=True)


class BlogPostComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    sodrzhina = models.CharField(max_length=250)

    def __str__(self):
        return self.sodrzhina
