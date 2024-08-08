
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet,hello_world

router = DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = [
    path('helloworld/',hello_world),
    path('', include(router.urls)),

]
