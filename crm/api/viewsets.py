from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from crm.models import (
    ActivityLog,
    Client,
    ContactPerson,
    CustomField,
    Deal,
    DealStage,
    IntegrationPlaceholder,
    Notification,
    Order,
    OrderItem,
    Product,
    Profile,
    Task,
)

from .serializers import (
    ActivityLogSerializer,
    ClientSerializer,
    ContactPersonSerializer,
    CustomFieldSerializer,
    DealSerializer,
    DealStageSerializer,
    IntegrationPlaceholderSerializer,
    NotificationSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ProductSerializer,
    ProfileSerializer,
    TaskSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.select_related("profile").order_by("username")
    serializer_class = UserSerializer
    search_fields = ["username", "email", "first_name", "last_name"]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    filterset_fields = ["role"]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.select_related("owner").prefetch_related("contacts")
    serializer_class = ClientSerializer
    search_fields = ["name", "phone", "email", "telegram", "instagram", "notes"]
    filterset_fields = ["status", "client_type", "owner"]
    ordering_fields = ["created_at", "updated_at", "name"]


class ContactPersonViewSet(viewsets.ModelViewSet):
    queryset = ContactPerson.objects.select_related("client")
    serializer_class = ContactPersonSerializer
    search_fields = ["name", "phone", "email", "client__name"]
    filterset_fields = ["client", "is_primary"]


class DealStageViewSet(viewsets.ModelViewSet):
    queryset = DealStage.objects.all()
    serializer_class = DealStageSerializer
    search_fields = ["name"]


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.select_related("client", "stage", "owner")
    serializer_class = DealSerializer
    search_fields = ["title", "client__name", "source", "description"]
    filterset_fields = ["stage", "owner", "priority", "client"]
    ordering_fields = ["created_at", "updated_at", "amount", "expected_close_date"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ["name", "sku", "category"]
    filterset_fields = ["status", "category"]
    ordering_fields = ["name", "price", "stock", "updated_at"]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("client", "deal", "owner").prefetch_related("items")
    serializer_class = OrderSerializer
    search_fields = ["number", "client__name", "comments"]
    filterset_fields = ["payment_status", "delivery_status", "work_status", "owner"]
    ordering_fields = ["created_at", "updated_at", "total"]


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related("order", "product")
    serializer_class = OrderItemSerializer
    filterset_fields = ["order", "product"]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("assigned_to", "created_by", "client", "deal")
    serializer_class = TaskSerializer
    search_fields = ["title", "description", "client__name", "deal__title"]
    filterset_fields = ["status", "priority", "assigned_to", "client", "deal"]
    ordering_fields = ["deadline", "created_at", "updated_at"]


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.mark_read()
        return Response({"status": "ok"})


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.select_related("user", "content_type")
    serializer_class = ActivityLogSerializer
    search_fields = ["object_repr", "user__username"]
    filterset_fields = ["action", "content_type"]


class CustomFieldViewSet(viewsets.ModelViewSet):
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer
    filterset_fields = ["entity", "field_type", "is_active"]


class IntegrationPlaceholderViewSet(viewsets.ModelViewSet):
    queryset = IntegrationPlaceholder.objects.all()
    serializer_class = IntegrationPlaceholderSerializer
    filterset_fields = ["provider", "is_enabled"]
