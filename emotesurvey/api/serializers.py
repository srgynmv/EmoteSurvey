from survey.models import Question, Answer
from rest_framework import serializers


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = serializers.SerializerMethodField()

    def get_answers(self, obj):
        answers = obj.answers.all()
        return [answer.text for answer in answers]

    class Meta:
        model = Question
        fields = ['url', 'type', 'text', 'answers']
