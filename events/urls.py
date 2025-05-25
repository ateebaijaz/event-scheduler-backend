from .views import EventView,EventDetailView,BulkEventView,EventHistoryView, EventRollbackView
from .views import EventShareView, EventPermissionListView, EventPermissionUpdateView, EventHistoryListView
from .views import EventChangelogView, EventDiffView
from django.urls import path
 
 # for all urls here prefix with api/events/
urlpatterns = [
    path('', EventView.as_view(), name='event_view'),
    path('<int:id>/', EventDetailView.as_view()),
    path('batch/',BulkEventView.as_view(), name='bulk_event'),
    path('<int:id>/share/', EventShareView.as_view(), name='share_event'),
    path('<int:id>/permissions/', EventPermissionListView.as_view(), name='list_permissions'),
    path('<int:id>/permissions/<int:user_id>/', EventPermissionUpdateView.as_view(), name='update_permission'),
    path('<int:id>/history/<int:version_id>/', EventHistoryView.as_view(), name='event_history'),
    path('<int:id>/history/', EventHistoryListView.as_view(), name='event_history_list'),
    path('<int:id>/rollback/<int:version_id>/', EventRollbackView.as_view(), name='event_rollback'),
    path('<int:id>/changelog/', EventChangelogView.as_view(), name='event_changelog'),
    path('<int:id>/diff/<int:version_id1>/<int:version_id2>/', EventDiffView.as_view(), name='event_diff'),
]
