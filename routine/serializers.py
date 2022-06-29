from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework import serializers

from .models import Routine, RoutineResult, RoutineDay
from .utils import (
    convert_days_list_to_date,
    convert_date_to_days_list,
    convert_days_list_to_date_at_update,
)


class CommonFieldMixin(serializers.Serializer):
    days = serializers.ListField(child=serializers.CharField(), read_only=True)
    id = serializers.IntegerField(source="account_id.id")
    result = serializers.SerializerMethodField()

    def get_result(self, obj):
        routine_result = get_object_or_404(
            RoutineResult, is_deleted=False, routine_id=obj
        )
        return routine_result.result


class RoutineCreateSerializer(CommonFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ("routine_id", "title", "category", "goal", "is_alarm", "days")

    @transaction.atomic
    def create(self, validated_data):
        routine = Routine.objects.create(**validated_data)
        self.create_routine_day(routine)
        return routine

    def create_routine_day(self, routine):
        days = self.get_days_data()
        for day in days:
            RoutineDay.objects.create(day=day, routine_id=routine)

    def get_days_data(self):
        request = self.context["request"].data
        days = request["days"]
        return convert_days_list_to_date(days)


class RoutineListSerializer(CommonFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = (
            "goal",
            "id",
            "result",
            "title",
        )


class RoutineDetailSerializer(CommonFieldMixin, serializers.ModelSerializer):
    days = serializers.SerializerMethodField()

    class Meta:
        model = Routine
        fields = ("goal", "id", "result", "title", "days")

    def get_days(self, obj):
        days = convert_date_to_days_list(obj)
        return days


class RoutineUpdateSerializer(CommonFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ("routine_id", "title", "category", "goal", "is_alarm", "days")

    @transaction.atomic
    def update(self, instance, validated_data):
        self.update_routine_day()
        return super().update(instance, validated_data)

    def update_routine_day(self):
        routine_id, days = self.get_request_data()
        routine = Routine.objects.get(routine_id=routine_id)
        data = convert_date_to_days_list(routine_id)
        old_days, new_days = set(data), set(days)
        delete_day = old_days - new_days
        create_day = new_days - old_days
        delete_date_box = convert_days_list_to_date_at_update(routine, delete_day)
        create_date_box = convert_days_list_to_date_at_update(routine, create_day)
        for delete_date in delete_date_box:
            routine_delete_day = RoutineDay.objects.get(
                day=delete_date, routine_id=routine
            )
            routine_delete_day.delete()

        for create_date in create_date_box:
            RoutineDay.objects.create(day=create_date, routine_id=routine)

    def get_request_data(self):
        request = self.context["request"].data
        return [request["routine_id"], request["days"]]


class RoutineResultCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineResult
        fields = ("result",)
