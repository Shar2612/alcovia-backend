from django.db import models
from django.utils import timezone


class Student(models.Model):
    class Status(models.TextChoices):
        ON_TRACK = "ON_TRACK", "On Track"
        NEEDS_INTERVENTION = "NEEDS_INTERVENTION", "Needs Intervention"
        REMEDIAL_ASSIGNED = "REMEDIAL_ASSIGNED", "Remedial Assigned"

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.ON_TRACK,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DailyLog(models.Model):
    class Result(models.TextChoices):
        SUCCESS = "SUCCESS", "Success"
        FAIL = "FAIL", "Fail"

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='daily_logs'
    )
    quiz_score = models.IntegerField()
    focus_minutes = models.IntegerField()
    result = models.CharField(
        max_length=10,
        choices=Result.choices
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.result} - {self.created_at.date()}"


class Intervention(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='interventions'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def mark_completed(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.student.name} - {self.title}"

