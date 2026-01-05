from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('films/', views.film_list, name='film_list'),
    path('films/<int:pk>/', views.film_detail, name='film_detail'),
    path('review/add/<int:pk>/', views.add_review, name='add_review'),
    path('review/delete/<int:pk>/', views.delete_review, name='delete_review'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)