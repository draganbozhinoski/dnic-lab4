from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class CustomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    biography = models.TextField()
    city = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    profile_photo = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.user.username


class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=50)
    fajlovi = models.FileField(upload_to='files/')
    date_created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Blocked(models.Model):
    user_blocker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_blocker', null=True, blank=True)
    user_blocked = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_blocked', null=True, blank=True)


class BlogPostComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    sodrzhina = models.CharField(max_length=250)
    comment_writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.sodrzhina
