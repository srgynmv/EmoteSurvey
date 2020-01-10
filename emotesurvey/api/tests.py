from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from survey.models import *
from survey.tests import TestWithQuestions
from . import views
from . import serializers

from datetime import timedelta

class TestWithQuestionsAndResults(TestWithQuestions):
    def setUp(self):
        super(TestWithQuestionsAndResults, self).setUp()

        # single choice question result
        r1 = Result.objects.create(question=self.q1)
        r1.answers.add(self.a1)

        # multiple choices question result
        r2 = Result.objects.create(question=self.q2)
        r2.answers.add(self.a3)
        r2.answers.add(self.a4)

        # text answer question result
        rans = Answer.objects.create(text='random answer', question=self.q3)
        r3 = Result.objects.create(question=self.q3)
        r3.answers.add(rans)

        RecordedData.objects.create(
            result=r3,
            timestamp=timedelta(seconds=1),
            surprise=0.1,
            fear=0.3,
            happiness=0.1,
            anger=0.0,
            disgust=0.0,
            sadness=0.0,
            neutral=0.5,
        )


class ResultSerializationTest(TestWithQuestionsAndResults):
    def test_serialize_query_results(self):
        query = views.ResultViewSet().get_queryset()
        serializer = serializers.ResultSerializer(query, many=True)
        data = serializer.data

        self.assertEqual(len(data), 3)
        for item in data:
            self.assertIn('question', item)
            self.assertIn('answers', item)
            self.assertIn('recorded_data_set', item)


class RawResultCreateTest(TestWithQuestions):
    def test_raw_result_serializer(self):
        factory = APIRequestFactory()
        view = views.ResultViewSet.as_view({'post': 'create'})
        url = reverse('api:result-list')
        data = {
            'question': self.q2.pk,
            'answers': ['answer3', 'answer4'],
            'recordedData': ',dGVzdA==\n'
        }

        request = factory.post(url, data=data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 201)

        results = Result.objects.all()
        self.assertEqual(len(results), 1)

        question = results[0].question
        answers = results[0].answers.all()
        self.assertEqual(question, self.q2)
        self.assertEqual(answers[0].text, 'answer3')
        self.assertEqual(answers[1].text, 'answer4')
