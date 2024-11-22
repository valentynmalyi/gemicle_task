from django.urls import path

from .views import WarehouseStrategyView

urlpatterns = [
    path("", WarehouseStrategyView.as_view())
]
