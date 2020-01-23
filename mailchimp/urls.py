from rest_framework import routers

from .views import MailchimpViewSet

router = routers.SimpleRouter()
router.register(r'mailchimp', MailchimpViewSet, basename='mailchimp')

urlpatterns = router.urls