from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'questions', views.QuestionViewSet)
router.register(r'results', views.ResultsViewSet, basename='result')

urlpatterns = [
    path('', include(router.urls)),
]