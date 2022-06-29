from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .models import Routine, RoutineDay
from .utils import get_response
from .serializers import (
    RoutineCreateSerializer,
    RoutineListSerializer,
    RoutineDetailSerializer,
    RoutineUpdateSerializer,
    RoutineResultCreateSerializer,
)


class RoutineCreateView(CreateAPIView):
    routine_id = None
    serializer_class = RoutineCreateSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return get_response(self.routine_id, "CREATE")

    def perform_create(self, serializer):
        routine = serializer.save(account_id=self.request.user)
        self.routine_id = routine.routine_id


class RoutineListView(ListAPIView):
    serializer_class = RoutineListSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        routine_day_queryset = RoutineDay.objects.filter(day=self.get_date())
        data = []
        for routine_day in routine_day_queryset:
            routine_queryset = self.get_filtered_valid_routine_queryset()
            routine = routine_queryset.get(routine_id=routine_day.routine_id.routine_id)
            data.append(self.get_serializer(routine).data)
        return get_response(data, "LIST")

    def get_filtered_valid_routine_queryset(self):
        routine_qs = Routine.valid_objects.select_related(
            "account_id", "routine_result"
        ).filter(account_id=self.request.user)
        return routine_qs

    def get_date(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        return datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")


class RoutineDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    routine_id = None
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RoutineDetailSerializer
        return RoutineUpdateSerializer

    def get_object(self):
        self.routine_id = self.kwargs["routine_id"]
        try:
            routine = Routine.valid_objects.get(
                routine_id=self.routine_id, account_id=self.request.user
            )
            return routine
        except ObjectDoesNotExist:
            raise Http404("No Routine object matches the given query")

    def retrieve(self, request, *args, **kwargs):
        routine = self.get_object()
        serializer = self.get_serializer(routine)
        return get_response(serializer.data, "DETAIL")

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return get_response(self.routine_id, "UPDATE")

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return get_response(self.routine_id, "DELETE")


class RoutineResultCreateView(CreateAPIView):
    serializer_class = RoutineResultCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        routine = Routine.objects.get(routine_id=self.kwargs["routine_id"])
        serializer.save(routine_id=routine)
