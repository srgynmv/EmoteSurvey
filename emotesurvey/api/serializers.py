import os
import time
import base64
from datetime import timedelta
from django.conf import settings
from survey.models import *
from rest_framework import serializers
from emotenn.emotenn.run import EmoteClassifier


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
    # TODO(srgynmv): add session
    question = serializers.IntegerField()
    answers = serializers.ListField(child=serializers.CharField(),
                                    allow_empty=False)
    recordedData = serializers.CharField() # base64
    classifier = EmoteClassifier()

    def create(self, validated_data):
        question = Question.objects.get(pk=validated_data['question'])
        result = Result.objects.create(question=question)

        for answer_text in validated_data['answers']:
            answer, created = Answer.objects.get_or_create(question=question, text=answer_text)
            result.answers.add(answer)

        recorded_data_base64 = validated_data['recordedData'].split(',', 1)[1].encode()
        video = base64.decodebytes(recorded_data_base64)
        self.process_video_data(video, result)

        return result

    def process_video_data(self, video, result):
        time_str = time.strftime('%Y%m%d-%H%M%S')
        file_name = '{ts}-q{number}.webm'.format(ts=time_str, number=result.question.pk)
        file_path = os.path.join(settings.TEMP_DIR, file_name)
        with open(file_path, 'wb') as video_file:
            video_file.write(video)

        def on_frame(img, faces, timestamp):
            faces = list(faces)
            if len(faces) == 0:
                return

            # Assume there is only one face, but if there are many, we take the largest
            faces.sort(key=lambda face: face[0][2] * face[0][3], reverse=True)
            _, emotion_classes = faces[0]

            RecordedData.objects.create(result=result,
                    timestamp=timedelta(milliseconds=timestamp),
                    anger=emotion_classes[0],
                    disgust=emotion_classes[1],
                    fear=emotion_classes[2],
                    happiness=emotion_classes[3],
                    sadness=emotion_classes[4],
                    surprise=emotion_classes[5],
                    neutral=emotion_classes[6])

        self.classifier.process_source(file_path, on_frame)
        os.remove(file_path)

    def to_representation(self, instance):
        return ResultSerializer(instance).data


class ResultSerializer(serializers.Serializer):
    # TODO(srgynmv): add session
    question = serializers.PrimaryKeyRelatedField(read_only=True)
    answers = AnswerSerializer(many=True)
    recorded_data_set = RecordedDataSerializer(many=True)
