from django.contrib import admin
from apps.rating.models import CookFeedback, DishGrade


class CookFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'cook', 'courier_user', 'star_rating', 'active')


admin.site.register(CookFeedback, CookFeedbackAdmin)


class DishGradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'menu_item', 'star_rating', 'like', 'dislike', 'taste', 'use_of_ingredients', 'presentation', 'active')


admin.site.register(DishGrade, DishGradeAdmin)

