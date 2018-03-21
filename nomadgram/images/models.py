from django.db import models
from nomadgram.users import models as user_models

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Image(TimeStampModel):

    """ Image Model """

    file = models.ImageField()
    location = models.CharField(max_length=140)
    caption = models.TextField()
    creator = models.ForeignKey(user_models.User, null=True)

class Comment(TimeStampModel):

    """ Comment Model """

    message = models.TextField()
    creator = models.ForeignKey(user_models.User, null=True)
    image = models.ForeignKey(Image, null=True)

class Like(TimeStampModel):

    """ Like Model """

    creator = models.ForeignKey(user_models.User, null=True)
    image = models.ForeignKey(Image, null=True)
