from django.contrib import admin
from .models import *

class customeradmin(admin.ModelAdmin):
    class Meta:
        model=Customer
    list_display=['name','phone','email','date_created']
    list_display_links=['phone','email']
    #list_editable=['name']
    #search_fields=['name','email']
    #list_filter=['date_created']

admin.site.register(Customer,customeradmin) 

admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)

