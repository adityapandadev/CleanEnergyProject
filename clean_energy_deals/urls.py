from django.urls import path
from .views import ProjectView, DealsView

urlpatterns = [
    path('projects/', ProjectView.as_view(), name='projects-list-create'),
    path('projects/<int:pk>/', ProjectView.as_view(), name='projects-edit-delete'),
    path('deals/', DealsView.as_view(), name='deals-list-create'),
    path('deals/<int:pk>/', DealsView.as_view(), name='deal-edit-delete'),
]