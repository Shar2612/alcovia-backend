from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone

import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Student, DailyLog, Intervention
from .serializers import (
    DailyCheckinSerializer,
    AssignInterventionSerializer,
    StudentStatusSerializer,
)


class DailyCheckinView(APIView):
   

    def post(self, request, *args, **kwargs):
        serializer = DailyCheckinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        student = get_object_or_404(Student, id=data['student_id'])
        quiz_score = data['quiz_score']
        focus_minutes = data['focus_minutes']

       
        if quiz_score > 7 and focus_minutes > 60:
          
            DailyLog.objects.create(
                student=student,
                quiz_score=quiz_score,
                focus_minutes=focus_minutes,
                result=DailyLog.Result.SUCCESS,
            )
            student.status = Student.Status.ON_TRACK
            student.save()

            return Response({"status": "On Track"}, status=status.HTTP_200_OK)

        else:
            
            DailyLog.objects.create(
                student=student,
                quiz_score=quiz_score,
                focus_minutes=focus_minutes,
                result=DailyLog.Result.FAIL,
            )
            student.status = Student.Status.NEEDS_INTERVENTION
            student.save()

          
            webhook_url = getattr(settings, "N8N_WEBHOOK_URL", None)
            if webhook_url:
                try:
                    requests.post(
                        webhook_url,
                        json={
                            "student_id": student.id,
                            "student_name": student.name,
                            "student_email": student.email,
                            "quiz_score": quiz_score,
                            "focus_minutes": focus_minutes,
                            "status": "Needs Intervention",
                        },
                        timeout=5,
                    )
                except requests.RequestException:
                   
                    pass

            return Response(
                {"status": "Pending Mentor Review"},
                status=status.HTTP_200_OK
            )


class AssignInterventionView(APIView):
  

    def post(self, request, *args, **kwargs):
        serializer = AssignInterventionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        student = get_object_or_404(Student, id=data['student_id'])

        intervention = Intervention.objects.create(
            student=student,
            title=data['task_title'],
            description=data.get('task_description', ''),
        )

       
        student.status = Student.Status.REMEDIAL_ASSIGNED
        student.save()

        return Response(
            {
                "message": "Intervention assigned",
                "student_id": student.id,
                "intervention_id": intervention.id,
            },
            status=status.HTTP_200_OK,
        )


class StudentStatusView(APIView):
    

    def get(self, request, student_id, *args, **kwargs):
        student = get_object_or_404(Student, id=student_id)
        serializer = StudentStatusSerializer(student)

       
        app_state = "NORMAL"
        if student.status == Student.Status.NEEDS_INTERVENTION:
            app_state = "LOCKED"
        elif student.status == Student.Status.REMEDIAL_ASSIGNED:
            app_state = "REMEDIAL"

        data = serializer.data
        data["app_state"] = app_state

        return Response(data, status=status.HTTP_200_OK)


class CompleteInterventionView(APIView):
   

    def post(self, request, student_id, *args, **kwargs):
        student = get_object_or_404(Student, id=student_id)

        intervention = student.interventions.filter(
            is_completed=False
        ).last()

        if not intervention:
            return Response(
                {"detail": "No active intervention to complete."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        intervention.mark_completed()

       
        student.status = Student.Status.ON_TRACK
        student.save()

        return Response(
            {"message": "Intervention completed. Student back On Track."},
            status=status.HTTP_200_OK,
        )

