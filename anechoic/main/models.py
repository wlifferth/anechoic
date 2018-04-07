from django.db import models

# Create your models here.
class Position(models.Model):
     statement = models.CharField(max_length=100, verbose_name="Stated Position")
     description = models.TextField(max_length=1000, verbose_name="Description of position")
     link = models.URLField(verbose_name="More information")

     def __str__(self):
         return "Position: \"{}\"".format(self.statement)

class Argument(models.Model):
    link = models.URLField(verbose_name="Link to Argument")
    title = models.CharField(max_length=100, verbose_name="Title of argument")
    description = models.TextField(max_length=1000, verbose_name="Description of argument")
    rating = models.FloatField(verbose_name="Rating of argument")
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return "Argument: \"{}\"".format(self.title)
