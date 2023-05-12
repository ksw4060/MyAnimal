
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('articles/', include('articles.urls')),
] + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)

# 배포 시에는 디버그 모드를 꺼야 하기에 다른 방식으로 설정해야한다고 말씀하셨다.
