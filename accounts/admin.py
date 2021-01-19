from django.contrib import admin

# Register your models here.
from .models import *

# admin.site.register(Product)
# admin.site.register(Tag)
# admin.site.register(Order)


admin.site.register(Customer)
admin.site.register(Bank)
admin.site.register(Transaction)
admin.site.register(Referral)
admin.site.register(Game)
admin.site.register(CustomerGame)
admin.site.register(CustomerBank)
admin.site.register(SuccessMessage)
admin.site.register(Promotion)
admin.site.register(MaxWithdrawal)

