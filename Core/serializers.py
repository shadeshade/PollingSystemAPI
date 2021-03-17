from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError, ObjectDoesNotExist

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
        if not attrs["answer_text"]:
            raise ValidationError

        if attrs["question"].question_type == "select" and len(attrs["answer_text"].split(',')) == 1:
            pass
        elif attrs["question"].question_type == "select_multiple" and len(attrs["answer_text"].split(',')) >= 2:
            pass
        elif attrs["question"].question_type == "text":
            pass
        else:
            raise ValidationError

        if attrs["question"].question_type in ("select", "select_multiple"):
            check_choices = set(el.strip() for el in attrs["answer_text"].split(',')) - set(el.strip() for el in attrs["question"].choices.split(','))
            if check_choices:
                raise ValidationError
        return attrs


class AllAnswersSerializer(serializers.Serializer):
    """
    {
        "user_id": 1,
        "answers": [
            {"question": 1, "answer_text": "a,b,e"},
            {"question": 2, "answer_text": "a,b,e"},
            {"question": 3, "answer_text": "a,b,e"}
        ]
    }
    """
    user_id = serializers.IntegerField()
    is_anonymous = serializers.BooleanField(required=False, default=False)
    answers = AnswerSerializer(many=True)

    def validate(self, attrs):
        questions = attrs['answers'][0]['question'].poll.questions.all()
        answers = attrs['answers']
        unique_answers = set(a['question'].id for a in answers)
        if len(questions) == len(unique_answers):
            return attrs

        return ValidationError

    def create(self, validated_data):
        """create all the answers and answerHead based on validated_data"""
        user_id = validated_data['user_id']
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist
        is_anonymous = validated_data['is_anonymous']
        poll = validated_data['answers'][0]['question'].poll

        answer_head = AnswerHead.objects.create(user=user, poll=poll, is_anonymous=is_anonymous)
        answer_head.save()

        answers = [vd for vd in validated_data["answers"]]
        for answer in answers:
            Answer.objects.create(answer_head=answer_head,
                                  question=answer["question"],
                                  answer_text=answer["answer_text"]).save()
        return answer_head


"""

{
        "user_id": 1,
        "answers": [
            {"question": 1, "answer_text": "qwe, eqw"},
            {"question": 2, "answer_text": "ew"},
            {"question": 3, "answer_text": "cxz,czxcxz"},
            {"question": 4, "answer_text": "cxz,czxcxz"}
        ]
    }

"""
