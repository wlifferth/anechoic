from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Position(models.Model):
     statement = models.CharField(max_length=100, verbose_name="Stated Position")
     description = models.TextField(max_length=1000, verbose_name="Description of position")
     link = models.URLField(verbose_name="More information")

     def __str__(self):
         return "Position: \"{}\"".format(self.statement)

class Argument(models.Model):
    SIDE = [("For", "For"), ("Against", "Against")]
    link = models.URLField(verbose_name="Link to Argument")
    title = models.CharField(max_length=100, verbose_name="Title of argument")
    description = models.TextField(max_length=1000, verbose_name="Description of argument")
    rating = models.FloatField(verbose_name="Rating of argument")
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    side = models.CharField(max_length=10, verbose_name="Whether an argument is for or against a position", choices=SIDE, default="For")

    def __str__(self):
        return "Argument: \"{}\"".format(self.title)

class UserPosition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User that has this position")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name="Position this user has commented on")
    rating = models.IntegerField(verbose_name="This users level of agreement with the position")
