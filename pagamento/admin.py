from django.contrib import admin
from .models import CreditCard, DebitCard, Payment

admin.site.register(CreditCard)
admin.site.register(DebitCard)
admin.site.register(Payment)


