from django.contrib import admin

from main_app.models import Product

# Register your models here.

# same sa:
# admin.site.register(Product)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
