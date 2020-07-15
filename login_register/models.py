from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class usersprofile(models.Model):
    user = models.OneToOneField(User,
                                primary_key=True,
                                on_delete=models.CASCADE)

    skills = models.TextField(max_length=200, default="python")
    interests = models.TextField(max_length=200, default="", null=True)
    aboutme = models.TextField(max_length=300, default="")
    fblink = models.URLField(max_length=128, default="facebook.com")
    gitlink = models.URLField(max_length=128, default="github.com")
    avatar = models.ImageField(default="avatar.jpg",
                               upload_to="profile_pictures")

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        super(usersprofile, self).save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)


class projects(models.Model):
    projectname = models.CharField(max_length=50)

    def __str__(self):
        return self.projectname
