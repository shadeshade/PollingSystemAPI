from django.core.exceptions import ValidationError
from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=40)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    description = models.TextField()


def validate_list(value):
    values = value.split(',')
    if len(values) < 2:
        raise ValidationError("Need more than one question for a poll")


class Question(models.Model):
    TEXT = 'text'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'

    QUESTION_TYPES = (
        (TEXT, 'Text'),
        (SELECT, 'Select'),
        (SELECT_MULTIPLE, 'Select Multiple'),
    )

    question_text = models.TextField()
    choices = models.TextField(blank=True, null=True)
    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
