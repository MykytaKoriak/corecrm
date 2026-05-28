from django.contrib.auth.models import User
from rest_framework import serializers

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


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "is_active"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    contacts = ContactPersonSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = "__all__"


class DealStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealStage
        fields = "__all__"


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ["recipient", "read_at", "created_at"]


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = "__all__"


class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = "__all__"


class IntegrationPlaceholderSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationPlaceholder
        fields = "__all__"
