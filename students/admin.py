from django.contrib import admin
from .models import Student, DailyLog, Intervention


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'status', 'created_at')
    search_fields = ('name', 'email')


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'quiz_score', 'focus_minutes', 'result', 'created_at')
    list_filter = ('result',)


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'title', 'is_completed', 'created_at', 'completed_at')
    list_filter = ('is_completed',)

