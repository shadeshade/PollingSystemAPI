from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validate_date(start_date, finish_date):
    if start_date > finish_date:
        raise ValidationError("The start date must be earlier than the finish date")


class Poll(models.Model):
    name = models.CharField(max_length=40)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    description = models.TextField()

    def save(self, *args, **kwargs):
        validate_date(self.start_date, self.finish_date)
        super(Poll, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def validate_list(value):
    values = value.split(',')
    if len(values) < 2:
        raise ValidationError("Need more than one choice for the poll")


class Question(models.Model):
    TEXT = 'text'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select_multiple'

    QUESTION_TYPES = (
        (TEXT, 'Text'),
        (SELECT, 'Select'),
        (SELECT_MULTIPLE, 'Select Multiple'),
    )

    question_text = models.TextField()
    choices = models.TextField(blank=True, null=True,
                               help_text="If the question type is select or select multiple provide "
                                         "a comma-separated list of options for this question")
    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.question_type == Question.SELECT or self.question_type == Question.SELECT_MULTIPLE:
            validate_list(self.choices)
        super(Question, self).save(*args, **kwargs)

    def get_choices(self):
        choices = self.choices.split(',')
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append((c, c))
        choices_tuple = tuple(choices_list)
        return choices_tuple

    def __str__(self):
        if len(self.question_text) > 40:
            return f"{self.question_text[:40]}..."
        return self.question_text



class AnswerHead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    answer_head = models.ForeignKey(AnswerHead, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
