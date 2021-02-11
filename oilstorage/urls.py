from django.urls import path
from .views import StorageListView, StorageCreateView


urlpatterns = [
    path('new/', StorageCreateView.as_view(), name='storage_new'),
    path('', StorageListView.as_view(), name='storage_list'),
]