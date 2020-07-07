from django.db import models

# Create your models here.


class Search(models.Model):
    """docstring for Search."""
    search = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    # need to use PostgreeSQL from ArrayField to work
    # ten_movies = models.ArrayField(with json)

    def __str__(self):
        return '{}'.format(self.search)

    class Meta:
        verbose_name_plural = "Searches"  # specifies the plural


class Movies(models.Model):
    id = models.IntegerField(
        primary_key=True, serialize=False, verbose_name="ID")
    title = models.CharField(max_length=100)
    genres = models.CharField(max_length=100)
    release_date = models.DateField()
    overview = models.TextField()
    popularity = models.IntegerField(verbose_name="popularities")
    vote_count = models.IntegerField()
    poster_path = models.CharField(max_length=400)
    vote_average = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        verbose_name_plural = "Movies"  # specifies the plural
