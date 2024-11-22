from django.urls import include, path

from app.warehouse.urls import urlpatterns as service_urlpatterns

urlpatterns = [
    path("", include(service_urlpatterns))
]
