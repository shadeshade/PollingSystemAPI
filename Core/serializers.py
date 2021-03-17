from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Poll, Question, Answer, AnswerHead


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        # fields = ['question_type', 'created']
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'answer_text']

    def validate(self, attrs):
        # validate response text for every question - answer
        print('a')
        return attrs


class AllAnswersSerializer(serializers.Serializer):
    """
    {
        "user_id": 1,
        "answers": [
            {"question": 1, "answer_text": "a,b,e"}
        ]
    }
    """
    user_id = serializers.IntegerField()
    is_anonymous = serializers.BooleanField(required=False, default=False)
    answers = AnswerSerializer(many=True)

    def validate(self, attrs):
        # questions = attrs['answers'][0]['question'].poll.questions.all()
        # answers = attrs['answers']
        # if len(questions) == len(answers):
        #     if attrs['user_id']:
        #         if User.objects.get(id=attrs['user_id']):  # validate that user exists if user_id specified
        #             pass
        #         return attrs
        return attrs

    def create(self, validated_data):
        # create all the answers and answerHead based on validated_data
        user_id = validated_data['user_id']
        user = User.objects.get(id=user_id)
        answers = validated_data['answers']
        try:
            answer_head = AnswerHead.objects.get(user=user)
        except:
            is_anonymous = validated_data['is_anonymous']
            poll = validated_data['answers'][0]['question'].poll
            new_answer_head = AnswerHead.objects.create(user=user, poll=poll, is_anonymous=is_anonymous)
            new_answer_head.save()


