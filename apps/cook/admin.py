from django.contrib import admin

from apps.cook.models import (
    Cook,
    KitchenPremises,
    MenuCategory,
    MenuItem,
    MenuSubItem,
    FSCCatalogue,
    FSCCatalogueImage,
    CookOrderDetails
)

admin.site.register(KitchenPremises)
# admin.site.register(MenuCategory)
admin.site.register(FSCCatalogue)
admin.site.register(FSCCatalogueImage)
admin.site.register(CookOrderDetails)


class CookAdmin(admin.ModelAdmin):
    list_display = ('id', 'cook_id', 'user', 'country', 'dob', 'featured_cook', 'top_cook', 'near_by_cook', 'status')


admin.site.register(Cook, CookAdmin)


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_number', 'title', 'cook', 'total_like', 'total_dislike', 'avg_star_rating', 'total_review')


admin.site.register(MenuItem, MenuItemAdmin)


class MenuSubItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'menu_item')


admin.site.register(MenuSubItem, MenuSubItemAdmin)


class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')


admin.site.register(MenuCategory, MenuCategoryAdmin)