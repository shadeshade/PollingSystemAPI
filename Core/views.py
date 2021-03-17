import datetime

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Poll, AnswerHead
from .serializers import PollSerializer, QuestionSerializer, AllAnswersSerializer, AnswerHeadSerializer

time_now = datetime.datetime.now()


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by('start_date')
    serializer_class = PollSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(start_date__lte=time_now, finish_date__gte=time_now)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer_data = []
        instance = self.get_object()
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


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = AnswerHead.objects.all()
    serializer_class = AnswerHeadSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user_id=kwargs['pk'])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
