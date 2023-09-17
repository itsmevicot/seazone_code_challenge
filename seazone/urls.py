from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Seazone API",
      default_version='v1',
      description="",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('anuncios.urls', namespace='anuncios')),
    path('', include('imoveis.urls', namespace='imoveis')),
    path('', include('reservas.urls', namespace='reservas')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
