from django.db import models

# Create your models here.

class Search(models.Model):
    """docstring for Search."""
    search= models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    # need to use PostgreeSQL from ArrayField to work
    #ten_movies = models.ArrayField(with json)

    def __str__(self):
        return '{}'.format(self.search)

    class Meta:
        verbose_name_plural= "Searches"  # specifies the plural
