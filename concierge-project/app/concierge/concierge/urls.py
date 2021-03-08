"""concierge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from mycore.views import index, PersonView, KeyView, RoomView, TenantView, KeyTransferView, api_serializer, PersonList,\
    KeyList, RoomList, TenantList, KetTransferList, TenantDetail
from .views import health_check


static_patterns = static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT) + \
                  static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('healthcheck/', health_check, name='health_check'),
    path('', index, name='index'),
    path('person/', PersonView.as_view(), name='person'),
    path('people/', PersonList.as_view(), name='people'),
    path('key/', KeyView.as_view(), name='key'),
    path('keys/', KeyList.as_view(), name='keys'),
    path('room/', RoomView.as_view(), name='room'),
    path('rooms/', RoomList.as_view(), name='rooms'),
    path('tenant/', TenantView.as_view(), name='tenant'),
    path('tenants/', TenantList.as_view(), name='tenants'),
    path('tenants/<int:pk>', TenantDetail.as_view(), name='tenantdetail'),
    path('keytransfer/', KeyTransferView.as_view(), name='keytransfer'),
    path('keytransfers/', KetTransferList.as_view(), name='keytransfers'),
    path('<str:object_type>/<int:object_id>', api_serializer, name='api-serializer')
              ] + static_patterns
