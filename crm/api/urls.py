from rest_framework.routers import DefaultRouter

from .viewsets import (
    ActivityLogViewSet,
    BotLeadViewSet,
    CallLogViewSet,
    ClientFileViewSet,
    ClientViewSet,
    ContactPersonViewSet,
    CustomFieldViewSet,
    DealItemViewSet,
    DealStageViewSet,
    DealViewSet,
    DocumentTemplateViewSet,
    InboxMessageViewSet,
    IntegrationPlaceholderViewSet,
    NotificationViewSet,
    OrderFileViewSet,
    OrderItemViewSet,
    OrderViewSet,
    ProductViewSet,
    ProfileViewSet,
    ShipmentViewSet,
    TaskViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("profiles", ProfileViewSet)
router.register("clients", ClientViewSet)
router.register("client-files", ClientFileViewSet)
router.register("contacts", ContactPersonViewSet)
router.register("deal-stages", DealStageViewSet)
router.register("deals", DealViewSet)
router.register("deal-items", DealItemViewSet)
router.register("products", ProductViewSet)
router.register("orders", OrderViewSet)
router.register("order-items", OrderItemViewSet)
router.register("order-files", OrderFileViewSet)
router.register("shipments", ShipmentViewSet)
router.register("tasks", TaskViewSet)
router.register("notifications", NotificationViewSet, basename="notifications")
router.register("activity", ActivityLogViewSet)
router.register("custom-fields", CustomFieldViewSet)
router.register("integrations", IntegrationPlaceholderViewSet)
router.register("inbox", InboxMessageViewSet)
router.register("bot-leads", BotLeadViewSet)
router.register("calls", CallLogViewSet)
router.register("document-templates", DocumentTemplateViewSet)

urlpatterns = router.urls
