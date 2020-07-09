from rest_framework import routers

from .api import MoviesViewSet


from movies.models import Movies
from .serializers import MoviesSerializer

router = routers.DefaultRouter()
router.register('api/Movies', MoviesViewSet, 'Movies')

urlpatterns = router.urls
