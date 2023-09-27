# django
from django.urls import path
from django.urls import include

# rest_framework
from rest_framework.routers import DefaultRouter

# views
from .views import OrderViewSet
from .views import PassengerView


router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
    path("orders/<int:order_number>/<uuid:passenger_id>/", PassengerView.as_view({'get': 'retrieve', 'patch': 'update'}), name='passenger-detail'),
]