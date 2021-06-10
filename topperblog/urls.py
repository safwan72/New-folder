from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='My Blogger Api......')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogger.urls'), name="blogger"),
    path('api/blog/', include('blogger.api.urls')),
    path('api/', include('cdi.api.urls')),
    url('doc/api/', schema_view)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_CUSTOM_DIRS[0])
