from django.views.generic import ListView, CreateView, UpdateView, FormView, TemplateView
# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, MultiplePermissionsRequiredMixin
from django.urls import reverse_lazy

from .models import StorageTank, StorageBranch, StorageLog, storage_operatons
from .forms import AddOilForm


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


class StorageOilDrawView(LoginRequiredMixin, MultiplePermissionsRequiredMixin, FormView):
    login_url = 'login'
    redirect_field_name = "hollaback"
    raise_exception = True
    redirect_unauthenticated_users = True
    permissions = {
        "any": ("oilstorage.store_keeping", "oilstorage.store_management")
    }

    form_class = AddOilForm
    template_name = 'storage_add_oil.html'

    def get_context_data(self, **kwargs):
        context = super(StorageOilDrawView, self).get_context_data(**kwargs)
        query_tank = StorageTank.objects.get(id=self.kwargs['pk'])
        context['tank_name'] = query_tank.name
        context['tank_capacity'] = query_tank.capacity
        context['tank_volume'] = query_tank.current_volume
        context['tank_id'] = self.kwargs['pk']
        return context

    def get_success_url(self) -> str:
        tank_id = self.get_context_data()['tank_id']
        tank = StorageTank.objects.get(id=tank_id)
        volume = int(self.request.POST['addVolume'])
        if volume >= 0:
            new_volume = volume + tank.current_volume
            if new_volume > tank.capacity:
                return False
            else:
                tank.current_volume = new_volume
        else:
            return False

        if new_volume > 0:
            if tank.is_empty:
                tank.is_empty = False

        if new_volume == tank.capacity:
            tank.is_full = True

        tank.last_operated_by = self.request.user

        tank.save()

        log = StorageLog.objects.create(
            operation = storage_operatons["ADD_OIL"],
            operated_tank = tank,
            operated_by = self.request.user,
            oil_volume = volume
        )
        log.save()

        return reverse_lazy('storage_list')


class BranchListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = "hollaback"
    raise_exception = True
    redirect_unauthenticated_users = True
    permission_required = 'oilstorage.store_management'

    model = StorageBranch
    template_name = 'storage_branch_list.html'


class BranchCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = "hollaback"
    raise_exception = True
    redirect_unauthenticated_users = True
    permission_required = 'oilstorage.store_management'

    model = StorageBranch
    template_name = 'storage_branch_new.html'
    fields = ('name', 'location', 'capacity',)


class BranchUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = "hollaback"
    raise_exception = True
    redirect_unauthenticated_users = True
    permission_required = 'oilstorage.store_management'

    model = StorageBranch
    fields = ('name', 'location', 'capacity', 'current_volume', 'is_active',)
    # success_url = reverse_lazy('branch_list')
    template_name = 'storage_branch_update.html'

