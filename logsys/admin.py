from django.contrib import admin
from .models import UserWallet


# Register your models here.


class adminUserWallet(admin.ModelAdmin):
    list_display = ('pk', 'UserWallet_user')


admin.site.register(UserWallet, adminUserWallet)




