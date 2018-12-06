from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.text import slugify
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    headline = models.CharField(blank=True, max_length=100)
    slug = models.SlugField(null = True, blank = True)
    bio = models.TextField(blank=True)
    imt = models.ImageField(upload_to="profile_img")
    join_date = models.DateTimeField(blank=True, default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' %(self.user)

def createProfile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user = kwargs['instance'])

post_save.connect(createProfile, sender = User)
