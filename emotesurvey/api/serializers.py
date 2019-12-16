from survey.models import *
from rest_framework import serializers


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['text']

    def to_representation(self, instance):
        return instance.text


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerSerializer(many=True)
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return obj.get_type_display().lower()

    class Meta:
        model = Question
        fields = ['url', 'id', 'type', 'text', 'answers']
        extra_kwargs = {
            'url': {'view_name': 'api:question-detail'}
        }


class RecordedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordedData
        fields = ['timestamp', 'surprise', 'fear', 'happiness', 'anger',
                  'disgust', 'sadness', 'neutral']


class RawResultSerializer(serializers.Serializer):
    # TODO(srgynmv): add session and recorded_data
    question = serializers.IntegerField()
    answers = serializers.ListField(child=serializers.CharField(),
                                    allow_empty=False)

    def create(self, validated_data):
        question = Question.objects.get(pk=validated_data['question'])
        result = Result.objects.create(question=question)
        for answer_text in validated_data['answers']:
            answer, created = Answer.objects.get_or_create(question=question, text=answer_text)
            result.answers.add(answer)
        return result

    def to_representation(self, instance):
        return ResultSerializer(instance).data


class ResultSerializer(serializers.Serializer):
    # TODO(srgynmv): add session
    question = serializers.PrimaryKeyRelatedField(read_only=True)
    answers = AnswerSerializer(many=True)
    recorded_data_set = RecordedDataSerializer(many=True)