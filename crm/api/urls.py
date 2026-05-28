from rest_framework.routers import DefaultRouter

from .viewsets import (
    ActivityLogViewSet,
    ClientViewSet,
    ContactPersonViewSet,
    CustomFieldViewSet,
    DealStageViewSet,
    DealViewSet,
    IntegrationPlaceholderViewSet,
    NotificationViewSet,
    OrderItemViewSet,
    OrderViewSet,
    ProductViewSet,
    ProfileViewSet,
    TaskViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("profiles", ProfileViewSet)
router.register("clients", ClientViewSet)
router.register("contacts", ContactPersonViewSet)
router.register("deal-stages", DealStageViewSet)
router.register("deals", DealViewSet)
router.register("products", ProductViewSet)
router.register("orders", OrderViewSet)
router.register("order-items", OrderItemViewSet)
router.register("tasks", TaskViewSet)
router.register("notifications", NotificationViewSet, basename="notifications")
router.register("activity", ActivityLogViewSet)
router.register("custom-fields", CustomFieldViewSet)
router.register("integrations", IntegrationPlaceholderViewSet)

urlpatterns = router.urls
