from django.contrib import admin
from .models import Pet, CartItem, Order
from django.utils.html import format_html
from .models import Profile



# Register your models here.
class PetAdmin(admin.ModelAdmin):
    list_display = ["pet_id", "product_name", "category", "price", "proImage"]


admin.site.register(Pet, PetAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ["pet", "quantity", "date_added"]


admin.site.register(CartItem, CartAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_id", "pet_with_image", "quantity", "user", "is_completed", "date_added", "payment_screenshot_thumbnail"]

    def pet_with_image(self, obj):
        return obj.pet.proImage

    pet_with_image.short_description = 'Pet Image'

    def payment_screenshot_thumbnail(self, obj):
        if obj.payment_screenshot:
            return format_html('<img src="{}" width="100" height="auto" />', obj.payment_screenshot.url)
        else:
            return 'No screenshot'

    payment_screenshot_thumbnail.short_description = 'Payment Screenshot'

admin.site.register(Order, OrderAdmin)
admin.site.register(Profile)


