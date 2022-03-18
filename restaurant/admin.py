from django.contrib import admin
from .models import Category,Review,Restaurant,Contact


class RestaurantAdmin(admin.ModelAdmin):
    list_display    = ["name","description","category","dt","prefecture","city","address","image","lat","lon","ip","judge_dt"]

class ContactAdmin(admin.ModelAdmin):
    list_display = ["title","content","dt","ip","email"]

admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Contact,ContactAdmin)


