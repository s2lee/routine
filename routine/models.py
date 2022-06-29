from django.db import models
from accounts.models import CustomUser as User


class RoutineValidManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_deleted=False)


class Routine(models.Model):

    CATEGORY_CHOICES = [
        ("MIRACLE", "기상 관련"),
        ("HOMEWORK", "숙제 관련"),
    ]

    routine_id = models.BigAutoField(primary_key=True)
    account_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    goal = models.TextField()
    is_alarm = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.title)[:10]

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    objects = models.Manager()
    valid_objects = RoutineValidManager()


class RoutineResult(models.Model):

    RESULT_CHOICES = [("NOT", "안함"), ("TRY", "시도"), ("DONE", "완료")]

    routine_result_id = models.AutoField(primary_key=True)
    routine_id = models.OneToOneField(
        Routine, on_delete=models.CASCADE, related_name="routine_result"
    )
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"Routine {self.routine_id} - Result"


class RoutineDay(models.Model):
    day = models.DateField()
    routine_id = models.ForeignKey(
        Routine, on_delete=models.CASCADE, related_name="routine_day"
    )
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"Routine {self.routine_id} - {self.day}"

