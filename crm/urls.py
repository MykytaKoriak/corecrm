from django.urls import include, path

from crm.views.clients import ClientCreateView, ClientDeleteView, ClientDetailView, ClientFileCreateView, ClientListView, ClientUpdateView, ContactPersonCreateView
from crm.views.dashboard import DashboardView, LoginView, LogoutView
from crm.views.deals import (
    DealCreateView,
    DealDeleteView,
    DealDetailView,
    DealItemCreateView,
    DealListView,
    DealPipelineView,
    DealUpdateView,
    create_order_from_deal,
    update_deal_stage,
)
from crm.views.integrations import (
    AnalyticsView,
    BotLeadCreateView,
    BotLeadListView,
    CallLogCreateView,
    CallLogListView,
    DocumentTemplateCreateView,
    DocumentTemplateListView,
    InboxMessageCreateView,
    InboxView,
    ShipmentCreateView,
    ShipmentListView,
)
from crm.views.notifications import NotificationListView, mark_all_notifications_read, mark_notification_read
from crm.views.orders import OrderCreateView, OrderDeleteView, OrderDetailView, OrderFileCreateView, OrderItemCreateView, OrderListView, OrderUpdateView
from crm.views.products import ProductCategoryListView, ProductCreateView, ProductDeleteView, ProductDetailView, ProductListView, ProductUpdateView
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
    path("clients/<int:client_pk>/files/new/", ClientFileCreateView.as_view(extra_context={"title": "Добавить файл клиента", "subtitle": "Документы, фото или служебные файлы", "cancel_url": "crm:clients"}), name="client_file_create"),
    path("clients/<int:client_pk>/contacts/new/", ContactPersonCreateView.as_view(extra_context={"title": "Новый контакт", "subtitle": "Контактное лицо внутри компании", "cancel_url": "crm:clients"}), name="contact_create"),
    path("deals/", DealPipelineView.as_view(), name="deals"),
    path("deals/list/", DealListView.as_view(), name="deal_list"),
    path("deals/new/", DealCreateView.as_view(extra_context={"title": "Новая сделка", "subtitle": "Клиент, этап, сумма и вероятность", "cancel_url": "crm:deals"}), name="deal_create"),
    path("deals/<int:pk>/", DealDetailView.as_view(), name="deal_detail"),
    path("deals/<int:pk>/edit/", DealUpdateView.as_view(extra_context={"title": "Редактировать сделку", "subtitle": "Обновите этап, сумму и детали", "cancel_url": "crm:deals"}), name="deal_update"),
    path("deals/<int:pk>/delete/", DealDeleteView.as_view(), name="deal_delete"),
    path("deals/<int:pk>/stage/", update_deal_stage, name="deal_stage_update"),
    path("deals/<int:pk>/create-order/", create_order_from_deal, name="deal_create_order"),
    path("deals/<int:deal_pk>/items/new/", DealItemCreateView.as_view(extra_context={"title": "Добавить товар в сделку", "subtitle": "Позиция автоматически пересчитает сумму сделки", "cancel_url": "crm:deals"}), name="deal_item_create"),
    path("orders/", OrderListView.as_view(), name="orders"),
    path("orders/new/", OrderCreateView.as_view(extra_context={"title": "Новый заказ", "subtitle": "Клиент, статусы и комментарии", "cancel_url": "crm:orders"}), name="order_create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("orders/<int:pk>/edit/", OrderUpdateView.as_view(extra_context={"title": "Редактировать заказ", "subtitle": "Оплата, доставка и рабочий статус", "cancel_url": "crm:orders"}), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("orders/<int:order_pk>/items/new/", OrderItemCreateView.as_view(extra_context={"title": "Добавить позицию", "subtitle": "Товар, количество, цена и скидка", "cancel_url": "crm:orders"}), name="order_item_create"),
    path("orders/<int:order_pk>/files/new/", OrderFileCreateView.as_view(extra_context={"title": "Добавить файл заказа", "subtitle": "Фото, документы и служебные файлы", "cancel_url": "crm:orders"}), name="order_file_create"),
    path("products/", ProductListView.as_view(), name="products"),
    path("products/categories/", ProductCategoryListView.as_view(), name="product_categories"),
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
    path("inbox/", InboxView.as_view(), name="inbox"),
    path("inbox/new/", InboxMessageCreateView.as_view(extra_context={"title": "Новое входящее сообщение", "subtitle": "Telegram, Instagram, телефония или ручной ввод", "cancel_url": "crm:inbox"}), name="inbox_create"),
    path("shipments/", ShipmentListView.as_view(), name="shipments"),
    path("shipments/new/", ShipmentCreateView.as_view(extra_context={"title": "Создать ТТН / отправление", "subtitle": "Базовая заготовка Новой Почты", "cancel_url": "crm:shipments"}), name="shipment_create"),
    path("bot-leads/", BotLeadListView.as_view(), name="bot_leads"),
    path("bot-leads/new/", BotLeadCreateView.as_view(extra_context={"title": "Заявка чат-бота", "subtitle": "Сбор контактов и создание клиента/сделки", "cancel_url": "crm:bot_leads"}), name="bot_lead_create"),
    path("calls/", CallLogListView.as_view(), name="calls"),
    path("calls/new/", CallLogCreateView.as_view(extra_context={"title": "Звонок", "subtitle": "Входящий, пропущенный и запись звонка", "cancel_url": "crm:calls"}), name="call_create"),
    path("analytics/", AnalyticsView.as_view(), name="analytics"),
    path("document-templates/", DocumentTemplateListView.as_view(), name="document_templates"),
    path("document-templates/new/", DocumentTemplateCreateView.as_view(extra_context={"title": "Шаблон документа", "subtitle": "КП, счет или договор", "cancel_url": "crm:document_templates"}), name="document_template_create"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("api/", include("crm.api.urls")),
]
