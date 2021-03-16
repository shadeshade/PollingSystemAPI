from rest_framework import serializers

from .models import Poll, Question


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'
        # fields = ['name', 'start_date', 'finish_date', 'description', 'question_question_text']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_type', 'created']
        # fields = '__all__'
