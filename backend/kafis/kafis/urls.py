from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from compare import views
from kafis import settings
from estimate import views as estimate_views

router = routers.DefaultRouter()
router.register(r'person', views.PersonView, 'person')
router.register(r'start', views.StartViewSet, 'start')
router.register(r'rate', views.RateViewSet, 'rate')
router.register(r'rating', views.RatingViewSet, 'rating')
router.register(r'report', views.ReportViewSet, 'report')

urlpatterns = [
    path('estimate', estimate_views.PhotoUploadView.as_view(), name='photo_upload'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
