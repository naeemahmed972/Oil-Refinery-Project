from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib import messages


from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ('first_name', 'last_name', 'email', 'age', 'address')
    template_name = 'update_user.html'
    login_url = 'login'
    # template_name = 'all_users_list.html'

    # def get_context_data(self,**kwargs):
    #     context = super(UsersView,self).get_context_data(**kwargs)
    #     context['users_list'] = CustomUser.objects.all()
    #     return context


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff



class UserListView(AdminStaffRequiredMixin, ListView):
    model = CustomUser
    template_name = 'user_list.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['store_management'] = 'oilstorage.store_management'
        context['store_keeping'] = 'oilstorage.store_keeping'
        return context


class UpdateUserPermissionView(AdminStaffRequiredMixin, UpdateView):
    model = CustomUser
    fields = ('user_permissions',)
    success_url = reverse_lazy('user_list')
    template_name = 'user_permissions.html'
    login_url = 'login'

