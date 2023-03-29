from django.contrib import admin
from apps.courier.models import (Courier,
                                 CourierOrder,
                                 NewCourierTrainingDocument)

# Register your models here.

admin.site.register(Courier)


class NewCourierTrainingDocumentAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'document_file')


admin.site.register(NewCourierTrainingDocument, NewCourierTrainingDocumentAdmin)


class CourierOrderAdmin(admin.ModelAdmin):
    list_display = (
    'courier_order_id', 'courier', 'order', 'courier_status', 'eta', 'reason', 'total_distance', 'earnings')


admin.site.register(CourierOrder, CourierOrderAdmin)
