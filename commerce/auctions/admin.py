from django.contrib import admin

# Register your models here.
from .models import AuctionList, Commentary, Lot

admin.site.register(AuctionList)
admin.site.register(Commentary)
admin.site.register(Lot)