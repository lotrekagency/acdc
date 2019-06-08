from rest_framework import routers

from .views import ActiveCampaignViewSet

router = routers.SimpleRouter()
router.register(r'deepdata', ActiveCampaignViewSet, basename='deepdata')

urlpatterns = router.urls
