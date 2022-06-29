from django.urls import path, re_path
from .views import (
    RoutineCreateView,
    RoutineListView,
    RoutineDetailUpdateDeleteView,
    RoutineResultCreateView,
)

urlpatterns = [
    path("routine/", RoutineCreateView.as_view()),
    re_path(
        r"^routine/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/",
        RoutineListView.as_view(),
    ),
    path("routine/<int:routine_id>/", RoutineDetailUpdateDeleteView.as_view()),
    path("routine/result/<int:routine_id>/", RoutineResultCreateView.as_view()),
]
