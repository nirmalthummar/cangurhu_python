from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import custom404,Redis,Translated

schema_view = get_schema_view(
   openapi.Info(
      title="Cangurhu API",
      default_version='v1',
      description="Cangurhu API Document",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

handler404 = custom404


urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Summernote Editor
    path('summernote/', include('django_summernote.urls')),

    path('Dashboard/', include('apps.dashboard.urls', namespace='dashboard')),

    # APIs URLs
    path('api/v1/accounts/', include('apps.accounts.api.urls', namespace='accounts')),
    path('api/v1/cook/', include('apps.cook.api.urls', namespace='cooks')),
    path('api/v1/courier/', include('apps.courier.api.urls', namespace='couriers')),
    path('api/v1/customer/', include('apps.customer.api.urls', namespace='customers')),
    path('api/v1/cart/', include('apps.cart.api.urls', namespace='carts')),
    path('api/v1/address/', include('apps.address.api.urls', namespace='address')),
    path('api/v1/snippets/', include('apps.snippets.api.urls', namespace='snippets')),
    path('api/v1/contents/', include('apps.contents.api.urls', namespace='content')),
    path('api/v1/notification/', include('apps.notification.api.urls', namespace='notification')),
    path('api/v1/cook-courier/', include('apps.rating.api.urls', namespace='ratings')),
    url(r'^./*$', custom404, name='error404'),
    # path("celery/",Redis.as_view(),name="celery")
    path("celery/", Redis.as_view(), name="celery"),
    path('api/v1/order/', include('apps.order.api.urls', namespace='order')),

    path("celery/", Redis.as_view(),name="celery"),
    path("translated/", Translated.as_view(),name="translated"),
    # path("api/v1/config/",include('apps.config.api.urls',namespace="config")),

    path('accounts/', include('allauth.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
