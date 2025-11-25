from rest_framework import serializers
from .models import Student, DailyLog, Intervention


class DailyCheckinSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    quiz_score = serializers.IntegerField()
    focus_minutes = serializers.IntegerField()


class AssignInterventionSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    task_title = serializers.CharField(max_length=255)
    task_description = serializers.CharField(allow_blank=True, required=False)


class StudentStatusSerializer(serializers.ModelSerializer):
    current_intervention = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'status', 'current_intervention']

    def get_current_intervention(self, obj):
        intervention = obj.interventions.filter(is_completed=False).last()
        if not intervention:
            return None
        return {
            "id": intervention.id,
            "title": intervention.title,
            "description": intervention.description,
            "is_completed": intervention.is_completed,
        }
