from django.contrib import admin

from .models import Routine, RoutineResult, RoutineDay


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = [
        "routine_id",
        "account_id",
        "title",
        "category",
        "goal",
        "is_alarm",
        "is_deleted",
        "created_at",
        "modified_at",
    ]


@admin.register(RoutineResult)
class RoutineResultAdmin(admin.ModelAdmin):
    list_display = [
        "routine_result_id",
        "routine_id",
        "result",
        "is_deleted",
        "created_at",
        "modified_at",
    ]


@admin.register(RoutineDay)
class RoutineDayAdmin(admin.ModelAdmin):
    list_display = ["day", "routine_id", "created_at", "modified_at"]
