from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Poll, Question
from .serializers import PollSerializer, QuestionSerializer


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by('start_date')
    serializer_class = PollSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        questions = instance.questions.all()
        queryset = Poll.objects.all()
        question_serializer = QuestionSerializer(questions)
        return Response(question_serializer.data)


# class QuestionViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         questions = instance.questions.all()
#         return Response(serializer.data)

