from django.urls import include, path

from crm.views.clients import ClientCreateView, ClientDeleteView, ClientDetailView, ClientListView, ClientUpdateView
from crm.views.dashboard import DashboardView, LoginView, LogoutView
from crm.views.deals import (
    DealCreateView,
    DealDeleteView,
    DealDetailView,
    DealListView,
    DealPipelineView,
    DealUpdateView,
    create_order_from_deal,
    update_deal_stage,
)
from crm.views.notifications import NotificationListView, mark_all_notifications_read, mark_notification_read
from crm.views.orders import OrderCreateView, OrderDeleteView, OrderDetailView, OrderItemCreateView, OrderListView, OrderUpdateView
from crm.views.products import ProductCreateView, ProductDeleteView, ProductDetailView, ProductListView, ProductUpdateView
from crm.views.settings import SettingsView
from crm.views.tasks import TaskCreateView, TaskDeleteView, TaskDetailView, TaskListView, TaskUpdateView, complete_task

app_name = "crm"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", DashboardView.as_view(), name="dashboard"),
    path("clients/", ClientListView.as_view(), name="clients"),
    path("clients/new/", ClientCreateView.as_view(extra_context={"title": "Новый клиент", "subtitle": "Контакты, ответственный и рабочая информация", "cancel_url": "crm:clients"}), name="client_create"),
    path("clients/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("clients/<int:pk>/edit/", ClientUpdateView.as_view(extra_context={"title": "Редактировать клиента", "subtitle": "Обновите карточку и контакты", "cancel_url": "crm:clients"}), name="client_update"),
    path("clients/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
    path("deals/", DealPipelineView.as_view(), name="deals"),
    path("deals/list/", DealListView.as_view(), name="deal_list"),
    path("deals/new/", DealCreateView.as_view(extra_context={"title": "Новая сделка", "subtitle": "Клиент, этап, сумма и вероятность", "cancel_url": "crm:deals"}), name="deal_create"),
    path("deals/<int:pk>/", DealDetailView.as_view(), name="deal_detail"),
    path("deals/<int:pk>/edit/", DealUpdateView.as_view(extra_context={"title": "Редактировать сделку", "subtitle": "Обновите этап, сумму и детали", "cancel_url": "crm:deals"}), name="deal_update"),
    path("deals/<int:pk>/delete/", DealDeleteView.as_view(), name="deal_delete"),
    path("deals/<int:pk>/stage/", update_deal_stage, name="deal_stage_update"),
    path("deals/<int:pk>/create-order/", create_order_from_deal, name="deal_create_order"),
    path("orders/", OrderListView.as_view(), name="orders"),
    path("orders/new/", OrderCreateView.as_view(extra_context={"title": "Новый заказ", "subtitle": "Клиент, статусы и комментарии", "cancel_url": "crm:orders"}), name="order_create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("orders/<int:pk>/edit/", OrderUpdateView.as_view(extra_context={"title": "Редактировать заказ", "subtitle": "Оплата, доставка и рабочий статус", "cancel_url": "crm:orders"}), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("orders/<int:order_pk>/items/new/", OrderItemCreateView.as_view(extra_context={"title": "Добавить позицию", "subtitle": "Товар, количество, цена и скидка", "cancel_url": "crm:orders"}), name="order_item_create"),
    path("products/", ProductListView.as_view(), name="products"),
    path("products/new/", ProductCreateView.as_view(extra_context={"title": "Новый товар", "subtitle": "Каталог, цена, себестоимость и остаток", "cancel_url": "crm:products"}), name="product_create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:pk>/edit/", ProductUpdateView.as_view(extra_context={"title": "Редактировать товар", "subtitle": "Данные каталога и склада", "cancel_url": "crm:products"}), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("tasks/", TaskListView.as_view(), name="tasks"),
    path("tasks/new/", TaskCreateView.as_view(extra_context={"title": "Новая задача", "subtitle": "Ответственный, дедлайн и приоритет", "cancel_url": "crm:tasks"}), name="task_create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(extra_context={"title": "Редактировать задачу", "subtitle": "Статус, дедлайн и привязки", "cancel_url": "crm:tasks"}), name="task_update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    path("tasks/<int:pk>/complete/", complete_task, name="task_complete"),
    path("notifications/", NotificationListView.as_view(), name="notifications"),
    path("notifications/<int:pk>/read/", mark_notification_read, name="notification_read"),
    path("notifications/read-all/", mark_all_notifications_read, name="notifications_read_all"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("api/", include("crm.api.urls")),
]
