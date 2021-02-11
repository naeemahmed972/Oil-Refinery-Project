from django.urls import path

from .views import SignUpView, UserUpdateView, UserListView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('<int:pk>/update_user/', UserUpdateView.as_view(), name='update_user'),
    path('users/', UserListView.as_view(), name='user_list'),
]