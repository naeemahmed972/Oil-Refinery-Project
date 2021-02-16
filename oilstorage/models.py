from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse



# Database Models


# only these operations can be performed on storage tanks
storage_operatons = {
    "NEW_TANK": "new tank added",
    "ADD_OIL" : "oil added",
    "DRAW_OIL" : "oil drawn",
    "EMPTY" : "tank emptied",
    "BLOCK" : "tank marked as not working",
    "UNBLOCK" : "tank marked as working",
    "REMOVE": "storage tank removed"
}



# following are the database tables to be created in the database

class StorageTank(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    current_volume = models.PositiveIntegerField(default=0)
    installed_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_empty = models.BooleanField(default=True)
    is_full = models.BooleanField(default=False)
    last_operated_at = models.DateTimeField(auto_now=True)
    last_operated_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='tank_operator')

    class Meta:
        permissions = [
            ('store_management', 'Can manage oil storage and tank info'),
            ('store_keeping', 'Can record the storage info'),
        ]

    def __str__(self):
        return f"Tank: {self.name}, Volume: {self.capacity} ltrs."

    def get_absolute_url(self):
        return reverse('storage_list')


class StorageBranch(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    current_volume = models.PositiveIntegerField(default=0)
    added_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Branch: {self.name}, Location: {self.location}"

    def get_absolute_url(self):
        return reverse('branch_list')


class StorageLog(models.Model):
    operation = models.CharField(max_length=200)
    operated_tank = models.ForeignKey(StorageTank, on_delete=models.CASCADE, related_name='operated_tank')
    operated_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='storage_operator')
    operation_date = models.DateTimeField(auto_now_add=True)
    oil_volume = models.PositiveIntegerField(null=True)
    delivered_to = models.ForeignKey(StorageBranch, on_delete=models.CASCADE, related_name='receiving_branch', null=True)

    def __str__(self):
        return f"Operation: {self.operation}, On: {self.operated_tank}"

