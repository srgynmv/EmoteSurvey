from django.db import models
from enum import Enum


class Survey(models.Model):
    title = models.CharField(max_length=100)


class AnswerTypeChoices(Enum):
    SINGLE = "single"
    MULTI = "multiple"
    TEXT = "text"


class Question(models.Model):
    type = models.CharField(
        max_length=10,
        choices=[(tag, tag.value) for tag in AnswerTypeChoices]
    )
    text = models.TextField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)


class Answer(models.Model):
    text = models.CharField(max_length=300)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Session(models.Model):
    pass


class Result(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


class RecordedData(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    timestamp = models.TimeField()
    surprise = models.FloatField()
    fear = models.FloatField()
    happiness = models.FloatField()
    anger = models.FloatField()
    disgust = models.FloatField()
    sadness = models.FloatField()
    neutral = models.FloatField()
