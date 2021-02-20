from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class usersprofile(models.Model):
    user = models.OneToOneField(User,
                                primary_key=True,
                                on_delete=models.CASCADE)
    cluster=models.IntegerField(null=True)
    skills = models.TextField(max_length=200, default="")
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projectname = models.CharField(max_length=200)
    contents = models.TextField()

    def __str__(self):
        return self.projectname

class ContactForm(models.Model):
    FirstName = models.TextField(max_length=200)
    LastName = models.TextField(max_length=200)
    Email = models.EmailField(max_length=200)
    Message = models.TextField(max_length=300)

    def __str__(self):
        return self.Email+"-"+self.FirstName
    class Meta:
        db_table = "contact"
