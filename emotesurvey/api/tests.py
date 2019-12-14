from django.test import TestCase
from survey.models import *
from survey.tests import TestWithFilledDb
from . import views
from . import serializers


class ResultSerializationTest(TestWithFilledDb):
    def test_query_results(self):
        query = views.ResultsViewSet().get_queryset()
        serializer = serializers.ResultSerializer(query, many=True)
        data = serializer.data

        self.assertEqual(len(data), 3)
        for item in data:
            self.assertIn('question', item)
            self.assertIn('answers', item)
            self.assertIn('recorded_data_set', item)
