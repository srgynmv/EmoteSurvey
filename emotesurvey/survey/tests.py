from django.test import TestCase
from .models import *


class TestWithQuestions(TestCase):
    def setUp(self):
        survey = Survey.objects.create(title='survey title')
        self.q1 = Question.objects.create(
            type=AnswerType.SINGLE,
            text='question one text',
            survey=survey
        )
        self.a1 = Answer.objects.create(text='answer1', question=self.q1)
        self.a2 = Answer.objects.create(text='answer2', question=self.q1)

        self.q2 = Question.objects.create(
            type=AnswerType.MULTIPLE,
            text='question two text',
            survey=survey
        )
        self.a3 = Answer.objects.create(text='answer3', question=self.q2)
        self.a4 = Answer.objects.create(text='answer4', question=self.q2)

        self.q3 = Question.objects.create(
            type=AnswerType.TEXT,
            text='question three text',
            survey=survey
        )


class SurveyTestCase(TestWithQuestions):
    def test_all_questions_can_be_queried_by_survey_title(self):
        questions = Question.objects.filter(survey__title__contains='survey title')
        self.assertEqual(len(questions), 3)
        self.assertEqual(questions[0].text, 'question one text')
        self.assertEqual(questions[1].text, 'question two text')
        self.assertEqual(questions[2].text, 'question three text')
