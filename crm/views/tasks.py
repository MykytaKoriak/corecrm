from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from crm.forms import TaskForm
from crm.models import Task

from .mixins import CRMLoginRequiredMixin, SearchFilterMixin, scope_queryset_for_user


class TaskListView(CRMLoginRequiredMixin, SearchFilterMixin, ListView):
    model = Task
    template_name = "crm/tasks/list.html"
    context_object_name = "tasks"
    paginate_by = 20
    search_fields = ["title", "description", "client__name", "deal__title"]
    filter_fields = {"status": "status", "priority": "priority", "assignee": "assigned_to"}

    def get_queryset(self):
        qs = Task.objects.select_related("assigned_to", "client", "deal", "created_by")
        return self.apply_search_and_filters(qs)


class TaskDetailView(CRMLoginRequiredMixin, DetailView):
    model = Task
    template_name = "crm/tasks/detail.html"
    context_object_name = "task"


class TaskCreateView(CRMLoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "crm/form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        if not form.instance.assigned_to:
            form.instance.assigned_to = self.request.user
        return super().form_valid(form)


class TaskUpdateView(CRMLoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "crm/form.html"


class TaskDeleteView(CRMLoginRequiredMixin, DeleteView):
    model = Task
    template_name = "crm/confirm_delete.html"
    success_url = reverse_lazy("crm:tasks")


@require_POST
@login_required
def complete_task(request, pk):
    tasks = scope_queryset_for_user(Task.objects.all(), request.user)
    task = get_object_or_404(tasks, pk=pk)
    task.status = Task.Status.DONE
    task.completed_at = timezone.now()
    task.save(update_fields=["status", "completed_at", "updated_at"])
    return redirect(request.POST.get("next") or "crm:tasks")
