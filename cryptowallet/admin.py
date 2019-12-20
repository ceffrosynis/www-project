from django.contrib import admin
from .models import BTCWallet, ETHWallet, LTCWallet, User
# Register your models here.


admin.site.register(BTCWallet)
admin.site.register(ETHWallet)
admin.site.register(LTCWallet)
admin.site.register(User)