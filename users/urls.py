from django.urls import path, include
from .forms import CustomAuthenticationForm
from .views import Register, CustomLoginView, block_reset

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('log/', CustomLoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('log/block-reset/', block_reset),
    path('register/', Register.as_view(), name='register'),
]