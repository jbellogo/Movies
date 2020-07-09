from movies.models import Movies
from rest_framework import viewsets, permissions
from .serializers import MoviesSerializer

# Lead viewsets
# default router. registe endpoint


class MoviesViewSet(viewsets.ModelViewSet):
    queryset = Movies.objects.all()  # get all the leads
    permission_classes = {
        permissions.AllowAny
    }
    serializer_class = MoviesSerializer
