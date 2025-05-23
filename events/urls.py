from .views import EventView,EventDetailView,BulkEventView,EventViewShare
from django.urls import path

urlpatterns = [
    path('event_view/', EventView.as_view(), name='event_view'),
    path('<int:id>/', EventDetailView.as_view()),
    path('bulk_event/',BulkEventView.as_view(), name='bulk_event'),
    path('<int:id>/share/', EventViewShare.as_view(), name='share_event'),
    path('<int:id>/permissions/<int:user_id>/', EventViewShare.as_view(), name='update_permission'),
]
