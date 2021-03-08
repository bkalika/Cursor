from django.contrib.auth.decorators import permission_required
from django.urls import path

from django.views.decorators.cache import cache_page

from .views import simple_view, tenant_view, TenantListView


room_patterns = [
    path('simple/', simple_view, name='simple'),
]

tenant_patterns = [
    path('tenants/', tenant_view, name='tenant'),
    path('tenant/list/', permission_required('mycore.view_tenant')(TenantListView.as_view()), name='tenant-list'),
]

urlpatterns = tenant_patterns + room_patterns
