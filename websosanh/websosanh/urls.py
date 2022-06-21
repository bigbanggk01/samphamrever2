from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
# from api import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include('api.urls')),
    path('admin/', admin.site.urls)
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]