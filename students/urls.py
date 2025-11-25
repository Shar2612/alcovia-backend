from django.urls import path
from .views import (
    DailyCheckinView,
    AssignInterventionView,
    StudentStatusView,
    CompleteInterventionView,
)

urlpatterns = [
    path('daily-checkin/', DailyCheckinView.as_view(), name='daily-checkin'),
    path('assign-intervention/', AssignInterventionView.as_view(), name='assign-intervention'),
    path('student/<int:student_id>/status/', StudentStatusView.as_view(), name='student-status'),
    path('student/<int:student_id>/complete-intervention/', CompleteInterventionView.as_view(), name='complete-intervention'),
]
