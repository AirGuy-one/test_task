from django.urls import path
from .views import CDRListCreateView, CDRDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('cdr/', CDRListCreateView.as_view(), name='cdr-list'),
    path('cdr/<uuid:pk>/', CDRDetailView.as_view(), name='cdr-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
