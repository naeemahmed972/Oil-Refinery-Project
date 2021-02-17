from django.views.generic import ListView, CreateView, UpdateView, FormView, DetailView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, MultiplePermissionsRequiredMixin
from django.urls import reverse_lazy

from .models import StorageTank, StorageBranch, StorageLog, storage_operatons
from .forms import AddOilForm, DrawOilForm, MakeTankEmptyForm


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


class StorageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = 'login'
    redirect_field_name = "hollaback"
    raise_exception = True
    redirect_unauthenticated_users = True
    permission_required = 'oilstorage.store_management'

    model = StorageTank
    template_name = 'storage_tank_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StorageDetailView, self).get_context_data(**kwargs)
        query_tank = StorageTank.objects.get(id=self.kwargs['pk'])
        context['logs'] = StorageLog.objects.filter(operated_tank=query_tank).order_by('-operation_date')
        return context


class StorageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = "hollaback"
    raise_exception = True
    redirect_unauthenticated_users = True
    permission_required = 'oilstorage.store_management'

    model = StorageTank
    fields = ('name', 'capacity',)
    template_name = 'storage_tank_update.html'

    def get_context_data(self, **kwargs):
        context = super(StorageUpdateView, self).get_context_data(**kwargs)
        context['tank_id'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        form.instance.last_operated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        tank_id = self.get_context_data()['tank_id']
        tank = StorageTank.objects.get(id=tank_id)

        return reverse_lazy('tank_detail', kwargs={'pk': tank.id})


class StorageOilAddView(LoginRequiredMixin, MultiplePermissionsRequiredMixin, FormView):
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
        context = super(StorageOilAddView, self).get_context_data(**kwargs)
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


class StorageOilDrawView(LoginRequiredMixin, MultiplePermissionsRequiredMixin, FormView):
    login_url = 'login'
    redirect_field_name = "hollaback"
    raise_exception = True
    redirect_unauthenticated_users = True
    permissions = {
        "any": ("oilstorage.store_keeping", "oilstorage.store_management")
    }

    form_class = DrawOilForm
    template_name = 'storage_draw_oil.html'

    def get_context_data(self, **kwargs):
        context = super(StorageOilDrawView, self).get_context_data(**kwargs)
        query_tank = StorageTank.objects.get(id=self.kwargs['pk'])
        context['tank_name'] = query_tank.name
        context['tank_capacity'] = query_tank.capacity
        context['tank_volume'] = query_tank.current_volume
        context['tank_id'] = self.kwargs['pk']
        context['branch_list'] = StorageBranch.objects.all()
        return context

    def get_success_url(self) -> str:
        tank_id = self.get_context_data()['tank_id']
        tank = StorageTank.objects.get(id=tank_id)
        volume = int(self.request.POST['drawVolume'])
        branch_id = int(self.request.POST['deliveryBranch'])
        if volume >= 0:
            new_volume = tank.current_volume - volume
            if new_volume < 0:
                return False
            else:
                tank.current_volume = new_volume
        else:
            return False

        if new_volume < tank.capacity:
            if tank.is_full:
                tank.is_full = False

        if new_volume == 0:
            tank.is_empty = True

        tank.last_operated_by = self.request.user

        tank.save()

        log = StorageLog.objects.create(
            operation = storage_operatons["DRAW_OIL"],
            operated_tank = tank,
            operated_by = self.request.user,
            oil_volume = volume,
            delivered_to = StorageBranch.objects.get(id=branch_id)
        )
        log.save()

        return reverse_lazy('storage_list')


class StorageMakeEmptyView(LoginRequiredMixin, MultiplePermissionsRequiredMixin, FormView):
    login_url = 'login'
    redirect_field_name = "hollaback"
    raise_exception = True
    redirect_unauthenticated_users = True
    permissions = {
        "any": ("oilstorage.store_keeping", "oilstorage.store_management")
    }

    form_class = MakeTankEmptyForm
    template_name = 'storage_make_tank_empty.html'

    def get_context_data(self, **kwargs):
        context = super(StorageMakeEmptyView, self).get_context_data(**kwargs)
        query_tank = StorageTank.objects.get(id=self.kwargs['pk'])
        context['tank_name'] = query_tank.name
        context['tank_volume'] = query_tank.current_volume
        context['tank_id'] = self.kwargs['pk']
        return context

    def get_success_url(self) -> str:
        tank_id = self.get_context_data()['tank_id']
        tank = StorageTank.objects.get(id=tank_id)
        volume = self.get_context_data()['tank_volume']

        tank.current_volume = 0
        tank.is_empty = True
        
        if tank.is_full:
            tank.is_full = False

        tank.last_operated_by = self.request.user

        tank.save()

        log = StorageLog.objects.create(
            operation = storage_operatons["EMPTY"],
            operated_tank = tank,
            operated_by = self.request.user,
            oil_volume = volume,
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
    template_name = 'storage_branch_update.html'

