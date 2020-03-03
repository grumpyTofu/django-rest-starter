from rest_framework import routers

from django.urls import path
from api.views import DataFileView

# router = routers.DefaultRouter()
# router.register('api/data', DataFileViewset, 'data')
# # url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())

# urlpatterns = router.urls

urlpatterns = [
    path('', DataFileView.as_view())
]