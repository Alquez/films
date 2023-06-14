from django.urls import path
from . import views

urlpatterns = [
    path('success/', views.SuccessView.as_view(), name='success'),
    path('need_authenticate/', views.need_authenticate, name='u_need_authenticate'),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
]
