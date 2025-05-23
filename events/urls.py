from .views import EventView,EventDetailView,BulkEventView,EventViewShare,EventHistoryView, EventRollbackView
from .views import EventHistoryListView,EventChangelogView,EventDiffView
from django.urls import path
 
 # for all urls here prefix with api/events/
urlpatterns = [
    path('event_view/', EventView.as_view(), name='event_view'),
    path('<int:id>/', EventDetailView.as_view()),
    path('bulk_event/',BulkEventView.as_view(), name='bulk_event'),
    path('<int:id>/share/', EventViewShare.as_view(), name='share_event'),
    path('<int:id>/permissions/<int:user_id>/', EventViewShare.as_view(), name='update_permission'),
    path('<int:id>/history/<int:version_id>/', EventHistoryView.as_view(), name='event_history'),
    path('<int:id>/history/', EventHistoryListView.as_view(), name='event_history_list'),
    path('<int:id>/rollback/<int:version_id>/', EventRollbackView.as_view(), name='event_rollback'),
    path('<int:id>/changelog/', EventChangelogView.as_view(), name='event_changelog'),
    path('<int:id>/diff/<int:version_id1>/<int:version_id2>/', EventDiffView.as_view(), name='event_diff'),
]
