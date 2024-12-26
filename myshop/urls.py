from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from myshop import settings

urlpatterns = [
    path('', include('shop.urls', namespace='pages')),
    path('', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'shop.views.permission_denied'
handler404 = 'shop.views.page_not_found'
handler500 = 'shop.views.server_error'
