from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet, OrderViewSet, CategoryViewSet, ManagerGroupView, DeliveryCrewGroupView, CartViewSet

router = DefaultRouter()
router.register(r'menu-items', MenuItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'cart/menu-items', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('groups/manager/users/', ManagerGroupView.as_view()),
    path('groups/delivery-crew/users/', DeliveryCrewGroupView.as_view()),
]
