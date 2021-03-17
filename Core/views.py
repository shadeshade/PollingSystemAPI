from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Poll, Question
from .serializers import PollSerializer, QuestionSerializer, AllAnswersSerializer
from django.db.models import Q
import datetime

time_now = datetime.datetime.now()


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by('start_date')
    serializer_class = PollSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(Q(start_date__lte=time_now) & Q(finish_date__gte=time_now))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer_data = []
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # serializer_data.append(serializer.data)
        questions = [question for question in instance.questions.all()]
        for question in questions:
            question_serializer = QuestionSerializer(question)
            serializer_data.append(question_serializer.data)

        return Response(serializer_data)

    def post(self, request, *args, **kwargs):
        serializer = AllAnswersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return status.HTTP_201_CREATED

# {
#         "user_id": 1,
#         "question_id": 1,
#         "response": "1"
#     }

# class ResponseViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#
#     def post(self, request, *args, **kwargs):
#         if request.method == 'POST':
#             # form = ResponseForm(request.POST, survey=survey)
#             print('huray')
#             print('huray')
#             # if form.is_valid():
#             #     response = form.save()
