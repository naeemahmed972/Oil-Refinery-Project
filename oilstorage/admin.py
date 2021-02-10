from django.contrib import admin

from .models import StorageTank, StorageBranch, StorageLog


admin.site.register(StorageTank)
admin.site.register(StorageBranch)
admin.site.register(StorageLog)

