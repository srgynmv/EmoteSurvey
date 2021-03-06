from django.db import models
from enum import IntEnum


def elide(text, max_length=20):
    return text if len(text) <= max_length else text[:max_length] + '...'


class Survey(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class AnswerType(IntEnum):
    SINGLE = 0
    MULTIPLE = 1
    TEXT = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name.title()) for key in cls]


class Question(models.Model):
    type = models.IntegerField(choices=AnswerType.choices())
    text = models.TextField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return elide(self.text)


class Answer(models.Model):
    text = models.CharField(max_length=300)
    question = models.ForeignKey(Question, related_name='answers', 
                                 on_delete=models.CASCADE)

    def __str__(self):
        return elide(self.text)


class Result(models.Model):
    #TODO(srgynmv): add a session identifier
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer)


class RecordedData(models.Model):
    result = models.ForeignKey(Result, related_name='recorded_data_set',
                               on_delete=models.CASCADE)
    timestamp = models.DurationField()
    surprise = models.FloatField()
    fear = models.FloatField()
    happiness = models.FloatField()
    anger = models.FloatField()
    disgust = models.FloatField()
    sadness = models.FloatField()
    neutral = models.FloatField()
