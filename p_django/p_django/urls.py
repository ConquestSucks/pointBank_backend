from django.contrib import admin
from django.urls import path
from pointBank.views import RegisterView, SignInView, ProtectedView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/signin/', SignInView.as_view(), name='signin'),   
    path('api/protected/', ProtectedView.as_view(), name='protected')
]
