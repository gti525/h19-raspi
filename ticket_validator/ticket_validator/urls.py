from django.contrib import admin
from django.urls import path, re_path

from rest_framework import permissions
from rest_framework.authtoken import views as drf_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Ticket Validator API",
      default_version='v1',
      description="API de gestion de billet",
   ),
   permission_classes=(permissions.AllowAny,),
   public=True,
)

urlpatterns = [
   path('admin/', admin.site.urls),

   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

   path('token-auth/', drf_views.ObtainAuthToken.as_view()),
   path('scan/', views.TicketScanView.as_view()),
   path('billetScan', views.TicketScanView.as_view()),
   path('tickets', views.ReceiveTicketView.as_view()),
   path('attendance', views.AttendingReportView.as_view()),
   path('scanned', views.ScannedTicketsView.as_view()),
]
