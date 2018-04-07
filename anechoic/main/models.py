from django.db import models

# Create your models here.
class Position(models.Model):
     statement = models.CharField(max_length=100, label="Stated Position")
     description = models.TextField(max_length=1000, label="Description of position")
     link = models.URLField(label="More information")

     def __str__(self):
         return "Position: \"{}\"".format(self.statement)

class Argument(models.Model):
    link = models.URLField(label="Link to Argument")
    title = models.CharField(max_length=100, label="Title of argument")
    description = models.TextField(max_length=1000, label="Description of argument")
    rating = models.FloatField(label="Rating of argument")
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return "Argument: \"{}\"".format(self.title)
