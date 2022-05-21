from rest_framework import routers

from song.views import SongViewSet, RatingViewSet

app_name = 'song'
router = routers.DefaultRouter()

router.register(prefix='song', viewset=SongViewSet, basename='song')
router.register(prefix='rating', viewset=RatingViewSet, basename='rating')

urlpatterns = router.urls
