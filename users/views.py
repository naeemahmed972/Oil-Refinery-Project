from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, TemplateView

from .models import CustomUser
from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UsersView(TemplateView):
    template_name = 'all_users_list.html'

    def get_context_data(self,**kwargs):
        context = super(UsersView,self).get_context_data(**kwargs)
        context['users_list'] = CustomUser.objects.all()
        return context

