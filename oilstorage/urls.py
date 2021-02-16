from django.urls import path
from .views import StorageListView, StorageCreateView, BranchListView, BranchCreateView, BranchUpdateView, StorageOilDrawView


urlpatterns = [
    path('new/', StorageCreateView.as_view(), name='storage_new'),
    path('', StorageListView.as_view(), name='storage_list'),
    path('branch_list/', BranchListView.as_view(), name='branch_list'),
    path('branch_new/', BranchCreateView.as_view(), name='branch_new'),
    path('<int:pk>/branch_update/', BranchUpdateView.as_view(), name='branch_update'),
    path('<int:pk>/add_oil/', StorageOilDrawView.as_view(), name='add_oil'),
]