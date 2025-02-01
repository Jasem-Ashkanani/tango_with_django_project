from django.urls import path
from rango import views 
from django.conf import settings
from django.conf.urls.static import static

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('about/', views.about, name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)