from django.urls import path, include
from django.contrib import admin
from core import views as core_views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/category/', include('category.urls')),
    path('contact/', core_views.ContactAPIView.as_view()),
    path('api/recommend/', core_views.recommend),
    path('api-token-auth/', obtain_auth_token), #gives us access to token auth
]