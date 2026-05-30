from django.contrib import admin

from crm.models import (
    ActivityLog,
    BotLead,
    CallLog,
    Client,
    ClientFile,
    ContactPerson,
    CustomField,
    Deal,
    DealItem,
    DealStage,
    DocumentTemplate,
    InboxMessage,
    IntegrationPlaceholder,
    Notification,
    Order,
    OrderFile,
    OrderItem,
    Product,
    Profile,
    Shipment,
    Task,
)


class ContactPersonInline(admin.TabularInline):
    model = ContactPerson
    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class DealItemInline(admin.TabularInline):
    model = DealItem
    extra = 0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone", "position")
    list_filter = ("role",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "company_name", "primary_contact_name", "status", "client_type", "phone", "email", "owner", "updated_at")
    list_filter = ("status", "client_type", "owner")
    search_fields = ("name", "phone", "email", "telegram", "instagram")
    inlines = [ContactPersonInline]


@admin.register(ClientFile)
class ClientFileAdmin(admin.ModelAdmin):
    list_display = ("client", "title", "file", "uploaded_by", "uploaded_at")
    search_fields = ("client__name", "title", "comment")


@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ("name", "client", "position", "phone", "email", "is_primary")
    search_fields = ("name", "client__name", "phone", "email")


@admin.register(DealStage)
class DealStageAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_won", "is_lost", "is_active")
    list_editable = ("order", "is_active")


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "stage", "owner", "amount", "priority", "updated_at")
    list_filter = ("stage", "priority", "owner")
    search_fields = ("title", "client__name")
    inlines = [DealItemInline]


@admin.register(DealItem)
class DealItemAdmin(admin.ModelAdmin):
    list_display = ("deal", "name", "quantity", "price", "discount", "line_total")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("number", "client", "owner", "payment_status", "delivery_status", "work_status", "total", "created_at")
    list_filter = ("payment_status", "delivery_status", "work_status")
    search_fields = ("number", "client__name")
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "name", "quantity", "price", "discount", "line_total")


@admin.register(OrderFile)
class OrderFileAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "file", "uploaded_by", "uploaded_at")


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("tracking_number", "order", "provider", "status", "recipient_city", "updated_at")
    list_filter = ("provider", "status")
    search_fields = ("tracking_number", "order__number", "order__client__name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "price", "cost", "stock", "status")
    list_filter = ("status", "category")
    search_fields = ("name", "sku", "category", "description")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "assigned_to", "deadline", "status", "priority", "updated_at")
    list_filter = ("status", "priority", "assigned_to")
    search_fields = ("title", "description")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "recipient", "kind", "read_at", "created_at")
    list_filter = ("kind", "read_at")
    search_fields = ("title", "message", "recipient__username")


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "action", "object_repr", "content_type")
    list_filter = ("action", "content_type", "created_at")
    search_fields = ("object_repr", "user__username")
    readonly_fields = ("user", "action", "content_type", "object_id", "object_repr", "changes", "created_at")


admin.site.register(CustomField)
admin.site.register(IntegrationPlaceholder)
admin.site.register(InboxMessage)
admin.site.register(BotLead)
admin.site.register(CallLog)
admin.site.register(DocumentTemplate)
