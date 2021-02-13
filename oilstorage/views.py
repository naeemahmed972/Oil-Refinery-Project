from django.views.generic import ListView, CreateView, UpdateView
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, MultiplePermissionsRequiredMixin
from django.urls import reverse_lazy

from .models import StorageTank, StorageBranch, StorageLog, storage_operatons


class StorageListView(LoginRequiredMixin, MultiplePermissionsRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = "hollaback"
    raise_exception = True
    redirect_unauthenticated_users = True
    permissions = {
        "any": ("oilstorage.store_keeping", "oilstorage.store_management")
    }

    model = StorageTank
    template_name = 'storage_list.html'


class StorageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = "hollaback"
    raise_exception = True
    redirect_unauthenticated_users = True
    permission_required = 'oilstorage.store_management'

    model = StorageTank
    template_name = 'storage_new.html'
    fields = ('name', 'capacity',)

    def form_valid(self, form):
        form.instance.last_operated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        log = StorageLog.objects.create(
            operation = storage_operatons["NEW_TANK"],
            operated_tank = StorageTank.objects.get(id=self.object.id),
            operated_by = self.request.user
        )
        log.save()
        return reverse_lazy('storage_list')


class StorageOperateView(LoginRequiredMixin, MultiplePermissionsRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = "hollaback"
    raise_exception = True
    redirect_unauthenticated_users = True
    permissions = {
        "any": ("oilstorage.store_keeping", "oilstorage.store_management")
    }

    model = StorageTank
    # fields = 

