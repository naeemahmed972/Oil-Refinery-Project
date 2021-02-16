from os import name
from django.urls import path
from .views import StorageListView, StorageCreateView, BranchListView, BranchCreateView, BranchUpdateView, StorageOilAddView, StorageOilDrawView, StorageMakeEmptyView, StorageDetailView, StorageUpdateView


urlpatterns = [
    path('new/', StorageCreateView.as_view(), name='storage_new'),
    path('', StorageListView.as_view(), name='storage_list'),
    path('branch_list/', BranchListView.as_view(), name='branch_list'),
    path('branch_new/', BranchCreateView.as_view(), name='branch_new'),
    path('<int:pk>/branch_update/', BranchUpdateView.as_view(), name='branch_update'),
    path('<int:pk>/add_oil/', StorageOilAddView.as_view(), name='add_oil'),
    path('<int:pk>/draw_oil/', StorageOilDrawView.as_view(), name='draw_oil'),
    path('<int:pk>/empty_tank/', StorageMakeEmptyView.as_view(), name='empty_tank'),
    path('<int:pk>/tank_detail/', StorageDetailView.as_view(), name='tank_detail'),
    path('<int:pk>/tank_update/', StorageUpdateView.as_view(), name='tank_update'),
]