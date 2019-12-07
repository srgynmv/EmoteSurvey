from django.test import TestCase
from .models import *


class TestWithFilledDb(TestCase):
    def setUp(self):
        survey = Survey.objects.create(title='survey title')
        q1 = Question.objects.create(
            type=AnswerType.SINGLE,
            text='question one text',
            survey=survey
        )
        a1 = Answer.objects.create(text='answer1', question=q1)
        a2 = Answer.objects.create(text='answer2', question=q1)

        q2 = Question.objects.create(
            type=AnswerType.MULTIPLE,
            text='question two text',
            survey=survey
        )
        a3 = Answer.objects.create(text='answer3', question=q2)
        a4 = Answer.objects.create(text='answer4', question=q2)


class SurveyTestCase(TestWithFilledDb):
    def test_all_questions_can_be_queried_by_survey_title(self):
        questions = Question.objects.filter(survey__title__contains='survey title')
        self.assertEqual(len(questions), 2)
        self.assertEqual(questions[0].text, 'question one text')
        self.assertEqual(questions[1].text, 'question two text')
